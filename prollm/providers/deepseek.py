"""DeepSeek provider — OpenAI-compatible ``/chat/completions`` endpoint."""

from typing import ClassVar

from prollm.providers.openai import OpenAIProvider


class DeepSeekProvider(OpenAIProvider):
    """DeepSeek provider.

    DeepSeek exposes an OpenAI-compatible Chat Completions API, so this class
    inherits ``OpenAIProvider``'s request/response logic verbatim and only
    overrides the provider identity and connection defaults.
    """

    name: ClassVar[str] = "deepseek"
    default_base_url: ClassVar[str] = "https://api.deepseek.com/v1"
    default_model: ClassVar[str] = "deepseek-chat"
