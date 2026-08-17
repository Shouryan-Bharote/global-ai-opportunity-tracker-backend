# scraper/scrapers/devpost/scraper.py
"""DevpostScraper: concrete scraper for devpost.com."""
from __future__ import annotations

import asyncio

from patchright.async_api import Locator

from scraper.core.browser.models import BrowserLaunchOptions
from scraper.parsers.opportunity_parser import OpportunityParser
from scraper.parsers.selector_parser import SelectorParser
from scraper.scrapers.base import BaseScraper
from scraper.scrapers.devpost.profile_manager import DevpostProfileManager
from shared.llm.client import LiteLLMClient
from shared.llm.manager import LLMManager
from shared.llm.models import LLMProvider
from shared.llm.providers import Providers
from shared.llm.selector_profile import SelectorProfile
from shared.logger import get_logger
from shared.models.enums import OpportunityField, OpportunitySource
from shared.models.opportunity import Opportunity

logger = get_logger(__name__)

# Devpost native filter URL for AI/ML theme hackathons (both online and in-person, open + upcoming)
# We use the built-in filter system instead of search queries for accuracy.
_DEVPOST_BASE_URL = (
    "https://devpost.com/hackathons"
    "?challenge_type[]=online"
    "&challenge_type[]=in-person"
    "&open_to[]=public"
    "&status[]=upcoming"
    "&status[]=open"
    "&themes[]=Machine%20Learning%2FAI"
)

# Fields we ask the LLM to generate selectors for (card-level extraction).
# NOTE: registration_fee is intentionally excluded — Devpost hackathons are free
# and the prize-amount selector is easily confused with a fee by LLMs.
_TARGET_FIELDS: list[str] = [
    OpportunityField.TITLE,
    OpportunityField.DESCRIPTION,
    OpportunityField.IMAGE_URL,
    OpportunityField.SOURCE_URL,
    OpportunityField.TAGS,
]

# Real Devpost card selectors
_CARD_SELECTORS = [
    ".hackathon-tile",
    "div.hackathon-tile",
    "[class*='hackathon-tile']",
]

# Wait timeout for cards
_CARD_WAIT_TIMEOUT = 10_000

# Safety limit for pages per search query
_MAX_PAGES = 3


