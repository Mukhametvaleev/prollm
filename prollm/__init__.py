"""prollm: unified SDK for OpenAI, Anthropic, Gemini, Mistral, Groq, DeepSeek, Perplexity."""

from prollm.client import GatewayClient
from prollm.exceptions import (
    AuthenticationError,
    GatewayError,
    ProviderError,
    RateLimitError,
)
from prollm.models import CompletionRequest, CompletionResponse

__all__ = [
    "AuthenticationError",
    "CompletionRequest",
    "CompletionResponse",
    "GatewayClient",
    "GatewayError",
    "ProviderError",
    "RateLimitError",
]

__version__ = "0.1.0"  # x-release-please-version
