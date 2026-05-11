"""Google Gemini (generativelanguage.googleapis.com) provider implementation."""

from typing import Any, ClassVar, Literal, override

from prollm.models import CompletionRequest, CompletionResponse
from prollm.providers.base import BaseProvider, ProviderRequest

FinishReason = Literal["error", "length", "stop"]

_FINISH_REASON_MAP: dict[str, FinishReason] = {
    "MAX_TOKENS": "length",
    "STOP": "stop",
}


class GeminiProvider(BaseProvider):
    """Provider that calls the Google Gemini ``generateContent`` API."""

    name: ClassVar[str] = "gemini"
    default_base_url: ClassVar[str] = "https://generativelanguage.googleapis.com/v1beta"
    default_model: ClassVar[str] = "gemini-1.5-pro"

    @override
    def _build_payload(
        self,
        request: CompletionRequest,
    ) -> ProviderRequest:
        """Build a Gemini ``generateContent`` HTTP payload.

        Args:
            request: Provider-agnostic completion request.

        Returns:
            HTTP path, headers, body, and resolved model for the Gemini
            ``/models/{model}:generateContent`` endpoint.
        """
        model: str = request.model or self.default_model
        return ProviderRequest(
            body={
                "contents": [
                    {
                        "parts": [{"text": request.prompt}],
                        "role": "user",
                    },
                ],
                "generationConfig": {
                    "maxOutputTokens": request.max_tokens,
                    "temperature": request.temperature,
                },
            },
            headers={"x-goog-api-key": self.api_key},
            model=model,
            path=f"/models/{model}:generateContent",
        )

    @override
    def _parse_success(
        self,
        data: dict[str, Any],
        model: str,
    ) -> CompletionResponse:
        """Parse a Gemini ``generateContent`` 200-OK payload.

        Args:
            data: Parsed JSON body returned by Gemini.
            model: Resolved model identifier used for the request.

        Returns:
            Provider-agnostic completion response populated from the Gemini
            ``candidates[0]`` and ``usageMetadata`` payload.
        """
        candidate: dict[str, Any] = data["candidates"][0]
        usage: dict[str, Any] = data["usageMetadata"]
        finish_reason: FinishReason = _FINISH_REASON_MAP.get(
            candidate["finishReason"],
            "error",
        )
        return CompletionResponse(
            finish_reason=finish_reason,
            input_tokens=usage["promptTokenCount"],
            model=model,
            output_tokens=usage.get("candidatesTokenCount", 0),
            provider=self.name,
            text=candidate["content"]["parts"][0]["text"],
        )
