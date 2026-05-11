"""Top-level gateway client that dispatches requests to the configured provider."""

import logging
from typing import Any, Unpack, cast

from prollm.exceptions import GatewayError
from prollm.models import CompletionKwargs, CompletionRequest, CompletionResponse
from prollm.providers.anthropic import AnthropicProvider
from prollm.providers.base import BaseProvider
from prollm.providers.deepseek import DeepSeekProvider
from prollm.providers.gemini import GeminiProvider
from prollm.providers.groq import GroqProvider
from prollm.providers.mistral import MistralProvider
from prollm.providers.openai import OpenAIProvider
from prollm.providers.perplexity import PerplexityProvider

logger: logging.Logger = logging.getLogger(__name__)

_PROVIDERS: dict[str, type[BaseProvider]] = {
    "anthropic": AnthropicProvider,
    "deepseek": DeepSeekProvider,
    "gemini": GeminiProvider,
    "groq": GroqProvider,
    "mistral": MistralProvider,
    "openai": OpenAIProvider,
    "perplexity": PerplexityProvider,
}


class GatewayClient:
    """Unified client for all LLM providers."""

    _provider: BaseProvider

    def __init__(
        self,
        provider: str,
        api_key: str,
        **kwargs: Any,
    ) -> None:
        """Initialize the gateway with a provider name and API key.

        Args:
            provider: Provider key; one of "anthropic", "deepseek", "gemini",
                "groq", "mistral", "openai", or "perplexity".
            api_key: API key passed through to the underlying provider.
            **kwargs: Additional keyword arguments forwarded to the provider
                constructor (e.g. ``base_url``, ``timeout``).

        Raises:
            GatewayError: If ``provider`` is not a registered provider name.
        """
        if provider not in _PROVIDERS:
            raise GatewayError(
                f"Unknown provider: {provider!r}. Choose from {list(_PROVIDERS)}",
            )
        logger.debug(
            "Initializing GatewayClient with provider=%s",
            provider,
        )
        self._provider = _PROVIDERS[provider](
            api_key=api_key,
            **kwargs,
        )

    async def acomplete(
        self,
        prompt: str,
        **kwargs: Unpack[CompletionKwargs],
    ) -> CompletionResponse:
        """Asynchronously send a prompt to the configured provider.

        Args:
            prompt: User prompt sent to the provider as a single user message.
            **kwargs: Optional ``CompletionRequest`` fields (``model``,
                ``max_tokens``, ``temperature``, ``stream``). Typed via PEP 692
                ``Unpack`` so mypy catches typos at call sites.

        Returns:
            Provider-agnostic completion response.
        """
        request = CompletionRequest(
            prompt=prompt,
            **kwargs,
        )
        # tenacity's @retry erases the return type; cast restores it
        return cast("CompletionResponse", await self._provider.acomplete(request))

    def complete(
        self,
        prompt: str,
        **kwargs: Unpack[CompletionKwargs],
    ) -> CompletionResponse:
        """Synchronously send a prompt to the configured provider.

        Args:
            prompt: User prompt sent to the provider as a single user message.
            **kwargs: Optional ``CompletionRequest`` fields (``model``,
                ``max_tokens``, ``temperature``, ``stream``). Typed via PEP 692
                ``Unpack`` so mypy catches typos at call sites.

        Returns:
            Provider-agnostic completion response.
        """
        request = CompletionRequest(
            prompt=prompt,
            **kwargs,
        )
        # tenacity's @retry erases the return type; cast restores it
        return cast("CompletionResponse", self._provider.complete(request))
