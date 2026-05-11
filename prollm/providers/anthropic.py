"""Anthropic Claude (Messages API) provider implementation."""

from typing import Any, ClassVar, override

from prollm.models import CompletionRequest, CompletionResponse
from prollm.providers.base import BaseProvider, ProviderRequest


class AnthropicProvider(BaseProvider):
    """Provider that calls the Anthropic Messages API."""

    name: ClassVar[str] = "anthropic"
    default_base_url: ClassVar[str] = "https://api.anthropic.com/v1"
    default_model: ClassVar[str] = "claude-sonnet-4-20250514"

    @override
    def _build_payload(
        self,
        request: CompletionRequest,
    ) -> ProviderRequest:
        """Build an Anthropic ``messages`` HTTP payload.

        Args:
            request: Provider-agnostic completion request.

        Returns:
            HTTP path, headers, body, and resolved model for the Anthropic
            ``messages`` endpoint.
        """
        model: str = request.model or self.default_model
        return ProviderRequest(
            body={
                "max_tokens": request.max_tokens,
                "messages": [
                    {
                        "content": request.prompt,
                        "role": "user",
                    },
                ],
                "model": model,
            },
            headers={
                "anthropic-version": "2023-06-01",
                "x-api-key": self.api_key,
            },
            model=model,
            path="/messages",
        )

    @override
    def _parse_success(
        self,
        data: dict[str, Any],
        model: str,
    ) -> CompletionResponse:
        """Parse an Anthropic ``messages`` 200-OK payload.

        Args:
            data: Parsed JSON body returned by Anthropic.
            model: Resolved model identifier used for the request.

        Returns:
            Provider-agnostic completion response populated from the Anthropic
            ``content[0]`` and ``usage`` payload.
        """
        return CompletionResponse(
            finish_reason="stop",
            input_tokens=data["usage"]["input_tokens"],
            model=model,
            output_tokens=data["usage"]["output_tokens"],
            provider=self.name,
            text=data["content"][0]["text"],
        )
