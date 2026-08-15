from __future__ import annotations
from functools import cached_property

from typing import Any, Callable, Coroutine
from patchright.async_api import Page, Locator
from shared.llm.selector_profile import (
    ExtractionField,
    ExtractionType,
    Selector,
    SelectorType,
)
from shared.logger import get_logger

import json

logger = get_logger(__name__)

ExtractionResult = str | list[str] | list[dict[str, str]] | None

ExtractionHandler = Callable[
    [ExtractionField, Locator],
    Coroutine[Any, Any, ExtractionResult],
]


class SelectorEngine:
    """Core extraction engine responsible for executing selector-based extraction.

    The engine locates elements on the page using the selectors defined in an
    ExtractionField, then dispatches the actual data extraction to a handler
    determined by the field's extraction_type.
    """

    def __init__(self, page: Page) -> None:
        self._page = page

    @cached_property
    def _dispatch_map(self) -> dict[ExtractionType, ExtractionHandler]:
        return {
            ExtractionType.TEXT: self._extract_text,
            ExtractionType.ATTRIBUTE: self._extract_attribute,
            ExtractionType.HTML: self._extract_html,
            ExtractionType.LIST: self._extract_list,
            ExtractionType.TABLE: self._extract_table,
            ExtractionType.JSON: self._extract_json,
        }

    def _locator(self, selector: Selector) -> Locator:
        """Create a Patchright locator from a Selector definition."""
        if selector.type == SelectorType.XPATH:
            return self._page.locator(f"xpath={selector.value}")
        return self._page.locator(selector.value)

    async def _wait_if_needed(
        self,
        locator: Locator,
        selector: Selector,
    ) -> None:
        """Waits for a locator to be visible if the selector requests it."""
        if selector.wait_for:
            timeout = selector.timeout or 5000
            await locator.first.wait_for(state="visible", timeout=timeout)

    async def extract(self, field: ExtractionField) -> ExtractionResult:
        """Try each selector in priority order and return the first successful result.

        Args:
            field: The ExtractionField containing selectors and extraction type.

        Returns:
            The extracted value, or None if all selectors fail on an optional field.

        Raises:
            ValueError: If the extraction type is unsupported.
            RuntimeError: If all selectors fail on a required field.
        """
        handler = self._dispatch_map.get(field.extraction_type)
        if not handler:
            supported = sorted(t.value for t in self._dispatch_map)
            raise ValueError(
                f"Unsupported extraction type: {field.extraction_type}. "
                f"Supported types: {supported}"
            )

        last_error: Exception | None = None

        for selector in field.ordered_selectors():
            logger.debug(
                "Trying selector type=%s value=%s for field=%s",
                selector.type,
                selector.value,
                field.name,
            )
            try:
                locator = self._locator(selector)
                await self._wait_if_needed(locator, selector)
                result = await handler(field, locator)

                if result is not None:
                    logger.debug(
                        "Successfully extracted field=%s using selector=%s",
                        field.name,
                        selector.value,
                    )
                    return result

            except Exception as exc:
                logger.debug(
                    "Selector failed for field=%s value=%s: %s",
                    field.name,
                    selector.value,
                    exc,
                )
                last_error = exc

        # All selectors exhausted
        if field.required:
            raise RuntimeError(
                f"All selectors failed for required field '{field.name}'."
            ) from last_error

        logger.debug(
            "All selectors failed for optional field=%s, using default=%s",
            field.name,
            field.default,
        )
        return field.default

    # ------------------------------------------------------------------
    # Extraction handlers
    # ------------------------------------------------------------------

    async def _extract_text(
        self,
        field: ExtractionField,
        locator: Locator,
    ) -> str | None:
        """Extract normalized text content from the first matched element."""
        raw = await locator.first.text_content()
        if raw is None:
            return None
        text = " ".join(raw.split())
        return text or None

    async def _extract_attribute(
        self,
        field: ExtractionField,
        locator: Locator,
    ) -> str | None:
        """Extract an HTML attribute value from the first matched element."""
        if not field.attribute:
            raise ValueError(
                f"Field '{field.name}' uses ATTRIBUTE extraction but "
                f"no attribute name is specified."
            )
        return await locator.first.get_attribute(field.attribute)

    async def _extract_html(
        self,
        field: ExtractionField,
        locator: Locator,
    ) -> str | None:
        """Extract the inner HTML of the first matched element."""
        html = await locator.first.inner_html()
        return html or None

    async def _extract_list(
        self,
        field: ExtractionField,
        locator: Locator,
    ) -> list[str]:
        """Extract text from all matched elements as a list."""
        elements = locator.all()
        raw_texts = await locator.all_text_contents()
        return [" ".join(t.split()) for t in raw_texts if t.strip()]

    async def _extract_table(
        self,
        field: ExtractionField,
        locator: Locator,
    ) -> list[dict[str, str]]:
        """Extract an HTML table as a list of row dicts.

        Assumes the first <tr> (or <thead>) contains header cells and
        subsequent rows contain data cells.
        """
        rows = locator.first.locator("tr")
        row_count = await rows.count()
        if row_count == 0:
            return []

        # Extract headers from the first row
        header_cells = rows.nth(0).locator("th, td")
        header_count = await header_cells.count()
        headers: list[str] = []
        for i in range(header_count):
            text = await header_cells.nth(i).text_content() or ""
            headers.append(" ".join(text.split()))

        # Extract data from remaining rows
        result: list[dict[str, str]] = []
        for row_idx in range(1, row_count):
            cells = rows.nth(row_idx).locator("td")
            cell_count = await cells.count()
            row_data: dict[str, str] = {}
            for col_idx in range(min(cell_count, len(headers))):
                text = await cells.nth(col_idx).text_content() or ""
                row_data[headers[col_idx]] = " ".join(text.split())
            result.append(row_data)

        return result

    async def _extract_json(
        self,
        field: ExtractionField,
        locator: Locator,
    ) -> str | None:
        """Extract and return JSON text content (e.g. from <script> tags)."""
        raw = await locator.first.text_content()
        if raw is None:
            return None

        # Validate it is parseable JSON and return the raw string
        try:
            json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Content matched by selector for field '{field.name}' "
                f"is not valid JSON."
            ) from exc

        return raw

