from abc import ABC, abstractmethod

from patchright.async_api import Page

from scraper.core.browser import BrowserManager
from scraper.core.browser.models import BrowserLaunchOptions
from scraper.core.exceptions import BrowserError
from shared.logger import logger


class BaseScraper(ABC):
    """
    Abstract base class defining the contract and lifecycle for scrapers.
    """

    def __init__(
        self,
        options: BrowserLaunchOptions | None = None,
    ) -> None:
        """
        Initialize the scraper.

        Args:
            options: Configuration options for launching the browser.
        """

        self._browser_manager = BrowserManager(options)
        self._page: Page | None = None

    @property
    def page(self) -> Page:
        """
        Access the current Patchright page.

        Returns:
            The active Patchright page.

        Raises:
            BrowserError: If the page has not been initialized.
        """

        if self._page is None:
            raise BrowserError("Browser page has not been initialized.")

        return self._page

    @property
    def browser_manager(self) -> BrowserManager:
        """
        Access the browser lifecycle manager.

        Returns:
            The browser manager instance.
        """

        return self._browser_manager

    async def start(self) -> None:
        """
        Start the browser and create a new page.
        """

        logger.debug("Starting scraper.")

        await self._browser_manager.start()
        self._page = await self._browser_manager.new_page()

        logger.debug("Scraper started successfully.")

    async def stop(self) -> None:
        """
        Close browser resources.
        """

        logger.debug("Stopping scraper.")

        self._page = None
        await self._browser_manager.close()

        logger.debug("Scraper stopped successfully.")

    async def goto(
        self,
        url: str,
        *,
        wait_until: str | None = None,
    ) -> None:
        """
        Navigate to the given URL.

        Args:
            url: The target URL.
            wait_until: Navigation completion event.
        """

        logger.debug(f"Navigating to {url}")

        kwargs = {}

        if wait_until is not None:
            kwargs["wait_until"] = wait_until

        await self.page.goto(url, **kwargs)

    @abstractmethod
    async def scrape(self):
        """
        Execute website-specific scraping logic.
        """
        raise NotImplementedError

    async def __aenter__(self) -> "BaseScraper":
        """
        Enter the asynchronous context manager.

        Returns:
            The scraper instance.
        """

        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        """
        Exit the asynchronous context manager.
        """

        await self.stop()