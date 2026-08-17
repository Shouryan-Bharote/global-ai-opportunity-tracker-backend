# scraper/scrapers/devpost/scraper.py
"""DevpostScraper: concrete scraper for devpost.com."""
from __future__ import annotations

import asyncio

from scraper.core.browser.models import BrowserLaunchOptions
from scraper.parsers.opportunity_parser import OpportunityParser
from scraper.parsers.selector_parser import SelectorParser
from scraper.scrapers.base import BaseScraper
from scraper.scrapers.devpost.profile_manager import DevpostProfileManager
from shared.llm.client import LiteLLMClient
from shared.llm.manager import LLMManager
from shared.llm.models import LLMProvider
from shared.llm.providers import Providers
from shared.logger import get_logger
from shared.models.enums import OpportunityField, OpportunitySource
from shared.models.opportunity import Opportunity

logger = get_logger(__name__)

# Target AI search queries on Devpost
DEFAULT_DEVPOST_QUERIES = [
    "artificial intelligence",
    "machine learning",
    "data science",
]

# Fields we ask the LLM to generate selectors for (card-level extraction)
_TARGET_FIELDS: list[str] = [
    OpportunityField.TITLE,
    OpportunityField.DESCRIPTION,
    OpportunityField.IMAGE_URL,
    OpportunityField.SOURCE_URL,
    OpportunityField.TAGS,
    OpportunityField.REGISTRATION_FEE,
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
        search_queries: list[str] | None = None,
    ) -> None:
        """Initialize DevpostScraper.

        Args:
            options: Browser launch options.
            provider: LLM provider for selector generation.
            search_queries: List of search keywords to scrape on Devpost.
        """
        super().__init__(options)
        self._provider = provider
        self._model = Providers.default_model(provider)
        self._search_queries = search_queries or DEFAULT_DEVPOST_QUERIES
        self._llm_manager = LLMManager(LiteLLMClient())
        self._profile_manager = DevpostProfileManager()
        self._opportunity_parser = OpportunityParser()

    def _build_target_url(self, query: str, page_num: int = 1) -> str:
        """Construct search listing URL for Devpost."""
        formatted_query = query.replace(" ", "+")
        url = f"https://devpost.com/hackathons?search={formatted_query}&challenge_type[]=online"
        if page_num > 1:
            url += f"&page={page_num}"
        return url

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
            for query in self._search_queries:
                for page_num in range(1, _MAX_PAGES + 1):
                    target_url = self._build_target_url(query, page_num)
                    logger.info("Scraping Devpost query: '%s' (page %d, url=%s)", query, page_num, target_url)

                    await self.goto(target_url, wait_until="domcontentloaded")
                    await asyncio.sleep(2)
                    await self._wait_for_cards()

                    if profile is None:
                        profile = await self._get_or_generate_profile()

                    selector_parser = SelectorParser(profile)
                    cards = await self._locate_cards()
                    card_count = await cards.count()

                    logger.info("Found %d opportunity cards on Devpost page %d.", card_count, page_num)
                    if card_count == 0:
                        break

                    for i in range(card_count):
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
                            raw_data.setdefault("organizer", {"name": "Devpost"})
                            raw_data.setdefault("location", {"type": "online"})
                            raw_data.setdefault("timeline", {})

                            opportunity = self._opportunity_parser.parse(raw_data)
                            opportunities.append(opportunity)
                            seen_urls.add(source_url)
                            logger.debug("Parsed Devpost opportunity: %s", opportunity.title)

                        except Exception:
                            logger.warning(
                                "Failed to parse card %d on Devpost query '%s' page %d — skipping.",
                                i,
                                query,
                                page_num,
                                exc_info=True,
                            )

        finally:
            await self.stop()

        logger.info(
            "Devpost scrape complete: %d unique AI opportunities collected across %d queries.",
            len(opportunities),
            len(self._search_queries),
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
