# Exceptions

```text
GatewayError
├── ProviderError       # any non-success HTTP response
│   └── RateLimitError  # HTTP 429 specifically
└── AuthenticationError # invalid/missing API key
```

::: prollm.exceptions
    options:
      show_root_heading: false
