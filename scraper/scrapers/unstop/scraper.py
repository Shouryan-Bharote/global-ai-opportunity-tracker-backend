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

# Target AI-related categories on Unstop
DEFAULT_AI_CATEGORIES = [
    "artificial-intelligence-machine-learning",
    "data-analytics",
    "data-science",
]

# Target event types on Unstop
DEFAULT_EVENT_TYPES = [
    "hackathons",
    "competitions",
    "quizzes",
    "conferences",
]

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

# Selectors for Unstop's Angular <app-pagination> control
_NEXT_PAGE_SELECTORS = [
    "app-pagination li.right-arrow:not(.disabled)",
    "div.pagination li.right-arrow:not(.disabled)",
    "li.right-arrow:not(.disabled)",
    "button[class*='load-more']",
]

# Maximum pages to scrape per event type (safety limit)
_MAX_PAGES = 5


class UnstopScraper(BaseScraper):
    """Concrete scraper for unstop.com AI/ML opportunity listings.

    Supports category-filtered URLs across multiple event types (hackathons,
    competitions, quizzes, etc.) and deduplicates parsed opportunities.
    """

    def __init__(
        self,
        options: BrowserLaunchOptions | None = None,
        provider: LLMProvider = LLMProvider.GROQ,
        event_types: list[str] | None = None,
        categories: list[str] | None = None,
    ) -> None:
        """Initialize UnstopScraper.

        Args:
            options: Browser launch options.
            provider: LLM provider to use for selector generation.
            event_types: List of Unstop event types to scrape (e.g. ['hackathons', 'competitions']).
            categories: List of Unstop categories to filter by (e.g. ['artificial-intelligence-machine-learning']).
        """
        super().__init__(options)
        self._provider = provider
        self._model = Providers.default_model(provider)
        self._event_types = event_types or DEFAULT_EVENT_TYPES
        self._categories = categories or DEFAULT_AI_CATEGORIES
        self._llm_manager = LLMManager(LiteLLMClient())
        self._profile_manager = UnstopProfileManager()
        self._opportunity_parser = OpportunityParser()

    def _build_target_url(self, event_type: str) -> str:
        """Construct the category-filtered listing URL for a given event type.

        Example:
            https://unstop.com/hackathons?oppstatus=open&category=artificial-intelligence-machine-learning:data-analytics
        """
        cat_query = ":".join(self._categories)
        return f"https://unstop.com/{event_type}?oppstatus=open&category={cat_query}"

    async def scrape(self) -> list[Opportunity]:
        """Execute the full Unstop scraping pipeline across all target event types.

        Returns:
            A list of unique parsed Opportunity models.
        """
        seen_urls: set[str] = set()
        opportunities: list[Opportunity] = []

        profile = None

        for event_type in self._event_types:
            target_url = self._build_target_url(event_type)
            logger.info("Scraping Unstop category: %s (url=%s)", event_type, target_url)

            await self.goto(target_url, wait_until="domcontentloaded")
            await self._dismiss_cookie_banner()
            await self._dismiss_login_modal()
            await self._wait_for_cards()

            if profile is None:
                profile = await self._get_or_generate_profile()

            selector_parser = SelectorParser(profile)
            pages_scraped = 0

            while pages_scraped < _MAX_PAGES:
                logger.info("Scraping %s — page %d/%d", event_type, pages_scraped + 1, _MAX_PAGES)

                cards = await self._locate_cards()
                card_count = await cards.count()

                logger.info("Found %d opportunity cards on this page.", card_count)

                for i in range(card_count):
                    card = cards.nth(i)
                    try:
                        raw_data = await selector_parser.parse(card)  # type: ignore[arg-type]
                        source_url = raw_data.get("source_url") or target_url

                        if source_url in seen_urls:
                            logger.debug("Duplicate opportunity skipped: %s", source_url)
                            continue

                        raw_data["source"] = OpportunitySource.UNSTOP
                        raw_data["source_url"] = source_url
                        raw_data["id"] = source_url
                        raw_data["type"] = event_type.rstrip("s")  # e.g. hackathons -> hackathon
                        raw_data["status"] = "open"
                        raw_data.setdefault("organizer", {"name": "Unstop"})
                        raw_data.setdefault("location", {"type": "online"})
                        raw_data.setdefault("timeline", {})

                        opportunity = self._opportunity_parser.parse(raw_data)
                        opportunities.append(opportunity)
                        seen_urls.add(source_url)
                        logger.debug("Parsed opportunity: %s", opportunity.title)

                    except Exception:
                        logger.warning(
                            "Failed to parse card %d on %s page %d — skipping.",
                            i,
                            event_type,
                            pages_scraped + 1,
                            exc_info=True,
                        )

                current_page = pages_scraped + 1
                pages_scraped += 1

                if pages_scraped >= _MAX_PAGES:
                    logger.info("Reached max pages limit (%d) for %s — moving to next type.", _MAX_PAGES, event_type)
                    break

                if not await self._click_next_page(current_page):
                    logger.info("No next page button for %s — moving to next type.", event_type)
                    break

                await asyncio.sleep(_PAGINATION_DELAY_S)
                await self._wait_for_cards()

        logger.info(
            "Unstop scrape complete: %d unique AI opportunities collected across %d categories.",
            len(opportunities),
            len(self._event_types),
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
        # 1. Try pressing Escape key twice
        try:
            await self.page.keyboard.press("Escape")
            await self.page.keyboard.press("Escape")
        except Exception:
            pass

        # 2. Directly purge any overlay modal containers from DOM via JS
        try:
            await self.page.evaluate("""() => {
                const overlays = document.querySelectorAll(
                    '.cdk-overlay-container, .un_modal_right_bg, [aria-label*="un-modal"], .cdk-overlay-backdrop, mat-dialog-container'
                );
                overlays.forEach(el => el.remove());
            }""")
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

    async def _click_next_page(self, current_page_num: int) -> bool:
        """Click the next page number or right arrow in app-pagination.

        Args:
            current_page_num: The 1-based index of the page currently being scraped.

        Returns:
            True if navigation to the next page succeeded, False otherwise.
        """
        # Ensure any newly popped overlays are purged before clicking
        await self._dismiss_login_modal()

        # Try clicking the next page number directly (e.g. page 2, 3)
        next_num_selector = f"app-pagination li.num span:has-text('{current_page_num + 1}')"
        try:
            btn = self.page.locator(next_num_selector).first
            if await btn.is_visible(timeout=2000):
                await btn.click()
                logger.info("Navigated to page %d via page number click.", current_page_num + 1)
                return True
        except Exception:
            pass

        # Fallback to right-arrow button
        for selector in _NEXT_PAGE_SELECTORS:
            try:
                btn = self.page.locator(selector).first
                if await btn.is_visible(timeout=2000):
                    await btn.click()
                    logger.info("Navigated to next page via right arrow selector: %s", selector)
                    return True
            except Exception:
                pass

        return False
