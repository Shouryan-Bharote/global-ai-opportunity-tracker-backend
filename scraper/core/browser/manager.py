class BrowserManager:
    def __init__(self):
        self._playwright = None
        self._browser = None
        self._context = None

    async def start(self) -> None:
        ...

    async def close(self) -> None:
        ...

    async def new_page(self):
        ...

    def is_running(self) -> bool:
        ...