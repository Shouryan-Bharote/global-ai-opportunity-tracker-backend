from __future__ import annotations
from functools import cached_property

from typing import Any, Callable, Coroutine
from patchright.async_api import Page, Locator
from shared.llm.selector_profile import ExtractionField, Selector
from shared.logger import get_logger


logger = get_logger(__name__)

ExtractionResult = object

ExtractionHandler = Callable[
    [Selector],
    Coroutine[Any, Any, ExtractionResult],
]



class SelectorEngine:


    """
    Core extraction engine responsible for executing individual selector definitions.
    
    The engine dispatches extraction tasks based on the selector type to 
    specialized internal methods.
    """

    def __init__(self, page: Page) -> None:
        self._page = page

    @cached_property
    def _dispatch_map(self) -> dict[str, ExtractionHandler]:
        return {
            "text": self._extract_text,
            "attribute": self._extract_attribute,
            "html": self._extract_html,
            "elements": self._extract_elements,
            "json": self._extract_json,
            "table": self._extract_table,
            "list": self._extract_list,
        }

    def _locator(
        self,
        selector: Selector,
    ) -> Locator:

        return self._page.locator(selector.value)

    async def extract(self, selector: Selector) -> object:


        """Executes the extraction for a given selector definition."""
        logger.debug(
            "Starting extraction for type=%s, value=%s",
            selector.type,
            selector.value,
        )

        handler = self._dispatch_map.get(selector.type)
        if not handler:
            supported_types = sorted(self._dispatch_map.keys())
            raise ValueError(
                f"Unsupported selector type: {selector.type}. "
                f"Supported selector types: {supported_types}"
            )

        try:
            result = await handler(selector)
            logger.debug("Successfully extracted value for type=%s", selector.type)

            return result
        except Exception:
            logger.exception("Failed to extract value for type=%s", selector.type)
            raise

    async def _extract_text(self, selector: Selector) -> object:

        """
        TODO:
        - Use locator.text_content()
        - Normalize whitespace
        - Return None if missing
        """
        raise NotImplementedError("Text extraction not implemented yet.")

    async def _extract_attribute(self, selector: Selector) -> object:

        """

        TODO:
        - Get attribute value from locator
        - Handle missing attributes
        """
        raise NotImplementedError("Attribute extraction not implemented yet.")

    async def _extract_html(self, selector: Selector) -> object:

        """
        TODO:
        - Use locator.inner_html()
        """
        raise NotImplementedError("HTML extraction not implemented yet.")

    async def _extract_elements(self, selector: Selector) -> object:

        """
        TODO:
        - Return list of elements or count
        """
        raise NotImplementedError("Element extraction not implemented yet.")

    async def _extract_json(self, selector: Selector) -> object:

        """
        TODO:
        - Extract from script tags or JSON-LD
        """
        raise NotImplementedError("JSON extraction not implemented yet.")

    async def _extract_table(self, selector: Selector) -> object:

        """
        TODO:
        - Parse table elements into list of dicts
        """
        raise NotImplementedError("Table extraction not implemented yet.")

    async def _extract_list(self, selector: Selector) -> object:


        """
        TODO:
        - Iterate over multiple elements
        - Return collection
        """
        raise NotImplementedError("List extraction not implemented yet.")
