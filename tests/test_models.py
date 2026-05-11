"""Tests for the Pydantic request and response models."""

import pytest
from pydantic import ValidationError

from prollm.models import CompletionRequest, CompletionResponse


def test_completion_request_defaults() -> None:
    """``CompletionRequest`` populates all optional fields with documented defaults."""
    request = CompletionRequest(prompt="hi")

    assert request.max_tokens == 1024
    assert request.model is None
    assert request.prompt == "hi"
    assert request.stream is False
    assert request.temperature == 0.7


def test_completion_request_temperature_above_max_rejected() -> None:
    """``CompletionRequest`` rejects ``temperature`` greater than 2.0 (Pydantic ``le=2.0``)."""
    with pytest.raises(ValidationError):
        CompletionRequest(
            prompt="hi",
            temperature=2.5,
        )


def test_completion_request_temperature_below_min_rejected() -> None:
    """``CompletionRequest`` rejects ``temperature`` less than 0.0 (Pydantic ``ge=0.0``)."""
    with pytest.raises(ValidationError):
        CompletionRequest(
            prompt="hi",
            temperature=-0.1,
        )


def test_completion_response_construction() -> None:
    """``CompletionResponse`` round-trips a fully populated payload."""
    response = CompletionResponse(
        finish_reason="stop",
        input_tokens=5,
        model="gpt-4o",
        output_tokens=3,
        provider="openai",
        text="hi there",
    )

    assert response.finish_reason == "stop"
    assert response.input_tokens == 5
    assert response.model == "gpt-4o"
    assert response.output_tokens == 3
    assert response.provider == "openai"
    assert response.text == "hi there"


def test_completion_response_invalid_finish_reason_rejected() -> None:
    """``CompletionResponse`` rejects ``finish_reason`` values outside the ``Literal`` set."""
    with pytest.raises(ValidationError):
        CompletionResponse(
            finish_reason="exploded",  # type: ignore[arg-type]
            input_tokens=1,
            model="gpt-4o",
            output_tokens=1,
            provider="openai",
            text="hi",
        )
