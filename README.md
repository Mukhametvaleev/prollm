# prollm

[![CI](https://img.shields.io/github/actions/workflow/status/Mukhametvaleev/prollm/ci.yml?branch=main)](../../actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.14%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Unified, provider-agnostic Python SDK for OpenAI, Anthropic, Google Gemini, Mistral, Groq, DeepSeek, and Perplexity
completion APIs. One client, one request/response shape, sync and async.

```python
from prollm import GatewayClient

client = GatewayClient(provider="openai", api_key="sk-...")
response = client.complete("Tell me a joke")
print(response.text)
```

## Features

- **One API, multiple providers** — switch providers by changing one string
- **Sync and async** — `complete()` and `acomplete()` on every client
- **Typed responses** — Pydantic `CompletionRequest` and `CompletionResponse` models
- **Built-in retries** — OpenAI rate-limit handling via tenacity (exponential backoff, 3 attempts)
- **Structured exceptions** — `RateLimitError`, `ProviderError`, `AuthenticationError`, all rooted in `GatewayError`
- **HTTP-native** — built on `httpx`; no provider SDKs as dependencies

## Supported providers

| Provider      | Sync | Async | Default model              | API style         |
| ------------- | :--: | :---: | -------------------------- | ----------------- |
| OpenAI        |  ✅  |  ✅   | `gpt-4o`                   | Chat Completions  |
| Anthropic     |  ✅  |  ✅   | `claude-sonnet-4-20250514` | Messages          |
| Google Gemini |  ✅  |  ✅   | `gemini-1.5-pro`           | generateContent   |
| Mistral       |  ✅  |  ✅   | `mistral-large-latest`     | OpenAI-compatible |
| Groq          |  ✅  |  ✅   | `llama-3.3-70b-versatile`  | OpenAI-compatible |
| DeepSeek      |  ✅  |  ✅   | `deepseek-chat`            | OpenAI-compatible |
| Perplexity    |  ✅  |  ✅   | `sonar`                    | OpenAI-compatible |

Other OpenAI-compatible providers (Azure OpenAI, Together AI, Fireworks, OpenRouter,
Ollama, etc.) work via `OpenAIProvider` with a `base_url` override.

## Requirements

- Python 3.14+
- `httpx >= 0.27`
- `pydantic >= 2.0`
- `tenacity >= 8.0`

## Install

```bash
pip install prollm
```

Or with `uv`:

```bash
uv add prollm
```

## Quick start

### Synchronous

```python
from prollm import GatewayClient

client = GatewayClient(api_key="sk-...", provider="openai")
response = client.complete(
    "What is the capital of France?",
    max_tokens=100,
    temperature=0.2,
)
print(response.text)
print(f"Used {response.input_tokens} in / {response.output_tokens} out")
```

### Asynchronous

```python
import asyncio
from prollm import GatewayClient


async def main() -> None:
    client = GatewayClient(api_key="sk-...", provider="openai")
    response = await client.acomplete("Tell me a joke")
    print(response.text)


asyncio.run(main())
```

### Switching providers

The request and response models stay the same. Only `provider` and `api_key` change:

```python
client = GatewayClient(api_key="sk-ant-...", provider="anthropic")
response = client.complete("Hello")
```

### Selecting a model

Pass `model` to override the provider's default:

```python
response = client.complete(
    "Summarize this in one sentence...",
    model="gpt-4o-mini",
    max_tokens=80,
)
```

## API reference

### `GatewayClient(api_key, provider, **kwargs)`

| Parameter  | Type    | Required | Default      | Description                                                                                        |
| ---------- | ------- | :------: | ------------ | -------------------------------------------------------------------------------------------------- |
| `api_key`  | `str`   |    ✅    | —            | Provider API key.                                                                                  |
| `provider` | `str`   |    ✅    | —            | One of `"anthropic"`, `"deepseek"`, `"gemini"`, `"groq"`, `"mistral"`, `"openai"`, `"perplexity"`. |
| `base_url` | `str`   |          | per-provider | Override the upstream API base URL (Azure, corporate proxies, self-hosted gateways).               |
| `timeout`  | `float` |          | `30.0`       | Per-request HTTP timeout in seconds.                                                               |
| `**kwargs` | `Any`   |          |              | Reserved for future provider-specific options.                                                     |

Raises `GatewayError` if `provider` is unknown.

Example with overrides:

```python
client = GatewayClient(
    api_key="sk-...",
    provider="openai",
    base_url="https://my-azure.openai.azure.com/v1",
    timeout=10.0,
)
```

### `CompletionRequest`

| Field         | Type          | Default | Description                              |
| ------------- | ------------- | ------- | ---------------------------------------- |
| `prompt`      | `str`         | —       | User prompt (required).                  |
| `model`       | `str \| None` | `None`  | Override the provider default.           |
| `max_tokens`  | `int`         | `1024`  | Upper bound on generated tokens.         |
| `temperature` | `float`       | `0.7`   | Sampling temperature (`0.0`–`2.0`).      |
| `stream`      | `bool`        | `False` | Reserved; streaming not yet implemented. |

### `CompletionResponse`

| Field           | Type                                 | Description                        |
| --------------- | ------------------------------------ | ---------------------------------- |
| `text`          | `str`                                | Generated completion text.         |
| `provider`      | `str`                                | Provider that handled the request. |
| `model`         | `str`                                | Resolved model identifier.         |
| `input_tokens`  | `int`                                | Prompt tokens consumed.            |
| `output_tokens` | `int`                                | Generated tokens.                  |
| `finish_reason` | `Literal["error", "length", "stop"]` | Why generation stopped.            |

### Exceptions

```text
GatewayError
├── ProviderError       # any non-success HTTP response
│   └── RateLimitError  # HTTP 429 specifically
└── AuthenticationError # invalid/missing API key
```

`ProviderError.provider` and `.status_code` are accessible for branching:

```python
from prollm import GatewayClient, RateLimitError, ProviderError

try:
    response = client.complete("...")
except RateLimitError:
    # OpenAI auto-retries 3x; this fires when retries are exhausted
    ...
except ProviderError as e:
    print(f"{e.provider} returned {e.status_code}")
```

## Logging

The SDK uses the standard `logging` module under the `prollm` logger namespace. No handler is configured by the
library — the application owns logging configuration:

```python
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
```

Set `prollm` to `DEBUG` to see per-request model, token counts, and retry warnings.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Clone and install
git clone https://github.com/Mukhametvaleev/prollm
cd prollm
uv sync --group dev

# Install pre-commit hooks (linting + commit-message validation)
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg

# Run linting, formatting, type-checking
uv run pre-commit run --all-files

# Run tests with coverage
uv run pytest
```

### Project layout

```text
prollm/
├── __init__.py        # public re-exports
├── client.py          # GatewayClient — provider dispatch
├── exceptions.py      # exception hierarchy
├── models.py          # Pydantic CompletionRequest / CompletionResponse
└── providers/
    ├── base.py        # BaseProvider abstract class
    ├── anthropic.py
    ├── deepseek.py
    ├── gemini.py
    ├── groq.py
    ├── mistral.py
    ├── openai.py
    └── perplexity.py
tests/                 # 100% line + branch coverage
docs/                  # MkDocs Material site source
```

### Commit messages

This repo enforces [Conventional Commits](https://www.conventionalcommits.org/) both locally (commit-msg hook) and in
CI (PR title check). Valid prefixes: `feat`, `fix`, `perf`, `refactor`, `revert`, `docs`, `style`, `test`, `build`,
`ci`, `chore`.

```text
feat: add streaming support for OpenAI
fix(anthropic): handle empty content array
docs: clarify temperature bounds
```

### Releases

Releases are fully automated:

1. Conventional Commits merged to `develop` trigger [release-please](https://github.com/googleapis/release-please) to
   open a Release PR that bumps the version everywhere and aggregates `CHANGELOG.md`.
2. Merging the Release PR cuts a tagged GitHub Release.
3. The `Publish` workflow then builds the package, uploads to TestPyPI, waits for maintainer approval, and uploads to
   PyPI — all via [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) with
   [Sigstore attestations](https://docs.pypi.org/attestations/), no API tokens stored in CI.

See [CONTRIBUTING.md](CONTRIBUTING.md#releases) for the maintainer setup checklist.

## License

MIT — see [LICENSE](LICENSE).
