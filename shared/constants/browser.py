from enum import StrEnum


class BrowserEngine(StrEnum):
    CHROMIUM = "chromium"


class Browser:
    DEFAULT_TIMEOUT = 30_000      # milliseconds
    NAVIGATION_TIMEOUT = 60_000
    PAGE_LOAD_DELAY = 2           # seconds

    DEFAULT_VIEWPORT = {
        "width": 1920,
        "height": 1080,
    }

    DEFAULT_LOCALE = "en-US"