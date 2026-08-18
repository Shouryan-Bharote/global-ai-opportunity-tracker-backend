from __future__ import annotations

from patchright.async_api import Page
from scraper.parsers.selector_engine import SelectorEngine
from shared.llm.selector_profile import SelectorProfile
from shared.llm.validator import SelectorProfileValidator
from shared.logger import get_logger

logger = get_logger(__name__)


class SelectorParser:
    """Orchestrates the extraction of data from a page using a SelectorProfile.

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
    """

    def __init__(self, selector_profile: SelectorProfile) -> None:
        self._selector_profile: SelectorProfile = selector_profile

    async def parse(self, page: Page) -> dict[str, object]:
        """Parses the page using the loaded selector profile.

        Args:
            page: The Patchright page to extract data from.

        Returns:
            A dictionary mapping OpportunityField names to extracted values.
        """
        logger.debug(
            "Starting selector parsing for website=%s page_type=%s",
            self._selector_profile.website,
            self._selector_profile.page_type,
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
        """Validates the selector profile using SelectorProfileValidator."""
        SelectorProfileValidator.validate(self._selector_profile)

    async def _extract_fields(self, page: Page) -> dict[str, object]:
        """Extract canonical opportunity fields from the page.

        Instantiates a SelectorEngine and iterates through every
        ExtractionField in the selector profile. The engine handles
        selector priority ordering and fallback internally.

        Returns:
            A dictionary mapping field names to extracted values.
        """
        engine = SelectorEngine(page)
        data: dict[str, object] = {}

        logger.debug(
            "Extracting %d fields from profile",
            len(self._selector_profile.fields),
        )

        for field in self._selector_profile.fields:
            try:
                value = await engine.extract(field)
                data[field.name.value] = value
                logger.debug(
                    "Extracted field=%s value_type=%s",
                    field.name,
                    type(value).__name__,
                )
            except RuntimeError:
                logger.warning(
                    "Failed to extract required field=%s — skipping.",
                    field.name,
                )
            except Exception:
                logger.exception(
                    "Unexpected error extracting field=%s",
                    field.name,
                )

        return data

    def _postprocess(self, data: dict[str, object]) -> dict[str, object]:
        """Cleans up and normalizes the extracted data.

        Performs lightweight normalization:
        - Strips whitespace from string values.
        - Removes keys with None values.

        This step remains generic and must not contain website-specific logic.
        """
        cleaned: dict[str, object] = {}
        for key, value in data.items():
            if value is None:
                continue
            if isinstance(value, str):
                value = value.strip()
                if not value:
                    continue
            cleaned[key] = value
        return cleaned

