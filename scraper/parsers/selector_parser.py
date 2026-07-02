from __future__ import annotations

from patchright.async_api import Page
from shared.llm.selector_profile import SelectorProfile
from shared.logger import get_logger

logger = get_logger(__name__)


class SelectorParser:
    """
    Architecture:
    Page
    ↓
    SelectorParser
    ↓
    SelectorEngine
    ↓
    dict[str, object]
    ↓
    OpportunityParser
    ↓
    Opportunity

    Orchestrates the extraction of data from a page using a SelectorProfile.
    """

    def __init__(self, selector_profile: SelectorProfile) -> None:
        self._selector_profile: SelectorProfile = selector_profile

    async def parse(self, page: Page) -> dict[str, object]:
        """
        Parses the page using the loaded selector profile.
        """
        logger.debug(
            "Starting selector parsing using profile=%s",
            getattr(self._selector_profile, "name", "<unknown>"),
        )

        self._validate_profile()
        data = await self._extract_fields(page)
        data = self._postprocess(data)

        logger.debug(
            "Selector parsing completed (%d fields extracted)",
            len(data),
        )
        return data

    def _validate_profile(self) -> None:
        """Performs lightweight validation of the selector profile."""
        # TODO: Implement more robust validation
        if not self._selector_profile.selectors:
            logger.warning("SelectorProfile has no selectors defined.")

    async def _extract_fields(self, page: Page) -> dict[str, object]:
        """Extract canonical opportunity fields from the page.

        Returns:
            A dictionary compatible with OpportunityParser.
        """
        data: dict[str, object] = {}

        logger.debug(
            "Extracting %d selectors",
            len(self._selector_profile.selectors),
        )

        # TODO:
        # for field_name, selector in self._selector_profile.selectors.items():
        #     value = await SelectorEngine.extract(page, selector)
        #     data[field_name] = value

        return data

    def _postprocess(self, data: dict[str, object]) -> dict[str, object]:
        """Cleans up and normalizes the extracted data."""
        # TODO:
        # - Perform lightweight normalization after extraction.
        # - This step should remain generic and must not contain
        #   website-specific logic.
        return data