class DevpostScraper(BaseScraper):
    """Concrete scraper for devpost.com AI hackathons and challenges."""

    def __init__(
        self,
        options: BrowserLaunchOptions | None = None,
        provider: LLMProvider = LLMProvider.GROQ,
    ) -> None:
        """Initialize DevpostScraper.

        Args:
            options: Browser launch options.
            provider: LLM provider for selector generation.
        """
        super().__init__(options)
        self._provider = provider
        self._model = Providers.default_model(provider)
        self._llm_manager = LLMManager(LiteLLMClient())
        self._profile_manager = DevpostProfileManager()
        self._opportunity_parser = OpportunityParser()

    def _build_target_url(self) -> str:
        """Construct the Devpost AI/ML filtered listing URL."""
        return _DEVPOST_BASE_URL

    async def scrape(self) -> list[Opportunity]:
        """Execute Devpost scraping pipeline across target search queries.

        Returns:
            A list of unique parsed Opportunity models.
        """
        if not self.browser_manager.is_running():
            await self.start()

        seen_urls: set[str] = set()
        opportunities: list[Opportunity] = []
        profile = None

        try:
            target_url = self._build_target_url()
            logger.info("Scraping Devpost AI/ML events (url=%s)", target_url)

            await self.goto(target_url, wait_until="domcontentloaded")
            await asyncio.sleep(2)
            await self._wait_for_cards()

            if profile is None:
                profile = await self._get_or_generate_profile()

            selector_parser = SelectorParser(profile)
            
            previous_count = 0
            # Treat _MAX_PAGES as max scrolls + 1 initial load
            for scroll_num in range(_MAX_PAGES):
                cards = await self._locate_cards()
                current_count = await cards.count()

                if current_count == previous_count:
                    logger.info("No more cards loaded after scroll %d — stopping.", scroll_num)
                    break

                logger.info("Found %d total opportunity cards on Devpost (newly loaded: %d).", 
                            current_count, current_count - previous_count)

                # Only parse the newly loaded cards
                for i in range(previous_count, current_count):
                    card = cards.nth(i)
                    try:
                        raw_data = await selector_parser.parse(card)  # type: ignore[arg-type]
                        source_url = raw_data.get("source_url") or target_url

                        # Clean up Devpost query ref params from URL
                        if "?" in source_url:
                            source_url = source_url.split("?")[0]

                        if source_url in seen_urls:
                            logger.debug("Duplicate Devpost opportunity skipped: %s", source_url)
                            continue

                        raw_data["source"] = OpportunitySource.DEVPOST
                        raw_data["source_url"] = source_url
                        raw_data["id"] = source_url
                        raw_data["type"] = "hackathon"
                        raw_data["status"] = "open"
                        # Devpost hackathons are free — hard-code to avoid
                        # LLM confusing prize counts with registration fees.
                        raw_data["registration_fee"] = 0.0
                        raw_data.setdefault("organizer", {"name": "Devpost"})
                        raw_data.setdefault("location", {"type": "online"})
                        raw_data.setdefault("timeline", {})

                        # Normalize protocol-relative image URLs (//cdn...) → https://
                        img = raw_data.get("image_url")
                        if isinstance(img, str) and img.startswith("//"):
                            raw_data["image_url"] = "https:" + img

                        opportunity = self._opportunity_parser.parse(raw_data)
                        opportunities.append(opportunity)
                        seen_urls.add(source_url)
                        logger.debug("Parsed Devpost opportunity: %s", opportunity.title)

                    except Exception:
                        logger.warning(
                            "Failed to parse card %d on Devpost — skipping.",
                            i,
                            exc_info=True,
                        )
                
                previous_count = current_count
                
                # Scroll down to load more if not on last iteration
                if scroll_num < _MAX_PAGES - 1:
                    logger.info("Scrolling down to load more Devpost events...")
                    await self.page.keyboard.press("End")
                    await asyncio.sleep(3)  # Wait for API and DOM update

        finally:
            await self.stop()

        logger.info(
            "Devpost scrape complete: %d unique AI/ML opportunities collected.",
            len(opportunities),
        )
        return opportunities

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _wait_for_cards(self) -> None:
        """Wait for at least one card element to appear."""
        for selector in _CARD_SELECTORS:
            try:
                locator = self.page.locator(selector).first
                await locator.wait_for(timeout=_CARD_WAIT_TIMEOUT)
                logger.debug("Devpost cards loaded using selector: %s", selector)
                return
            except Exception:
                pass
        logger.warning(
            "No Devpost cards appeared using any known selector — page may have changed."
        )

    async def _locate_cards(self) -> Locator:
        """Return a Patchright Locator matching all cards."""
        for selector in _CARD_SELECTORS:
            locator = self.page.locator(selector)
            if await locator.count() > 0:
                return locator
        return self.page.locator(_CARD_SELECTORS[0])

    async def _get_or_generate_profile(self) -> SelectorProfile:
        """Load profile from disk or call LLMManager to generate a new one."""
        cached_profile = self._profile_manager.load()
        if cached_profile is not None:
            return cached_profile

        logger.info("Generating new Devpost SelectorProfile via LLM (%s)...", self._model)

        cards = await self._locate_cards()
        if await cards.count() == 0:
            raise RuntimeError("Cannot generate profile: 0 cards found on page.")

        first_card = cards.first
        card_html = await first_card.inner_html()

        profile = await self._llm_manager.generate_selector_profile(
            provider=self._provider,
            model=self._model,
            website="https://devpost.com",
            page_type="card",
            html=card_html,
            fields=_TARGET_FIELDS,
        )

        self._profile_manager.save(profile)
        return profile
