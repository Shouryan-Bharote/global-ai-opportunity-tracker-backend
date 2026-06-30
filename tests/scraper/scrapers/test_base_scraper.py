import asyncio
import pytest
from unittest.mock import AsyncMock

from patchright.async_api import Page
from scraper.core.browser.models import BrowserLaunchOptions
from scraper.core.exceptions import BrowserError
from scraper.scrapers.base import BaseScraper


class ConcreteScraper(BaseScraper):
    """Concrete subclass of BaseScraper for testing."""

    async def scrape(self) -> None:
        pass


def test_cannot_instantiate_base_scraper() -> None:
    """Verify BaseScraper is an abstract base class and cannot be instantiated."""
    with pytest.raises(TypeError):
        BaseScraper()  # type: ignore


def test_init_with_options(mocker) -> None:
    """Verify scraper instantiates BrowserManager with options."""
    mock_manager = mocker.patch("scraper.scrapers.base.base_scraper.BrowserManager")
    options = BrowserLaunchOptions(headless=False)

    scraper = ConcreteScraper(options=options)

    mock_manager.assert_called_once_with(options)
    assert scraper.browser_manager == mock_manager.return_value


def test_page_property_error_before_start() -> None:
    """Verify page property raises BrowserError before start is called."""
    scraper = ConcreteScraper()
    with pytest.raises(BrowserError) as exc_info:
        _ = scraper.page
    assert "Browser is not started or page is not initialized." in str(exc_info.value)


def test_start_lifecycle(mocker) -> None:
    """Verify start initializes browser and creates a page."""
    async def run() -> None:
        mock_manager_cls = mocker.patch("scraper.scrapers.base.base_scraper.BrowserManager")
        mock_manager = mock_manager_cls.return_value
        mock_manager.start = AsyncMock()
        mock_manager.new_page = AsyncMock()

        mock_page = mocker.MagicMock(spec=Page)
        mock_manager.new_page.return_value = mock_page

        scraper = ConcreteScraper()
        await scraper.start()

        mock_manager.start.assert_called_once()
        mock_manager.new_page.assert_called_once()
        assert scraper.page == mock_page

    asyncio.run(run())


def test_stop_lifecycle(mocker) -> None:
    """Verify stop closes page and browser resources."""
    async def run() -> None:
        mock_manager_cls = mocker.patch("scraper.scrapers.base.base_scraper.BrowserManager")
        mock_manager = mock_manager_cls.return_value
        mock_manager.start = AsyncMock()
        mock_manager.new_page = AsyncMock()
        mock_manager.close = AsyncMock()

        mock_page = mocker.MagicMock(spec=Page)
        mock_manager.new_page.return_value = mock_page

        scraper = ConcreteScraper()
        await scraper.start()

        # Verify page is accessible
        assert scraper.page == mock_page

        await scraper.stop()
        mock_manager.close.assert_called_once()

        # Page should raise exception again
        with pytest.raises(BrowserError):
            _ = scraper.page

    asyncio.run(run())


def test_goto_navigation(mocker) -> None:
    """Verify goto routes call to page.goto."""
    async def run() -> None:
        mock_manager_cls = mocker.patch("scraper.scrapers.base.base_scraper.BrowserManager")
        mock_manager = mock_manager_cls.return_value
        mock_manager.start = AsyncMock()
        mock_manager.new_page = AsyncMock()

        mock_page = mocker.MagicMock(spec=Page)
        mock_page.goto = AsyncMock()
        mock_manager.new_page.return_value = mock_page

        scraper = ConcreteScraper()
        await scraper.start()

        url = "https://unstop.com"
        await scraper.goto(url)
        mock_page.goto.assert_called_once_with(url)

    asyncio.run(run())


def test_async_context_manager(mocker) -> None:
    """Verify async context manager initializes and cleans up resources."""
    async def run() -> None:
        mock_manager_cls = mocker.patch("scraper.scrapers.base.base_scraper.BrowserManager")
        mock_manager = mock_manager_cls.return_value
        mock_manager.start = AsyncMock()
        mock_manager.new_page = AsyncMock()
        mock_manager.close = AsyncMock()

        mock_page = mocker.MagicMock(spec=Page)
        mock_manager.new_page.return_value = mock_page

        async with ConcreteScraper() as scraper:
            assert scraper.page == mock_page
            mock_manager.start.assert_called_once()
            mock_manager.new_page.assert_called_once()
            mock_manager.close.assert_not_called()

        mock_manager.close.assert_called_once()

    asyncio.run(run())
