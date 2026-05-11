# Getting started

## Requirements

- Python 3.14+
- `httpx >= 0.27`
- `pydantic >= 2.0`
- `tenacity >= 8.0`

## Install

=== "pip"

    ```bash
    pip install prollm
    ```

=== "uv"

    ```bash
    uv add prollm
    ```

## First request

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

## Switching providers

The request and response models stay the same. Only `provider` and `api_key` change:

```python
client = GatewayClient(api_key="sk-ant-...", provider="anthropic")
response = client.complete("Hello")
```

## Selecting a model

Pass `model` to override the provider's default:

```python
response = client.complete(
    "Summarize this in one sentence...",
    model="gpt-4o-mini",
    max_tokens=80,
)
```

## Handling errors

```python
from prollm import GatewayClient, ProviderError, RateLimitError

try:
    response = client.complete("...")
except RateLimitError:
    # OpenAI auto-retries 3x; this fires when retries are exhausted
    print("Provider rate-limited us. Backing off.")
except ProviderError as e:
    print(f"{e.provider} returned {e.status_code}")
```

See [Exceptions][prollm.exceptions] for the full hierarchy.

## Logging

The SDK uses the stdlib `logging` module under the `prollm` namespace. The library configures no
handlers — your application owns logging setup:

```python
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
```

Set the `prollm` logger to `DEBUG` to see per-request model, token counts, and retry warnings.
