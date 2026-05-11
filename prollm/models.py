"""Pydantic request and response models shared across all providers."""

from typing import Literal, TypedDict

from pydantic import BaseModel, Field


class CompletionKwargs(TypedDict, total=False):
    """Typed kwargs forwarded through ``GatewayClient.complete`` / ``acomplete``.

    Mirrors the optional fields of ``CompletionRequest`` so mypy can catch typos
    like ``temprature=0.5`` at type-check time (PEP 692).
    """

    max_tokens: int
    model: str | None
    stream: bool
    temperature: float


class CompletionRequest(BaseModel):
    """Provider-agnostic completion request payload."""

    max_tokens: int = Field(
        default=1024,
        description="Maximum number of tokens the provider may generate.",
    )
    model: str | None = Field(
        default=None,
        description="Provider-specific model identifier; falls back to provider default when None.",
    )
    prompt: str = Field(
        description="User prompt sent to the model as a single user message.",
    )
    stream: bool = Field(
        default=False,
        description="Whether to stream tokens as they are produced (not yet implemented).",
    )
    temperature: float = Field(
        default=0.7,
        description="Sampling temperature; higher is more random, lower is more deterministic.",
        ge=0.0,
        le=2.0,
    )


class CompletionResponse(BaseModel):
    """Provider-agnostic completion response payload."""

    finish_reason: Literal["error", "length", "stop"] = Field(
        description="Why the provider stopped: natural stop, hit max_tokens, or error.",
    )
    input_tokens: int = Field(
        description="Tokens consumed by the prompt as reported by the provider.",
    )
    model: str = Field(
        description="Resolved model identifier the provider actually used.",
    )
    output_tokens: int = Field(description="Tokens generated in the completion.")
    provider: str = Field(
        description="Name of the provider that handled the request (e.g. 'openai').",
    )
    text: str = Field(description="Generated completion text.")
