# Phase 3: Scraper Framework

## Status: ✅ COMPLETED

## Objective
Build the abstract base scraper (`BaseScraper`) that orchestrates the browser and page lifecycle and defines the contract for all website-specific scrapers.

## Deliverables
- `BaseScraper` abstract base class with async context manager support
- Integration with `BrowserManager` for lifecycle management
- Abstract `scrape()` contract for concrete implementations
- High-level `goto()` navigation
- Unit tests for the base scraper

## Key Files
| File | Purpose |
|------|---------|
| `scraper/scrapers/base/base_scraper.py` | Abstract base scraper class |
| `scraper/scrapers/base/__init__.py` | Public exports |
| `tests/scraper/scrapers/test_base_scraper.py` | Unit tests |

## API Contract
```python
class BaseScraper(ABC):
    @property
    def page(self) -> Page: ...
    
    @property
    def browser_manager(self) -> BrowserManager: ...
    
    async def start(self) -> None: ...
    async def stop(self) -> None: ...
    async def goto(self, url: str) -> None: ...
    
    @abstractmethod
    async def scrape(self): ...
```

## Design Constraints
- `BaseScraper` manages `BrowserManager` but does **not** expose a direct browser property.
- Concrete classes must only interact with `self.page` and `self.browser_manager`.
- No retries, pagination, rate limiting, or screenshots in this phase.
- No redundant logging — `BrowserManager` already logs lifecycle events.
