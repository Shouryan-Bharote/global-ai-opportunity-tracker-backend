import asyncio

from scraper.core.browser import BrowserManager
from scraper.core.browser.models import BrowserLaunchOptions
from shared.logger import logger


async def main() -> None:
    options = BrowserLaunchOptions(
    headless=False,
    slow_mo=500,
    )

    browser = BrowserManager(options)

    try:
        await browser.start()

        page = await browser.new_page()

        logger.info("Navigating to Example.com...")

        await page.goto("https://unstop.com")

        title = await page.title()

        logger.info(f"Page title: {title}")

    finally:
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())