"""OpenAI Chat Completions provider implementation."""

from typing import Any, ClassVar, override

from prollm.models import CompletionRequest, CompletionResponse
from prollm.providers.base import BaseProvider, ProviderRequest


class OpenAIProvider(BaseProvider):
    """Provider that calls the OpenAI Chat Completions API."""

    name: ClassVar[str] = "openai"
    default_base_url: ClassVar[str] = "https://api.openai.com/v1"
    default_model: ClassVar[str] = "gpt-4o"

    @override
    def _build_payload(
        self,
        request: CompletionRequest,
    ) -> ProviderRequest:
        """Build an OpenAI ``chat/completions`` HTTP payload.

        Args:
            request: Provider-agnostic completion request.

        Returns:
            HTTP path, headers, body, and resolved model for the OpenAI
            ``chat/completions`` endpoint.
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
                "temperature": request.temperature,
            },
            headers={"Authorization": f"Bearer {self.api_key}"},
            model=model,
            path="/chat/completions",
        )

    @override
    def _parse_success(
        self,
        data: dict[str, Any],
        model: str,
    ) -> CompletionResponse:
        """Parse an OpenAI ``chat/completions`` 200-OK payload.

        Args:
            data: Parsed JSON body returned by OpenAI.
            model: Resolved model identifier used for the request.

        Returns:
            Provider-agnostic completion response populated from the OpenAI
            ``choices[0]`` and ``usage`` payload.
        """
        choice: dict[str, Any] = data["choices"][0]
        return CompletionResponse(
            finish_reason=choice["finish_reason"],
            input_tokens=data["usage"]["prompt_tokens"],
            model=model,
            output_tokens=data["usage"]["completion_tokens"],
            provider=self.name,
            text=choice["message"]["content"],
        )
