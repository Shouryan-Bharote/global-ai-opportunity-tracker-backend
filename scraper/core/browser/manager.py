from patchright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
)

from scraper.core.browser.factory import BrowserFactory
from scraper.core.browser.models import BrowserLaunchOptions
from scraper.core.exceptions import BrowserError
from shared.logger import logger


class BrowserManager:
    """
    Manages the Patchright browser lifecycle.
    """

    def __init__(
        self,
        options: BrowserLaunchOptions | None = None,
    ) -> None:
        """
        Initialize the BrowserManager.

        Args:
            options: Browser launch configuration.
        """

        self._options = options or BrowserLaunchOptions()

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

        self._playwright = await BrowserFactory.start_playwright()

        self._browser = await BrowserFactory.launch_browser(
            self._playwright,
            self._options,
        )

        self._context = await BrowserFactory.create_context(
            self._browser,
            self._options,
        )

        logger.info("Browser started successfully.")

    async def new_page(self) -> Page:
        """
        Create a new page from the default browser context.

        Raises:
            BrowserError: If the browser has not been started.
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

        if self._context is not None:
            await self._context.close()

        if self._browser is not None:
            await self._browser.close()

        if self._playwright is not None:
            await self._playwright.stop()

        self._context = None
        self._browser = None
        self._playwright = None

        logger.info("Browser closed successfully.")

    @property
    def browser(self) -> Browser:
        """
        Return the active browser instance.

        Raises:
            BrowserError: If the browser has not been started.
        """

        if self._browser is None:
            raise BrowserError("Browser has not been started.")

        return self._browser

    @property
    def context(self) -> BrowserContext:
        """
        Return the active browser context.

        Raises:
            BrowserError: If the browser has not been started.
        """

        if self._context is None:
            raise BrowserError("Browser has not been started.")

        return self._context

    def is_running(self) -> bool:
        """
        Returns True if the browser is currently running.
        """

        return self._browser is not None