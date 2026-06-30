import time

from litellm import ModelResponse, acompletion
from litellm.exceptions import (
    APIError,
    AuthenticationError,
    LiteLLMException,
    RateLimitError,
    Timeout as LiteLLMTimeout,
)

from shared.llm.exceptions import (
    LLMAuthenticationError,
    LLMError,
    LLMProviderError,
    LLMRateLimitError,
    LLMTimeoutError,
    LLMValidationError,
)
from shared.llm.models import LLMRequest, LLMResponse, TokenUsage
from shared.logger import logger


class LiteLLMClient:
    """Client for interacting with LLM providers using the LiteLLM library."""

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a response from an LLM provider.

        Args:
            request: The request to send to the LLM.

        Returns:
            The generated LLM response.

        Raises:
            LLMValidationError: If the request is invalid.
            LLMAuthenticationError: If authentication fails.
            LLMRateLimitError: If the provider rate limit is exceeded.
            LLMTimeoutError: If the request times out.
            LLMProviderError: If the provider returns an API error.
            LLMError: For any other unexpected errors.
        """

        if request.model is None:
            raise LLMValidationError("Request model must be provided.")

        if request.provider is None:
            raise LLMValidationError("Request provider must be provided.")

        logger.debug(
            "Sending LLM request (provider=%s, model=%s)",
            request.provider.value,
            request.model,
        )

        start_time = time.perf_counter()

        try:
            response: ModelResponse = await acompletion(
                model=request.model,
                custom_llm_provider=request.provider.value,
                messages=[
                    {
                        "role": "user",
                        "content": request.prompt,
                    }
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

        except AuthenticationError as e:
            logger.exception(
                "Authentication failed for provider=%s",
                request.provider.value,
            )
            raise LLMAuthenticationError(str(e)) from e

        except RateLimitError as e:
            logger.exception(
                "Rate limit exceeded for provider=%s",
                request.provider.value,
            )
            raise LLMRateLimitError(str(e)) from e

        except LiteLLMTimeout as e:
            logger.exception(
                "Request timed out for provider=%s",
                request.provider.value,
            )
            raise LLMTimeoutError(str(e)) from e

        except APIError as e:
            logger.exception(
                "Provider API error for provider=%s",
                request.provider.value,
            )
            raise LLMProviderError(str(e)) from e

        except LiteLLMException as e:
            logger.exception("Unexpected LiteLLM error.")
            raise LLMError(f"Unexpected LiteLLM error: {e}") from e

        except Exception as e:
            logger.exception("Unexpected error while communicating with the LLM.")
            raise LLMError(f"Unexpected error: {e}") from e

        elapsed_time = time.perf_counter() - start_time

        usage: TokenUsage | None = None
        if response.usage:
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens or 0,
                completion_tokens=response.usage.completion_tokens or 0,
                total_tokens=response.usage.total_tokens or 0,
            )

        token_count: int | str = (
            usage.total_tokens if usage is not None else "unknown"
        )

        logger.debug(
            "LLM request completed (provider=%s, model=%s, time=%.2fs, total_tokens=%s)",
            request.provider.value,
            request.model,
            elapsed_time,
            token_count,
        )

        return LLMResponse(
            content=response.choices[0].message.content or "",
            provider=request.provider,
            model=request.model,
            usage=usage,
            response_time=elapsed_time,
        )