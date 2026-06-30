from shared.llm.client import LiteLLMClient
from shared.llm.models import (
    LLMProvider,
    LLMRequest,
    LLMResponse,
    LLMTask,
)
from shared.llm.parser import LLMParser
from shared.llm.prompt_builder import PromptBuilder
from shared.llm.selector_profile import SelectorProfile
from shared.llm.validator import SelectorProfileValidator


class LLMManager:
    """Coordinates all LLM operations."""

    def __init__(self, client: LiteLLMClient) -> None:
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
        """Generate a selector profile for a webpage."""

        prompt = PromptBuilder.build(
            task=LLMTask.SELECTOR_GENERATION,
            website=website,
            page_type=page_type,
            html=html,
            fields=fields,
        )

        response = await self._generate(
            task=LLMTask.SELECTOR_GENERATION,
            prompt=prompt,
            provider=provider,
            model=model,
        )

        profile = LLMParser.parse(
            response.content,
            SelectorProfile,
        )

        SelectorProfileValidator.validate(profile)

        return profile

    async def _generate(
        self,
        *,
        task: LLMTask,
        prompt: str,
        provider: LLMProvider,
        model: str,
    ) -> LLMResponse:
        """Send a request to the configured LLM."""

        request = LLMRequest(
            task=task,
            prompt=prompt,
            provider=provider,
            model=model,
        )

        return await self._client.generate(request)