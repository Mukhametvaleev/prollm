"""Tests for the Anthropic provider."""

from http import HTTPStatus
from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture

from prollm.exceptions import ProviderError, RateLimitError
from prollm.models import CompletionRequest, CompletionResponse
from prollm.providers.anthropic import AnthropicProvider
from tests._factories import (
    make_anthropic_success_response,
    make_rate_limit_response,
    make_server_error_response,
)


def test_complete_returns_completion_response(mocker: MockerFixture) -> None:
    """``AnthropicProvider.complete`` parses a 200-OK payload into ``CompletionResponse``."""
    mocker.patch(
        "httpx.Client.post",
        return_value=make_anthropic_success_response(),
    )
    provider = AnthropicProvider(api_key="sk-test")
    response = provider.complete(CompletionRequest(prompt="hi"))

    assert isinstance(
        response,
        CompletionResponse,
    )
    assert response.finish_reason == "stop"
    assert response.input_tokens == 4
    assert response.model == AnthropicProvider.default_model
    assert response.output_tokens == 2
    assert response.provider == "anthropic"
    assert response.text == "Hi from Claude"


def test_complete_rate_limit_raises(mocker: MockerFixture) -> None:
    """``AnthropicProvider.complete`` raises ``RateLimitError`` on persistent 429s."""
    mocker.patch(
        "httpx.Client.post",
        return_value=make_rate_limit_response(),
    )
    provider = AnthropicProvider(api_key="sk-test")

    with pytest.raises(RateLimitError):
        provider.complete(CompletionRequest(prompt="hi"))


def test_complete_non_success_raises_provider_error(mocker: MockerFixture) -> None:
    """``AnthropicProvider.complete`` raises ``ProviderError`` on non-429 failure responses."""
    mocker.patch(
        "httpx.Client.post",
        return_value=make_server_error_response(),
    )
    provider = AnthropicProvider(api_key="sk-test")

    with pytest.raises(ProviderError) as exception_info:
        provider.complete(CompletionRequest(prompt="hi"))

    assert exception_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


async def test_acomplete_returns_completion_response(mocker: MockerFixture) -> None:
    """``AnthropicProvider.acomplete`` parses a 200-OK payload into ``CompletionResponse``."""
    mocker.patch(
        "httpx.AsyncClient.post",
        new=AsyncMock(return_value=make_anthropic_success_response()),
    )
    provider = AnthropicProvider(api_key="sk-test")
    response = await provider.acomplete(CompletionRequest(prompt="hi"))

    assert isinstance(
        response,
        CompletionResponse,
    )
    assert response.provider == "anthropic"
    assert response.text == "Hi from Claude"
