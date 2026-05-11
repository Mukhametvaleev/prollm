"""Tests for the GatewayClient public surface."""

from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture

from prollm import GatewayClient
from prollm.exceptions import GatewayError
from prollm.models import CompletionResponse
from tests._factories import make_openai_success_response


def test_unknown_provider_raises() -> None:
    """Constructing GatewayClient with an unknown provider raises GatewayError."""
    with pytest.raises(
        GatewayError,
        match="Unknown provider",
    ):
        GatewayClient(
            api_key="test",
            provider="unknown",
        )


@pytest.mark.parametrize(
    "provider",
    [
        "anthropic",
        "deepseek",
        "gemini",
        "groq",
        "mistral",
        "openai",
        "perplexity",
    ],
)
def test_known_providers_construct(provider: str) -> None:
    """Each registered provider key constructs without raising."""
    client = GatewayClient(
        api_key="x",
        provider=provider,
    )

    assert client is not None


def test_complete_returns_response(mocker: MockerFixture) -> None:
    """``GatewayClient.complete`` returns a ``CompletionResponse`` from the provider HTTP response.

    Args:
        mocker: pytest-mock fixture used to patch ``httpx.Client.post``.
    """
    mocker.patch(
        "httpx.Client.post",
        return_value=make_openai_success_response(),
    )
    client = GatewayClient(
        api_key="sk-test",
        provider="openai",
    )
    response = client.complete("Hello!")

    assert isinstance(
        response,
        CompletionResponse,
    )
    assert response.provider == "openai"
    assert response.text == "Hi!"


async def test_acomplete_returns_response(mocker: MockerFixture) -> None:
    """``GatewayClient.acomplete`` dispatches async and returns a ``CompletionResponse``.

    Args:
        mocker: pytest-mock fixture used to patch ``httpx.AsyncClient.post``.
    """
    mocker.patch(
        "httpx.AsyncClient.post",
        new=AsyncMock(return_value=make_openai_success_response()),
    )
    client = GatewayClient(
        api_key="sk-test",
        provider="openai",
    )
    response = await client.acomplete("Hello!")

    assert isinstance(
        response,
        CompletionResponse,
    )
    assert response.provider == "openai"
    assert response.text == "Hi!"
