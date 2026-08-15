# Architecture

## Overview
The Global AI Opportunity Tracker backend follows a strict **layered architecture** with downward-only dependencies. Each layer has a single responsibility and communicates through explicit contracts (Pydantic models).

## Layer Diagram
```
┌─────────────────────────────────────────────────┐
│                 Phase 9: FastAPI                │
│              (REST API exposure)                │
├─────────────────────────────────────────────────┤
│                 Phase 8: Scheduler              │
│            (Job scheduling & orchestration)      │
├─────────────────────────────────────────────────┤
│                 Phase 7: Database               │
│            (Persistence & deduplication)         │
├─────────────────────────────────────────────────┤
│                 Phase 6: Exporters              │
│            (JSON, CSV output formats)           │
├─────────────────────────────────────────────────┤
│                 Phase 5: LLM Pipeline           │
│        (Advanced LLM features & caching)        │
├─────────────────────────────────────────────────┤
│            Phase 4: Website Scrapers            │
│      (Concrete scrapers + LLM-driven parsing)   │
│                                                 │
│  ┌───────────┐  ┌──────────────┐  ┌──────────┐ │
│  │  Scrapers  │→│ LLM Pipeline │→│ Parsers  │ │
│  └───────────┘  └──────────────┘  └──────────┘ │
├─────────────────────────────────────────────────┤
│            Phase 3: Scraper Framework           │
│          (BaseScraper abstraction)              │
├─────────────────────────────────────────────────┤
│            Phase 2: Browser Engine              │
│     (BrowserFactory + BrowserManager)           │
├─────────────────────────────────────────────────┤
│              Phase 1: Foundation                │
│    (Config, Logger, Constants, Models)          │
└─────────────────────────────────────────────────┘
```

## Dependency Rules
1. **Downward only**: Upper layers depend on lower layers, never the reverse.
2. **No cross-layer imports**: Scrapers never import from Exporters or Database.
3. **Explicit contracts**: Each layer boundary uses dedicated Pydantic models.
4. **Composition over inheritance**: Classes own components, not inherit them.

## Data Flow
```
Web Page → Patchright (Browser Engine)
    → BaseScraper.scrape() (Scraper Framework)
    → LLMManager.generate_selector_profile() (LLM Pipeline)
    → SelectorParser.parse(page) (Parser Pipeline)
    → dict[str, object] (raw extracted data)
    → OpportunityParser.parse(data) (Parser Pipeline)
    → Opportunity (structured model)
    → Database (persistence)
    → FastAPI (API exposure)
```

## Module Boundaries

### `shared/` — Cross-cutting concerns
- `config/` — Application settings
- `constants/` — Domain constants
- `logger/` — Logging infrastructure
- `models/` — Domain models (Opportunity, enums, etc.)
- `llm/` — LLM client, models, selector profiles, validation
- `exceptions/` — Base exception hierarchy
- `utils/` — Shared utilities

### `scraper/` — Scraping domain
- `core/browser/` — Browser engine (factory, manager, config)
- `core/exceptions/` — Scraper-specific exceptions
- `core/manager/` — Scraper orchestration
- `core/scheduler/` — Job scheduling
- `scrapers/base/` — Abstract base scraper
- `scrapers/{platform}/` — Platform-specific scrapers
- `parsers/` — Extraction and parsing pipeline
- `exporters/` — Data export modules
- `data/` — Output storage (screenshots, exports)
