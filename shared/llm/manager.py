from typing import TypeVar

from pydantic import BaseModel

from shared.logger import logger
from shared.llm.client import LiteLLMClient
from shared.llm.exceptions import LLMError, LLMValidationError
from shared.llm.models import (
    LLMProvider,
    LLMRequest,
    LLMResponse,
    LLMTask,
)
from shared.llm.parser import ResponseParser
from shared.llm.prompt_builder import PromptBuilder
from shared.llm.providers import Providers
from shared.llm.selector_profile import GenerationMetadata, SelectorProfile
from shared.llm.validator import SelectorProfileValidator

T = TypeVar("T", bound=BaseModel)


class LLMManager:
    """Coordinates all LLM operations."""

    def __init__(self, client: LiteLLMClient) -> None:
        """Initializes the LLM manager."""
        self._client = client

    async def generate_selector_profile(
        self,
        *,
        provider: LLMProvider | None = None,
        model: str | None = None,
        website: str,
        page_type: str,
        html: str,
        fields: list[str],
    ) -> SelectorProfile:
        """Generates a selector profile for a webpage.

        Tries providers in the order returned by ``Providers.resolve_chain()``.
        If *provider* is explicitly given it is tried first (regardless of the
        chain), then the chain is consulted for fallbacks.

        Raises ``LLMError`` only when every provider in the chain has failed.
        """

        logger.info(
            "Generating selector profile for website=%s page_type=%s",
            website,
            page_type,
        )

        prompt = PromptBuilder.build(
            task=LLMTask.SELECTOR_GENERATION,
            website=website,
            page_type=page_type,
            html=html,
            fields=fields,
        )

        # Build the ordered list of (provider, model) pairs to attempt
        chain = Providers.resolve_chain()

        if not chain:
            raise LLMError(
                "No LLM provider is configured. "
                "Set at least one API key (GROQ_API_KEY, GEMINI_API_KEY, "
                "OPENROUTER_API_KEY, NVIDIA_API_KEY, or CUSTOM_API_KEY) in .env."
            )

        # If caller specified an explicit provider, put it first (deduplicated)
        if provider is not None and provider in chain:
            chain = [provider] + [p for p in chain if p != provider]
        elif provider is not None and Providers.has_api_key(provider):
            chain = [provider] + chain

        response: LLMResponse | None = None
        used_provider: LLMProvider | None = None
        used_model: str | None = None
        last_exc: Exception | None = None

        for attempt_provider in chain:
            attempt_model = (
                model
                if (model and attempt_provider == provider)
                else Providers.default_model(attempt_provider)
            )

            try:
                response = await self._execute_request(
                    task=LLMTask.SELECTOR_GENERATION,
                    prompt=prompt,
                    provider=attempt_provider,
                    model=attempt_model,
                )
                used_provider = attempt_provider
                used_model = attempt_model
                break  # Success — stop trying

            except LLMError as exc:
                logger.warning(
                    "Provider %s (%s) failed: %s. Trying next in chain...",
                    attempt_provider.value,
                    attempt_model,
                    exc,
                )
                last_exc = exc
                continue

        if response is None or not response.content.strip():
            if last_exc is not None:
                raise LLMError(
                    f"All {len(chain)} provider(s) in the chain failed. "
                    f"Last error: {last_exc}"
                ) from last_exc
            raise LLMValidationError("LLM returned an empty response.")

        profile = self._parse_response(response.content, SelectorProfile)

        SelectorProfileValidator.validate(profile)

        # Inject accurate metadata (overrides whatever the LLM guessed)
        profile = profile.model_copy(
            update={
                "metadata": GenerationMetadata(
                    llm_provider=used_provider.value,
                    llm_model=used_model,
                )
            }
        )

        logger.debug(
            "Selector profile validation succeeded for website=%s",
            website,
        )

        logger.info(
            "Successfully generated selector profile for website=%s (provider=%s model=%s)",
            website,
            used_provider.value,
            used_model,
        )

        return profile

    async def _execute_request(
        self,
        *,
        task: LLMTask,
        prompt: str,
        provider: LLMProvider,
        model: str,
    ) -> LLMResponse:
        """Creates and sends an LLM request."""

        logger.debug(
            "Executing LLM task=%s provider=%s model=%s",
            task.value,
            provider.value,
            model,
        )

        request = LLMRequest(
            task=task,
            prompt=prompt,
            provider=provider,
            model=model,
        )

        return await self._client.generate(request)

    @staticmethod
    def _parse_response(
        content: str,
        model: type[T],
    ) -> T:
        """Parses an LLM response into the specified Pydantic model."""

        logger.debug(
            "Parsing LLM response into %s",
            model.__name__,
        )

        return ResponseParser.parse(content, model)