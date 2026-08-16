"""
Unstop Scraper End-to-End Runner.

Run with:
    poetry run python -m examples.scraper.run_unstop

On first run:
  - Opens a browser (headless by default).
  - Navigates to unstop.com/hackathons.
  - Sends the page HTML to Groq LLM to generate CSS/XPath selectors.
  - Saves the selector profile to scraper/scrapers/unstop/profiles/hackathon_listing.json
  - Extracts and prints each parsed Opportunity.

On subsequent runs:
  - Loads the cached selector profile from disk (no LLM cost).
  - Extracts and prints opportunities directly.

To force a fresh profile, delete the JSON file or call:
    from scraper.scrapers.unstop import UnstopProfileManager
    UnstopProfileManager().invalidate()
"""

import asyncio
import json
from pathlib import Path

from scraper.core.browser.models import BrowserLaunchOptions
from scraper.scrapers.unstop import UnstopScraper
from shared.llm.models import LLMProvider


async def main() -> None:
    options = BrowserLaunchOptions(headless=False)

    print("=" * 60)
    print("  Unstop Scraper — End-to-End Test")
    print("=" * 60)
    print()

    async with UnstopScraper(options=options, provider=LLMProvider.GROQ) as scraper:
        opportunities = await scraper.scrape()

    print(f"\nTotal opportunities parsed: {len(opportunities)}\n")

    for i, opp in enumerate(opportunities, start=1):
        print(f"[{i}] {opp.title}")
        print(f"     Type   : {opp.type}")
        print(f"     Status : {opp.status}")
        print(f"     Source : {opp.source_url}")
        print(f"     Tags   : {', '.join(opp.tags) if opp.tags else 'N/A'}")
        print()

    if opportunities:
        output_dir = Path("scraper/data/outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "unstop_opportunities.json"

        data = [json.loads(opp.model_dump_json()) for opp in opportunities]
        output_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

        print(f"Saved {len(opportunities)} opportunities to {output_file.resolve()}\n")

        print("--- First opportunity sample ---")
        print(json.dumps(data[0], indent=2))


if __name__ == "__main__":
    asyncio.run(main())
