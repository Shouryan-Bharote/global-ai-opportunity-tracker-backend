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
        provider: LLMProvider,
        model: str,
        website: str,
        page_type: str,
        html: str,
        fields: list[str],
    ) -> SelectorProfile:
        """Generates a selector profile for a webpage.

        Tries the given primary provider/model first. If it fails, automatically
        falls back to Gemini (gemini-3.6-flash) as a secondary provider.
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

        # --- Primary attempt (Groq by default) ---
        response: LLMResponse | None = None
        used_provider = provider
        used_model = model

        try:
            response = await self._execute_request(
                task=LLMTask.SELECTOR_GENERATION,
                prompt=prompt,
                provider=provider,
                model=model,
            )
        except LLMError as primary_exc:
            # --- Fallback to Gemini if primary is not already Gemini ---
            fallback_provider = LLMProvider.GEMINI
            fallback_model = Providers.default_model(fallback_provider)

            if provider == fallback_provider:
                # Already on Gemini — no further fallback available
                raise

            logger.warning(
                "Primary LLM provider %s failed (%s). Falling back to %s (%s).",
                provider.value,
                primary_exc,
                fallback_provider.value,
                fallback_model,
            )

            try:
                response = await self._execute_request(
                    task=LLMTask.SELECTOR_GENERATION,
                    prompt=prompt,
                    provider=fallback_provider,
                    model=fallback_model,
                )
                used_provider = fallback_provider
                used_model = fallback_model
            except LLMError as fallback_exc:
                raise LLMError(
                    f"Both primary ({provider.value}) and fallback ({fallback_provider.value}) "
                    f"providers failed. Last error: {fallback_exc}"
                ) from fallback_exc

        if not response or not response.content.strip():
            raise LLMValidationError("LLM returned an empty response.")

        profile = self._parse_response(
            response.content,
            SelectorProfile,
        )

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