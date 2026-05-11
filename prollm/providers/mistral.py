"""Mistral AI provider — OpenAI-compatible ``/chat/completions`` endpoint."""

from typing import ClassVar

from prollm.providers.openai import OpenAIProvider


class MistralProvider(OpenAIProvider):
    """Mistral AI provider.

    Mistral exposes an OpenAI-compatible Chat Completions API, so this class
    inherits ``OpenAIProvider``'s request/response logic verbatim and only
    overrides the provider identity and connection defaults.
    """

    name: ClassVar[str] = "mistral"
    default_base_url: ClassVar[str] = "https://api.mistral.ai/v1"
    default_model: ClassVar[str] = "mistral-large-latest"
