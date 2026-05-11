"""Shared HTTP response mock builders used across provider and client tests."""

from http import HTTPStatus
from unittest.mock import MagicMock


def make_anthropic_success_response() -> MagicMock:
    """Return a MagicMock shaped like a 200-OK Anthropic Messages response."""
    response_mock = MagicMock()
    response_mock.is_success = True
    response_mock.status_code = HTTPStatus.OK
    response_mock.json.return_value = {
        "content": [{"text": "Hi from Claude"}],
        "usage": {
            "input_tokens": 4,
            "output_tokens": 2,
        },
    }
    return response_mock


def make_gemini_success_response() -> MagicMock:
    """Return a MagicMock shaped like a 200-OK Gemini ``generateContent`` response."""
    response_mock = MagicMock()
    response_mock.is_success = True
    response_mock.status_code = HTTPStatus.OK
    response_mock.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": "Hi from Gemini"}],
                    "role": "model",
                },
                "finishReason": "STOP",
            },
        ],
        "usageMetadata": {
            "candidatesTokenCount": 4,
            "promptTokenCount": 6,
        },
    }
    return response_mock


def make_openai_success_response() -> MagicMock:
    """Return a MagicMock shaped like a 200-OK OpenAI Chat Completions response."""
    response_mock = MagicMock()
    response_mock.is_success = True
    response_mock.status_code = HTTPStatus.OK
    response_mock.json.return_value = {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {"content": "Hi!"},
            },
        ],
        "usage": {
            "completion_tokens": 3,
            "prompt_tokens": 5,
        },
    }
    return response_mock


def make_rate_limit_response() -> MagicMock:
    """Return a MagicMock shaped like a 429 rate-limit HTTP response (provider-agnostic)."""
    response_mock = MagicMock()
    response_mock.is_success = False
    response_mock.status_code = HTTPStatus.TOO_MANY_REQUESTS
    response_mock.text = "rate limited"
    return response_mock


def make_server_error_response() -> MagicMock:
    """Return a MagicMock shaped like a 500 server-error HTTP response (provider-agnostic)."""
    response_mock = MagicMock()
    response_mock.is_success = False
    response_mock.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    response_mock.text = "boom"
    return response_mock
