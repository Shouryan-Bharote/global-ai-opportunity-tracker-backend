from patchright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)

from scraper.core.exceptions import BrowserError
from shared.config import settings
from shared.logger import logger


class BrowserManager:
    """
    Manages the Patchright browser lifecycle.
    """

    def __init__(self) -> None:
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None

    async def start(self) -> None:
        """
        Start Patchright and launch the browser.
        
        Raises:
            BrowserError: If the browser fails to launch.
        
        """

        if self.is_running():
            logger.warning("Browser is already running.")
            return

        logger.info("Starting browser...")

        self._playwright = await async_playwright().start()

        self._browser = await self._playwright.chromium.launch(
            headless=settings.headless,
        )

        self._context = await self._browser.new_context()

        logger.info("Browser started successfully.")

    async def new_page(self) -> Page:
        """
        Create a new page from the default browser context.
        """

        if self._context is None:
            raise BrowserError("Browser has not been started.")

        logger.debug("Creating new page.")

        return await self._context.new_page()

    async def close(self) -> None:
        """
        Close all browser resources.
        """

        if not self.is_running():
            logger.warning("Browser is already closed.")
            return

        logger.info("Closing browser...")

        if self._context:
            await self._context.close()

        if self._browser:
            await self._browser.close()

        if self._playwright:
            await self._playwright.stop()

        self._context = None
        self._browser = None
        self._playwright = None

        logger.info("Browser closed successfully.")

    def is_running(self) -> bool:
        """
        Returns True if the browser is currently running.
        """

        return (
            self._playwright is not None
            and self._browser is not None
            and self._context is not None
        )