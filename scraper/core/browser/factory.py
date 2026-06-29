from patchright.async_api import (
    Browser,
    BrowserContext,
    Playwright,
    async_playwright,
)

from scraper.core.browser.models import BrowserLaunchOptions


class BrowserFactory:
    """
    Factory responsible for creating Patchright browser objects.
    """

    def __new__(cls):
        raise TypeError("BrowserFactory cannot be instantiated.")

    @staticmethod
    async def start_playwright() -> Playwright:
        """
        Start the Patchright engine.
        """
        return await async_playwright().start()

    @staticmethod
    async def launch_browser(
        playwright: Playwright,
        options: BrowserLaunchOptions,
    ) -> Browser:
        """
        Launch a Chromium browser instance.
        """

        return await playwright.chromium.launch(
            headless=options.headless,
            slow_mo=options.slow_mo,
            channel=options.channel,
        )

    @staticmethod
    async def create_context(
        browser: Browser,
        options: BrowserLaunchOptions,
    ) -> BrowserContext:
        """
        Create the default browser context.
        """

        return await browser.new_context(
            viewport=options.viewport.to_patchright(),
            locale=options.locale,
            ignore_https_errors=options.ignore_https_errors,
        )