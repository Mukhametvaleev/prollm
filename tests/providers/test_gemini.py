"""Tests for the Gemini provider."""

from http import HTTPStatus
from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture

from prollm.exceptions import ProviderError, RateLimitError
from prollm.models import CompletionRequest, CompletionResponse
from prollm.providers.gemini import GeminiProvider
from tests._factories import (
    make_gemini_success_response,
    make_rate_limit_response,
    make_server_error_response,
)


def test_complete_returns_completion_response(mocker: MockerFixture) -> None:
    """``GeminiProvider.complete`` parses a 200-OK payload into ``CompletionResponse``."""
    mocker.patch(
        "httpx.Client.post",
        return_value=make_gemini_success_response(),
    )
    provider = GeminiProvider(api_key="gem-test")
    response = provider.complete(CompletionRequest(prompt="hi"))

    assert isinstance(
        response,
        CompletionResponse,
    )
    assert response.finish_reason == "stop"
    assert response.input_tokens == 6
    assert response.model == GeminiProvider.default_model
    assert response.output_tokens == 4
    assert response.provider == "gemini"
    assert response.text == "Hi from Gemini"


def test_complete_routes_model_into_path(mocker: MockerFixture) -> None:
    """``GeminiProvider`` puts the resolved model into the URL path (Google convention)."""
    mocked_post = mocker.patch(
        "httpx.Client.post",
        return_value=make_gemini_success_response(),
    )
    provider = GeminiProvider(api_key="gem-test")
    provider.complete(
        CompletionRequest(
            model="gemini-1.5-flash",
            prompt="hi",
        ),
    )

    request_url = mocked_post.call_args.args[0]
    assert request_url.endswith("/models/gemini-1.5-flash:generateContent")


def test_complete_sends_api_key_header(mocker: MockerFixture) -> None:
    """``GeminiProvider`` authenticates via the ``x-goog-api-key`` header."""
    mocked_post = mocker.patch(
        "httpx.Client.post",
        return_value=make_gemini_success_response(),
    )
    provider = GeminiProvider(api_key="gem-test")
    provider.complete(CompletionRequest(prompt="hi"))

    headers = mocked_post.call_args.kwargs["headers"]
    assert headers["x-goog-api-key"] == "gem-test"


def test_complete_max_tokens_finish_reason(mocker: MockerFixture) -> None:
    """``GeminiProvider`` maps Gemini ``MAX_TOKENS`` to ``length`` finish reason."""
    response_mock = make_gemini_success_response()
    response_mock.json.return_value["candidates"][0]["finishReason"] = "MAX_TOKENS"
    mocker.patch(
        "httpx.Client.post",
        return_value=response_mock,
    )
    provider = GeminiProvider(api_key="gem-test")
    response = provider.complete(CompletionRequest(prompt="hi"))

    assert response.finish_reason == "length"


def test_complete_unknown_finish_reason_maps_to_error(mocker: MockerFixture) -> None:
    """``GeminiProvider`` maps unrecognized Gemini finish reasons to ``error``."""
    response_mock = make_gemini_success_response()
    response_mock.json.return_value["candidates"][0]["finishReason"] = "SAFETY"
    mocker.patch(
        "httpx.Client.post",
        return_value=response_mock,
    )
    provider = GeminiProvider(api_key="gem-test")
    response = provider.complete(CompletionRequest(prompt="hi"))

    assert response.finish_reason == "error"


def test_complete_rate_limit_raises(mocker: MockerFixture) -> None:
    """``GeminiProvider.complete`` raises ``RateLimitError`` on persistent 429s."""
    mocker.patch(
        "httpx.Client.post",
        return_value=make_rate_limit_response(),
    )
    provider = GeminiProvider(api_key="gem-test")

    with pytest.raises(RateLimitError):
        provider.complete(CompletionRequest(prompt="hi"))


def test_complete_non_success_raises_provider_error(mocker: MockerFixture) -> None:
    """``GeminiProvider.complete`` raises ``ProviderError`` on non-429 failure responses."""
    mocker.patch(
        "httpx.Client.post",
        return_value=make_server_error_response(),
    )
    provider = GeminiProvider(api_key="gem-test")

    with pytest.raises(ProviderError) as exception_info:
        provider.complete(CompletionRequest(prompt="hi"))

    assert exception_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


async def test_acomplete_returns_completion_response(mocker: MockerFixture) -> None:
    """``GeminiProvider.acomplete`` parses a 200-OK payload into ``CompletionResponse``."""
    mocker.patch(
        "httpx.AsyncClient.post",
        new=AsyncMock(return_value=make_gemini_success_response()),
    )
    provider = GeminiProvider(api_key="gem-test")
    response = await provider.acomplete(CompletionRequest(prompt="hi"))

    assert isinstance(
        response,
        CompletionResponse,
    )
    assert response.provider == "gemini"
    assert response.text == "Hi from Gemini"
