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
from shared.llm.models import (
    LLMRequest,
    LLMResponse,
    TokenUsage,
)
from shared.llm.providers import Providers
from shared.logger import logger


class LiteLLMClient:
    """Client for interacting with LLM providers using LiteLLM."""

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a response from an LLM provider."""

        self._validate_request(request)

        provider_config = Providers.get(request.provider)

        logger.debug(
            "Sending LLM request (provider=%s, model=%s)",
            provider_config.provider_name,
            request.model,
        )

        start_time = time.perf_counter()

        try:
            response: ModelResponse = await acompletion(
                model=request.model,
                custom_llm_provider=provider_config.provider_name,
                api_key=Providers.api_key(request.provider),
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
                provider_config.provider_name,
            )
            raise LLMAuthenticationError(str(e)) from e

        except RateLimitError as e:
            logger.exception(
                "Rate limit exceeded for provider=%s",
                provider_config.provider_name,
            )
            raise LLMRateLimitError(str(e)) from e

        except LiteLLMTimeout as e:
            logger.exception(
                "Request timed out for provider=%s",
                provider_config.provider_name,
            )
            raise LLMTimeoutError(str(e)) from e

        except APIError as e:
            logger.exception(
                "Provider API error for provider=%s",
                provider_config.provider_name,
            )
            raise LLMProviderError(str(e)) from e

        except LiteLLMException as e:
            logger.exception("Unexpected LiteLLM error.")
            raise LLMError(f"Unexpected LiteLLM error: {e}") from e

        except Exception as e:
            logger.exception("Unexpected error while communicating with the LLM.")
            raise LLMError(f"Unexpected error: {e}") from e

        elapsed_time = time.perf_counter() - start_time

        usage = self._build_token_usage(response)

        logger.debug(
            "LLM request completed (provider=%s, model=%s, time=%.2fs, total_tokens=%s)",
            provider_config.provider_name,
            request.model,
            elapsed_time,
            usage.total_tokens if usage else "unknown",
        )

        return LLMResponse(
            content=response.choices[0].message.content or "",
            provider=request.provider,
            model=request.model,
            usage=usage,
            response_time=elapsed_time,
        )

    @staticmethod
    def _validate_request(request: LLMRequest) -> None:
        """Validates an LLM request before execution."""

        if request.provider is None:
            raise LLMValidationError("Request provider must be provided.")

        if request.model is None:
            raise LLMValidationError("Request model must be provided.")

        if not Providers.has_api_key(request.provider):
            raise LLMValidationError(
                f"No API key configured for provider '{request.provider.value}'."
            )

    @staticmethod
    def _build_token_usage(
        response: ModelResponse,
    ) -> TokenUsage | None:
        """Builds a TokenUsage object from a LiteLLM response."""

        if response.usage is None:
            return None

        return TokenUsage(
            prompt_tokens=response.usage.prompt_tokens or 0,
            completion_tokens=response.usage.completion_tokens or 0,
            total_tokens=response.usage.total_tokens or 0,
        )