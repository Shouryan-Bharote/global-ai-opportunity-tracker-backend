from typing import TypeVar

from pydantic import BaseModel

from shared.logger import logger
from shared.llm.client import LiteLLMClient
from shared.llm.exceptions import LLMValidationError
from shared.llm.models import (
    LLMProvider,
    LLMRequest,
    LLMResponse,
    LLMTask,
)
from shared.llm.parser import ResponseParser
from shared.llm.prompt_builder import PromptBuilder
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
        """Generates a selector profile for a webpage."""

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

        response = await self._execute_request(
            task=LLMTask.SELECTOR_GENERATION,
            prompt=prompt,
            provider=provider,
            model=model,
        )

        if not response.content.strip():
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
                    llm_provider=provider.value,
                    llm_model=model,
                )
            }
        )

        logger.debug(
            "Selector profile validation succeeded for website=%s",
            website,
        )

        logger.info(
            "Successfully generated selector profile for website=%s",
            website,
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