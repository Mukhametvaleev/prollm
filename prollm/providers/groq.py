"""Groq provider — OpenAI-compatible ``/chat/completions`` endpoint."""

from typing import ClassVar

from prollm.providers.openai import OpenAIProvider


class GroqProvider(OpenAIProvider):
    """Groq Cloud provider.

    Groq exposes an OpenAI-compatible Chat Completions API, so this class
    inherits ``OpenAIProvider``'s request/response logic verbatim and only
    overrides the provider identity and connection defaults.
    """

    name: ClassVar[str] = "groq"
    default_base_url: ClassVar[str] = "https://api.groq.com/openai/v1"
    default_model: ClassVar[str] = "llama-3.3-70b-versatile"
