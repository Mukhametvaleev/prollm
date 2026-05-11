# Configuration

`GatewayClient` and all providers accept connection-level overrides for production use cases
(Azure OpenAI, corporate proxies, self-hosted gateways, custom timeouts).

## Constructor arguments

| Parameter  | Type    | Default      | Purpose                                              |
| ---------- | ------- | ------------ | ---------------------------------------------------- |
| `api_key`  | `str`   | —            | Provider API key (required).                         |
| `provider` | `str`   | —            | `"anthropic"`, `"gemini"`, or `"openai"` (required). |
| `base_url` | `str`   | per provider | Override the upstream API base URL.                  |
| `timeout`  | `float` | `30.0`       | Per-request HTTP timeout in seconds.                 |

## Custom `base_url`

The most common reason to override `base_url` is to point at:

- **Azure OpenAI** — `https://<resource>.openai.azure.com/v1`
- **A corporate proxy** — `https://corp-proxy.example.com/openai/v1`
- **A self-hosted gateway** (e.g. LiteLLM, OpenRouter) — `https://litellm.example.com/v1`
- **A local mock server** during tests — `http://localhost:4010/v1`

```python
from prollm import GatewayClient

client = GatewayClient(
    api_key="...",
    provider="openai",
    base_url="https://my-resource.openai.azure.com/v1",
)
```

The default base URLs are defined as class attributes on each provider:

- [`OpenAIProvider.default_base_url`][prollm.providers.openai.OpenAIProvider]:
  `https://api.openai.com/v1`
- [`AnthropicProvider.default_base_url`][prollm.providers.anthropic.AnthropicProvider]:
  `https://api.anthropic.com/v1`
- [`GeminiProvider.default_base_url`][prollm.providers.gemini.GeminiProvider]:
  `https://generativelanguage.googleapis.com/v1`

## Custom `timeout`

Default is 30 seconds. Lower for tight SLAs, higher for long-running completions on weaker models:

```python
client = GatewayClient(
    api_key="...",
    provider="openai",
    timeout=5.0,  # fail fast
)
```

The value is passed directly to `httpx`, so any value supported there works — including
`httpx.Timeout(connect=2.0, read=30.0, write=10.0, pool=2.0)` if you import `httpx` yourself.

## Logging configuration

The SDK emits structured `logging` records on the `prollm` namespace. Each provider uses its
submodule logger:

- `prollm.client` — provider dispatch
- `prollm.providers.openai` — OpenAI requests, retries, errors
- `prollm.providers.anthropic` — Anthropic requests, errors

Configure verbosity per-namespace if you want:

```python
import logging

logging.getLogger("prollm").setLevel(logging.INFO)
logging.getLogger("prollm.providers.openai").setLevel(logging.DEBUG)
```
