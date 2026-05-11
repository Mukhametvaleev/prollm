"""Exception hierarchy raised by the prollm SDK."""


class GatewayError(Exception):
    """Base exception for prollm."""


class ProviderError(GatewayError):
    """Raised when an upstream provider returns a non-success HTTP response."""

    provider: str
    status_code: int

    def __init__(
        self,
        provider: str,
        status_code: int,
        message: str,
    ) -> None:
        """Build a ProviderError from the upstream provider response.

        Args:
            provider: Name of the provider that produced the error (e.g. "openai").
            status_code: HTTP status code returned by the provider.
            message: Body or error message returned by the provider.
        """
        self.provider = provider
        self.status_code = int(status_code)
        super().__init__(f"[{provider}] {self.status_code}: {message}")


class RateLimitError(ProviderError):
    """Provider rate limit exceeded."""


class AuthenticationError(GatewayError):
    """Invalid or missing API key."""
