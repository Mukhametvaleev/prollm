"""Abstract base class with shared HTTP, retry, and error-handling machinery."""

import logging
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any, ClassVar, NamedTuple

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from prollm.exceptions import ProviderError, RateLimitError
from prollm.models import CompletionRequest, CompletionResponse

logger: logging.Logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_SECONDS: float = 30.0

_RETRY_DECORATOR = retry(
    reraise=True,
    retry=retry_if_exception_type(RateLimitError),
    stop=stop_after_attempt(3),
    wait=wait_exponential(max=10, min=2, multiplier=1),
)


class ProviderRequest(NamedTuple):
    """Provider-specific HTTP request payload built by ``_build_payload``.

    Attributes:
        body: Request JSON body, sent as ``json=...`` to httpx.
        headers: Request headers (auth + provider-specific keys).
        model: Resolved model identifier (request override or provider default).
        path: URL path relative to ``base_url``, e.g. ``/chat/completions``.
    """

    body: dict[str, Any]
    headers: dict[str, str]
    model: str
    path: str


class BaseProvider(ABC):
    """Common interface and shared transport for every concrete provider.

    Concrete subclasses implement two abstract methods — ``_build_payload`` and
    ``_parse_success`` — and set the three ``ClassVar`` constants. All HTTP
    transport, retry, and error handling lives here.
    """

    name: ClassVar[str]
    default_base_url: ClassVar[str]
    default_model: ClassVar[str]

    api_key: str
    base_url: str
    timeout: float

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        """Store credentials and connection-level settings.

        Args:
            api_key: API key used when authenticating with the provider.
            base_url: Override the provider's default base URL (Azure, proxies,
                self-hosted gateways). Falls back to ``default_base_url`` when None.
            timeout: Per-request HTTP timeout in seconds.
        """
        self.api_key = api_key
        self.base_url = base_url if base_url is not None else self.default_base_url
        self.timeout = timeout

    @_RETRY_DECORATOR
    async def acomplete(
        self,
        request: CompletionRequest,
    ) -> CompletionResponse:
        """Asynchronously perform a completion against the provider.

        Args:
            request: Provider-agnostic completion request.

        Returns:
            Provider-agnostic completion response.

        Raises:
            RateLimitError: When the provider returns HTTP 429 after retries.
            ProviderError: When the provider returns any other non-success status.
        """
        payload = self._build_payload(request)
        logger.debug(
            "%s async request: model=%s max_tokens=%s",
            self.name,
            payload.model,
            request.max_tokens,
        )
        async with httpx.AsyncClient() as client:
            resp: httpx.Response = await client.post(
                f"{self.base_url}{payload.path}",
                headers=payload.headers,
                json=payload.body,
                timeout=self.timeout,
            )
        return self._handle_response(resp, payload.model)

    @_RETRY_DECORATOR
    def complete(
        self,
        request: CompletionRequest,
    ) -> CompletionResponse:
        """Synchronously perform a completion against the provider.

        Args:
            request: Provider-agnostic completion request.

        Returns:
            Provider-agnostic completion response.

        Raises:
            RateLimitError: When the provider returns HTTP 429 after retries.
            ProviderError: When the provider returns any other non-success status.
        """
        payload = self._build_payload(request)
        logger.debug(
            "%s sync request: model=%s max_tokens=%s",
            self.name,
            payload.model,
            request.max_tokens,
        )
        with httpx.Client() as client:
            resp: httpx.Response = client.post(
                f"{self.base_url}{payload.path}",
                headers=payload.headers,
                json=payload.body,
                timeout=self.timeout,
            )
        return self._handle_response(resp, payload.model)

    @abstractmethod
    def _build_payload(
        self,
        request: CompletionRequest,
    ) -> ProviderRequest:
        """Build the provider-specific HTTP request payload.

        Args:
            request: Provider-agnostic completion request.

        Returns:
            Provider-specific HTTP path, headers, body, and resolved model.
        """

    def _handle_response(
        self,
        resp: httpx.Response,
        model: str,
    ) -> CompletionResponse:
        """Map an HTTP response into a ``CompletionResponse`` or raise.

        Args:
            resp: Raw httpx response from the provider.
            model: Resolved model identifier (for logging + response metadata).

        Returns:
            Parsed completion response on success.

        Raises:
            RateLimitError: On HTTP 429.
            ProviderError: On any other non-success status.
        """
        if resp.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            logger.warning("%s rate limit hit (model=%s)", self.name, model)
            raise RateLimitError(
                self.name,
                HTTPStatus.TOO_MANY_REQUESTS,
                "Rate limit exceeded",
            )
        if not resp.is_success:
            logger.error(
                "%s request failed: status=%s body=%s",
                self.name,
                resp.status_code,
                resp.text,
            )
            raise ProviderError(
                self.name,
                resp.status_code,
                resp.text,
            )
        return self._parse_success(resp.json(), model)

    @abstractmethod
    def _parse_success(
        self,
        data: dict[str, Any],
        model: str,
    ) -> CompletionResponse:
        """Parse a successful provider response into a ``CompletionResponse``.

        Args:
            data: Parsed JSON body returned by the provider.
            model: Resolved model identifier used for the request.

        Returns:
            Provider-agnostic completion response.
        """
