# API reference

The full public surface of `prollm`. All types and methods documented here are part of the
stable API contract.

- [GatewayClient](client.md) — the top-level entrypoint
- [Models](models.md) — `CompletionRequest`, `CompletionResponse`
- [Exceptions](exceptions.md) — error types raised by the SDK
- [Providers](providers.md) — direct access to per-provider classes (advanced)

## Public re-exports

::: prollm
    options:
      show_root_heading: false
      show_source: false
      members:
        - GatewayClient
        - CompletionRequest
        - CompletionResponse
        - GatewayError
        - ProviderError
        - RateLimitError
