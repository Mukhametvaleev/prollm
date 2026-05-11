"""Tests for OpenAI-compatible providers (Mistral, Groq, DeepSeek).

These providers inherit ``OpenAIProvider``'s request/response logic and only
override ``name``, ``default_base_url``, and ``default_model``. We verify the
identity (constants) and one happy-path round trip per provider.
"""

from pytest_mock import MockerFixture

from prollm.models import CompletionRequest
from prollm.providers.deepseek import DeepSeekProvider
from prollm.providers.groq import GroqProvider
from prollm.providers.mistral import MistralProvider
from prollm.providers.openai import OpenAIProvider
from prollm.providers.perplexity import PerplexityProvider
from tests._factories import make_openai_success_response


def test_mistral_identity() -> None:
    """``MistralProvider`` declares its name and Mistral-specific defaults."""
    assert issubclass(MistralProvider, OpenAIProvider)
    assert MistralProvider.name == "mistral"
    assert MistralProvider.default_base_url == "https://api.mistral.ai/v1"
    assert MistralProvider.default_model == "mistral-large-latest"


def test_mistral_complete_returns_response(mocker: MockerFixture) -> None:
    """``MistralProvider.complete`` reuses OpenAI logic and returns provider='mistral'."""
    post = mocker.patch(
        "httpx.Client.post",
        return_value=make_openai_success_response(),
    )
    provider = MistralProvider(api_key="mistral-test")
    response = provider.complete(CompletionRequest(prompt="hi"))

    assert response.provider == "mistral"
    assert response.text == "Hi!"
    assert post.call_args.args[0].startswith("https://api.mistral.ai/v1")


def test_groq_identity() -> None:
    """``GroqProvider`` declares its name and Groq-specific defaults."""
    assert issubclass(GroqProvider, OpenAIProvider)
    assert GroqProvider.name == "groq"
    assert GroqProvider.default_base_url == "https://api.groq.com/openai/v1"
    assert GroqProvider.default_model == "llama-3.3-70b-versatile"


def test_groq_complete_returns_response(mocker: MockerFixture) -> None:
    """``GroqProvider.complete`` reuses OpenAI logic and returns provider='groq'."""
    post = mocker.patch(
        "httpx.Client.post",
        return_value=make_openai_success_response(),
    )
    provider = GroqProvider(api_key="groq-test")
    response = provider.complete(CompletionRequest(prompt="hi"))

    assert response.provider == "groq"
    assert response.text == "Hi!"
    assert post.call_args.args[0].startswith("https://api.groq.com/openai/v1")


def test_deepseek_identity() -> None:
    """``DeepSeekProvider`` declares its name and DeepSeek-specific defaults."""
    assert issubclass(DeepSeekProvider, OpenAIProvider)
    assert DeepSeekProvider.name == "deepseek"
    assert DeepSeekProvider.default_base_url == "https://api.deepseek.com/v1"
    assert DeepSeekProvider.default_model == "deepseek-chat"


def test_deepseek_complete_returns_response(mocker: MockerFixture) -> None:
    """``DeepSeekProvider.complete`` reuses OpenAI logic and returns provider='deepseek'."""
    post = mocker.patch(
        "httpx.Client.post",
        return_value=make_openai_success_response(),
    )
    provider = DeepSeekProvider(api_key="ds-test")
    response = provider.complete(CompletionRequest(prompt="hi"))

    assert response.provider == "deepseek"
    assert response.text == "Hi!"
    assert post.call_args.args[0].startswith("https://api.deepseek.com/v1")


def test_perplexity_identity() -> None:
    """``PerplexityProvider`` declares its name and Perplexity-specific defaults."""
    assert issubclass(PerplexityProvider, OpenAIProvider)
    assert PerplexityProvider.name == "perplexity"
    assert PerplexityProvider.default_base_url == "https://api.perplexity.ai"
    assert PerplexityProvider.default_model == "sonar"


def test_perplexity_complete_returns_response(mocker: MockerFixture) -> None:
    """``PerplexityProvider.complete`` reuses OpenAI logic and returns provider='perplexity'."""
    post = mocker.patch(
        "httpx.Client.post",
        return_value=make_openai_success_response(),
    )
    provider = PerplexityProvider(api_key="pplx-test")
    response = provider.complete(CompletionRequest(prompt="hi"))

    assert response.provider == "perplexity"
    assert response.text == "Hi!"
    assert post.call_args.args[0] == "https://api.perplexity.ai/chat/completions"
