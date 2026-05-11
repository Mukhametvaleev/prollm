# prollm

Unified, provider-agnostic Python SDK for OpenAI, Anthropic, and Google Gemini completion APIs.
One client, one request/response shape, sync and async.

```python
from prollm import GatewayClient

client = GatewayClient(api_key="sk-...", provider="openai")
response = client.complete("Tell me a joke")
print(response.text)
```

## Features

- **One API, multiple providers** — switch providers by changing one string
- **Sync and async** — `complete()` and `acomplete()` on every client
- **Typed responses** — Pydantic [`CompletionRequest`][prollm.models.CompletionRequest] and
  [`CompletionResponse`][prollm.models.CompletionResponse] models
- **Built-in retries** — OpenAI rate-limit handling via tenacity (exponential backoff, 3 attempts)
- **Structured exceptions** — [`RateLimitError`][prollm.exceptions.RateLimitError],
  [`ProviderError`][prollm.exceptions.ProviderError],
  [`AuthenticationError`][prollm.exceptions.AuthenticationError], all rooted in
  [`GatewayError`][prollm.exceptions.GatewayError]
- **HTTP-native** — built on `httpx`; no provider SDKs as dependencies
- **Fully typed** — ships with `py.typed`, mypy-strict consumers get full type info

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

## Next steps

- [Getting started](getting-started.md) — install and send your first request
- [Configuration](configuration.md) — base URLs, timeouts, custom proxies
- [API reference](reference/index.md) — full type and method docs

## License

MIT — see [LICENSE](https://github.com/Mukhametvaleev/prollm/blob/main/LICENSE).
