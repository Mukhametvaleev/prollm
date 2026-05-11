"""Tests for the prollm exception hierarchy."""

from http import HTTPStatus

from prollm.exceptions import (
    AuthenticationError,
    GatewayError,
    ProviderError,
    RateLimitError,
)


def test_authentication_error_is_gateway_error() -> None:
    """``AuthenticationError`` inherits from ``GatewayError``."""
    assert issubclass(
        AuthenticationError,
        GatewayError,
    )


def test_provider_error_formats_message() -> None:
    """``ProviderError`` renders ``[provider] status: message`` in its string form."""
    error = ProviderError(
        "openai",
        HTTPStatus.INTERNAL_SERVER_ERROR,
        "boom",
    )

    assert error.provider == "openai"
    assert error.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert str(error) == "[openai] 500: boom"


def test_provider_error_is_gateway_error() -> None:
    """``ProviderError`` inherits from ``GatewayError``."""
    assert issubclass(
        ProviderError,
        GatewayError,
    )


def test_rate_limit_error_is_provider_error() -> None:
    """``RateLimitError`` inherits from ``ProviderError`` and preserves attributes."""
    error = RateLimitError(
        "openai",
        HTTPStatus.TOO_MANY_REQUESTS,
        "Rate limit exceeded",
    )

    assert isinstance(
        error,
        ProviderError,
    )
    assert error.provider == "openai"
    assert error.status_code == HTTPStatus.TOO_MANY_REQUESTS
