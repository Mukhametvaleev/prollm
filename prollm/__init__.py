"""prollm: unified SDK for OpenAI, Anthropic, and Gemini LLM providers."""

from prollm.client import GatewayClient
from prollm.exceptions import GatewayError, ProviderError, RateLimitError
from prollm.models import CompletionRequest, CompletionResponse

__all__ = [
    "CompletionRequest",
    "CompletionResponse",
    "GatewayClient",
    "GatewayError",
    "ProviderError",
    "RateLimitError",
]

__version__ = "0.1.0"  # x-release-please-version
