class LLMError(Exception):
    """Base class for all LLM-related errors."""


class LLMValidationError(LLMError):
    """Raised when the LLM request or response is invalid."""


class LLMProviderError(LLMError):
    """Error raised when an LLM provider returns an error."""


class LLMAuthenticationError(LLMError):
    """Error raised when authentication with an LLM provider fails."""


class LLMResponseParseError(LLMError):
    """Raised when the LLM response cannot be parsed."""


class LLMRateLimitError(LLMProviderError):
    """Raised when rate limits are exceeded."""


class LLMTimeoutError(LLMProviderError):
    """Raised when the request to the LLM provider times out."""
