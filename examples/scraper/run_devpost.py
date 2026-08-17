"""
Devpost Scraper End-to-End Runner.

Run with:
    poetry run python -m examples.scraper.run_devpost
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

from scraper.core.browser.models import BrowserLaunchOptions
from scraper.scrapers.devpost import DevpostScraper
from shared.logger import logger

_OUTPUT_PATH = Path("scraper/data/outputs/devpost_opportunities.json")


async def main() -> None:
    options = BrowserLaunchOptions(headless=False)
    scraper = DevpostScraper(options=options)

    print("=" * 60)
    print("  Devpost AI Scraper — End-to-End Test")
    print("=" * 60)

    try:
        opportunities = await scraper.scrape()

        print(f"\nSuccessfully scraped {len(opportunities)} opportunities from Devpost:\n")
        for idx, opp in enumerate(opportunities, 1):
            print(f"[{idx}] {opp.title}")
            print(f"     Type   : {opp.type}")
            print(f"     Status : {opp.status}")
            print(f"     Source : {opp.source_url}")
            print(f"     Tags   : {', '.join(opp.tags)}")
            print()

        # Save to JSON
        _OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        dump_data = [opp.model_dump(mode="json") for opp in opportunities]
        _OUTPUT_PATH.write_text(json.dumps(dump_data, indent=2), encoding="utf-8")
        print(f"Saved {len(opportunities)} opportunities to {_OUTPUT_PATH.resolve()}")

        if opportunities:
            print("\n--- First opportunity sample ---")
            print(json.dumps(opportunities[0].model_dump(mode="json"), indent=2))

    except Exception:
        logger.error("Devpost scraper failed.", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
