"""Tests for the OpenAI provider."""

from http import HTTPStatus
from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture

from prollm.exceptions import ProviderError, RateLimitError
from prollm.models import CompletionRequest, CompletionResponse
from prollm.providers.openai import OpenAIProvider
from tests._factories import (
    make_openai_success_response,
    make_rate_limit_response,
    make_server_error_response,
)


def test_complete_returns_completion_response(mocker: MockerFixture) -> None:
    """``OpenAIProvider.complete`` parses a 200-OK payload into ``CompletionResponse``."""
    mocker.patch(
        "httpx.Client.post",
        return_value=make_openai_success_response(),
    )
    provider = OpenAIProvider(api_key="sk-test")
    response = provider.complete(CompletionRequest(prompt="hi"))

    assert isinstance(
        response,
        CompletionResponse,
    )
    assert response.finish_reason == "stop"
    assert response.input_tokens == 5
    assert response.model == OpenAIProvider.default_model
    assert response.output_tokens == 3
    assert response.provider == "openai"
    assert response.text == "Hi!"


def test_complete_uses_request_model_override(mocker: MockerFixture) -> None:
    """``OpenAIProvider.complete`` honors ``request.model`` over ``default_model``."""
    mocker.patch(
        "httpx.Client.post",
        return_value=make_openai_success_response(),
    )
    provider = OpenAIProvider(api_key="sk-test")
    response = provider.complete(
        CompletionRequest(
            model="gpt-4o-mini",
            prompt="hi",
        ),
    )

    assert response.model == "gpt-4o-mini"


def test_complete_honors_custom_base_url_and_timeout(mocker: MockerFixture) -> None:
    """``OpenAIProvider`` forwards ``base_url`` + ``timeout`` to the HTTP request."""
    mocked_post = mocker.patch(
        "httpx.Client.post",
        return_value=make_openai_success_response(),
    )
    provider = OpenAIProvider(
        api_key="sk-test",
        base_url="https://corp-proxy.example.com/openai/v1",
        timeout=5.0,
    )
    provider.complete(CompletionRequest(prompt="hi"))

    call_args = mocked_post.call_args
    assert call_args.args[0] == "https://corp-proxy.example.com/openai/v1/chat/completions"
    assert call_args.kwargs["timeout"] == 5.0


def test_provider_defaults_when_no_overrides() -> None:
    """``OpenAIProvider`` falls back to ``default_base_url`` and the default timeout."""
    provider = OpenAIProvider(api_key="sk-test")

    assert provider.base_url == OpenAIProvider.default_base_url
    assert provider.timeout == 30.0


def test_complete_rate_limit_raises_after_retries(mocker: MockerFixture) -> None:
    """``OpenAIProvider.complete`` raises ``RateLimitError`` and retries on persistent 429s."""
    mocked_post = mocker.patch(
        "httpx.Client.post",
        return_value=make_rate_limit_response(),
    )
    provider = OpenAIProvider(api_key="sk-test")

    with pytest.raises(RateLimitError):
        provider.complete(CompletionRequest(prompt="hi"))

    assert mocked_post.call_count == 3


def test_complete_non_success_raises_provider_error(mocker: MockerFixture) -> None:
    """``OpenAIProvider.complete`` raises ``ProviderError`` on non-429 failure responses."""
    mocker.patch(
        "httpx.Client.post",
        return_value=make_server_error_response(),
    )
    provider = OpenAIProvider(api_key="sk-test")

    with pytest.raises(ProviderError) as exception_info:
        provider.complete(CompletionRequest(prompt="hi"))

    assert exception_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


async def test_acomplete_returns_completion_response(mocker: MockerFixture) -> None:
    """``OpenAIProvider.acomplete`` parses a 200-OK payload into ``CompletionResponse``."""
    mocker.patch(
        "httpx.AsyncClient.post",
        new=AsyncMock(return_value=make_openai_success_response()),
    )
    provider = OpenAIProvider(api_key="sk-test")
    response = await provider.acomplete(CompletionRequest(prompt="hi"))

    assert isinstance(
        response,
        CompletionResponse,
    )
    assert response.text == "Hi!"


async def test_acomplete_rate_limit_raises_after_retries(mocker: MockerFixture) -> None:
    """``OpenAIProvider.acomplete`` raises ``RateLimitError`` after exhausting retries."""
    mocked_post = AsyncMock(return_value=make_rate_limit_response())
    mocker.patch(
        "httpx.AsyncClient.post",
        new=mocked_post,
    )
    provider = OpenAIProvider(api_key="sk-test")

    with pytest.raises(RateLimitError):
        await provider.acomplete(CompletionRequest(prompt="hi"))

    assert mocked_post.await_count == 3


async def test_acomplete_non_success_raises_provider_error(mocker: MockerFixture) -> None:
    """``OpenAIProvider.acomplete`` raises ``ProviderError`` on non-429 failure responses."""
    mocker.patch(
        "httpx.AsyncClient.post",
        new=AsyncMock(return_value=make_server_error_response()),
    )
    provider = OpenAIProvider(api_key="sk-test")

    with pytest.raises(ProviderError) as exception_info:
        await provider.acomplete(CompletionRequest(prompt="hi"))

    assert exception_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
