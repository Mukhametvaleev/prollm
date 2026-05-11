"""Perplexity AI provider — OpenAI-compatible ``/chat/completions`` endpoint."""

from typing import ClassVar

from prollm.providers.openai import OpenAIProvider


class PerplexityProvider(OpenAIProvider):
    """Perplexity AI provider.

    Perplexity exposes an OpenAI-compatible Chat Completions API at
    ``https://api.perplexity.ai/chat/completions``, so this class inherits
    ``OpenAIProvider``'s request/response logic verbatim and only overrides
    the provider identity and connection defaults.
    """

    name: ClassVar[str] = "perplexity"
    default_base_url: ClassVar[str] = "https://api.perplexity.ai"
    default_model: ClassVar[str] = "sonar"
