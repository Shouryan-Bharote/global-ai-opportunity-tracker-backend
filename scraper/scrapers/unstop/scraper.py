# scraper/scrapers/unstop/scraper.py
"""UnstopScraper: concrete scraper for unstop.com."""
from __future__ import annotations

import asyncio

from patchright.async_api import Locator

from scraper.core.browser.models import BrowserLaunchOptions
from scraper.parsers.opportunity_parser import OpportunityParser
from scraper.parsers.selector_parser import SelectorParser
from scraper.scrapers.base import BaseScraper
from scraper.scrapers.unstop.profile_manager import UnstopProfileManager
from shared.llm.client import LiteLLMClient
from shared.llm.manager import LLMManager
from shared.llm.models import LLMProvider
from shared.llm.providers import Providers
from shared.logger import get_logger
from shared.models.enums import OpportunityField, OpportunitySource
from shared.models.opportunity import Opportunity

logger = get_logger(__name__)

# The Unstop listing page for hackathons / competitions
_LISTING_URL = "https://unstop.com/hackathons"

# Fields we ask the LLM to generate selectors for (card-level extraction)
_TARGET_FIELDS: list[str] = [
    OpportunityField.TITLE,
    OpportunityField.DESCRIPTION,
    OpportunityField.IMAGE_URL,
    OpportunityField.SOURCE_URL,
    OpportunityField.TAGS,
    OpportunityField.TEAM_SIZE_MIN,
    OpportunityField.TEAM_SIZE_MAX,
    OpportunityField.REGISTRATION_FEE,
]

# Real Unstop card selectors (discovered from live page DOM inspection)
# Cards are <a> elements with class 'item opp_XXXXX position-relative'
_CARD_SELECTORS = [
    "a[class*='item'][class*='opp_']",
    "a.item.position-relative",
    "a[id^='i_']",
    "[itemtype*='ListItem'][defercontent]",
]

# How long to wait (ms) for cards to appear after page load
_CARD_WAIT_TIMEOUT = 10_000

# Pause between pagination steps to avoid rate limiting
_PAGINATION_DELAY_S = 2.0

# CSS selector for the "Load More" button
_LOAD_MORE_SELECTOR = "button[class*='load-more'], button[class*='see-more'], a[class*='load-more']"

# Maximum pages to scrape in one run (safety limit)
_MAX_PAGES = 5


class UnstopScraper(BaseScraper):
    """Concrete scraper for unstop.com opportunity listings.

    Responsibilities:
    - Navigate to the Unstop listing page.
    - Handle cookie consent dismissal.
    - Locate opportunity cards on the page.
    - Use LLMManager to generate/load a SelectorProfile for card data.
    - Extract raw field dictionaries via SelectorParser.
    - Parse raw dicts into Opportunity models via OpportunityParser.
    - Handle "Load More" pagination up to _MAX_PAGES.

    This class must NOT contain parsing logic, HTML selectors for field
    extraction, or any LLM prompt engineering — that lives in SelectorParser
    and LLMManager respectively.
    """

    def __init__(
        self,
        options: BrowserLaunchOptions | None = None,
        provider: LLMProvider = LLMProvider.GROQ,
    ) -> None:
        """Initialize UnstopScraper.

        Args:
            options: Browser launch options.
            provider: LLM provider to use for selector generation.
        """
        super().__init__(options)
        self._provider = provider
        self._model = Providers.default_model(provider)
        self._llm_manager = LLMManager(LiteLLMClient())
        self._profile_manager = UnstopProfileManager()
        self._opportunity_parser = OpportunityParser()

    async def scrape(self) -> list[Opportunity]:
        """Execute the full Unstop scraping pipeline.

        Returns:
            A list of parsed Opportunity models.
        """
        logger.info("Starting Unstop scrape (url=%s)", _LISTING_URL)

        await self.goto(_LISTING_URL, wait_until="domcontentloaded")
        await self._dismiss_cookie_banner()
        await self._dismiss_login_modal()
        await self._wait_for_cards()

        profile = await self._get_or_generate_profile()
        selector_parser = SelectorParser(profile)

        opportunities: list[Opportunity] = []
        pages_scraped = 0

        while pages_scraped < _MAX_PAGES:
            logger.info("Scraping page %d/%d", pages_scraped + 1, _MAX_PAGES)

            cards = await self._locate_cards()
            card_count = await cards.count()

            logger.info("Found %d opportunity cards on this page.", card_count)

            for i in range(card_count):
                card = cards.nth(i)
                try:
                    raw_data = await selector_parser.parse(card)  # type: ignore[arg-type]
                    raw_data["source"] = OpportunitySource.UNSTOP
                    raw_data["source_url"] = raw_data.get("source_url") or _LISTING_URL
                    raw_data["id"] = raw_data.get("source_url") or f"unstop-{i}"
                    raw_data["type"] = "hackathon"
                    raw_data["status"] = "open"
                    raw_data.setdefault("organizer", {"name": "Unstop"})
                    raw_data.setdefault("location", {"type": "online"})
                    raw_data.setdefault("timeline", {})

                    opportunity = self._opportunity_parser.parse(raw_data)
                    opportunities.append(opportunity)
                    logger.debug("Parsed opportunity: %s", opportunity.title)

                except Exception:
                    logger.warning(
                        "Failed to parse card %d on page %d — skipping.",
                        i,
                        pages_scraped + 1,
                        exc_info=True,
                    )

            pages_scraped += 1

            if not await self._click_load_more():
                logger.info("No 'Load More' button found — stopping pagination.")
                break

            await asyncio.sleep(_PAGINATION_DELAY_S)

        logger.info(
            "Unstop scrape complete: %d opportunities collected.", len(opportunities)
        )
        return opportunities

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _dismiss_cookie_banner(self) -> None:
        """Attempt to dismiss a cookie consent banner if visible."""
        cookie_selectors = [
            "button[id*='cookie'][id*='accept']",
            "button[class*='cookie'][class*='accept']",
            "button:has-text('Accept')",
            "button:has-text('Accept All')",
            "button:has-text('Got it')",
        ]
        for selector in cookie_selectors:
            try:
                btn = self.page.locator(selector).first
                if await btn.is_visible(timeout=2000):
                    await btn.click()
                    logger.debug("Dismissed cookie banner via selector: %s", selector)
                    return
            except Exception:
                pass

    async def _dismiss_login_modal(self) -> None:
        """Attempt to dismiss login popup modal if visible."""
        # Try pressing Escape key
        try:
            await self.page.keyboard.press("Escape")
            await asyncio.sleep(0.5)
        except Exception:
            pass

        # Try clicking common close button selectors
        close_selectors = [
            "button.close",
            "span.close",
            "div.close",
            "i.close",
            "[class*='close']",
            "mat-icon:has-text('close')",
            ".cdk-overlay-backdrop",
        ]
        for selector in close_selectors:
            try:
                btn = self.page.locator(selector).first
                if await btn.is_visible(timeout=1000):
                    await btn.click()
                    logger.debug("Dismissed login modal via selector: %s", selector)
                    return
            except Exception:
                pass

    async def _wait_for_cards(self) -> None:
        """Wait for at least one opportunity card to appear on the page."""
        for selector in _CARD_SELECTORS:
            try:
                await self.page.locator(selector).first.wait_for(
                    state="visible",
                    timeout=_CARD_WAIT_TIMEOUT,
                )
                logger.debug("Cards visible using selector: %s", selector)
                return
            except Exception:
                continue

        logger.warning(
            "No opportunity cards found using any known selector. "
            "The page structure may have changed."
        )

    async def _locate_cards(self) -> Locator:
        """Return a Locator pointing to all opportunity cards on the current page."""
        for selector in _CARD_SELECTORS:
            locator = self.page.locator(selector)
            count = await locator.count()
            if count > 0:
                return locator

        # Fallback: return an empty locator so the scrape loop exits gracefully
        return self.page.locator("__no_match__")

    async def _get_or_generate_profile(self):
        """Load the saved SelectorProfile or generate a new one via the LLM.

        Returns:
            A valid SelectorProfile for the Unstop listing cards.
        """
        # Try loading from disk first
        cached = self._profile_manager.load()
        if cached is not None:
            logger.info("Loaded cached Unstop SelectorProfile from disk.")
            return cached

        logger.info("No cached profile found — generating via LLM.")

        # Locate the cards and grab the outer HTML of the first card
        cards = await self._locate_cards()
        if await cards.count() > 0:
            card_html = await cards.first.evaluate("el => el.outerHTML")
            logger.debug("Extracted card HTML (length=%d chars) for LLM context.", len(card_html))
        else:
            # Fallback to page content if cards aren't located yet
            card_html = (await self.page.content())[:15_000]

        profile = await self._llm_manager.generate_selector_profile(
            provider=self._provider,
            model=self._model,
            website="unstop.com",
            page_type="hackathon_listing_card",
            html=card_html,
            fields=[f.value for f in _TARGET_FIELDS],
        )

        self._profile_manager.save(profile)
        logger.info("Generated and cached new Unstop SelectorProfile.")
        return profile

    async def _click_load_more(self) -> bool:
        """Click the 'Load More' button if it is visible.

        Returns:
            True if the button was found and clicked, False otherwise.
        """
        try:
            btn = self.page.locator(_LOAD_MORE_SELECTOR).first
            if await btn.is_visible(timeout=3000):
                await btn.click()
                logger.debug("Clicked 'Load More' button.")
                return True
        except Exception:
            pass
        return False
