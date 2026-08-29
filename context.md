# Project Context: Global AI Opportunity Tracker Backend

## Current Phase: Phase 4 (Website Scrapers)
We are currently starting the implementation of **Phase 4: Website Scrapers**.
The goal of this phase is to build the specific website scrapers (Unstop, Hack2Skill, Devpost, Kaggle) that inherit from `BaseScraper` and implement the extraction logic for each platform.

## Technology Stack & Guidelines
- **Language**: Python 3.13+
- **Browser Automation**: Patchright (async API)
- **LLM Orchestration**: LiteLLM (future phases)
- **Development Tooling**: Poetry, pytest, Pydantic (v2+)
- **Architecture Principle**: Downward-only dependencies, composition over inheritance, and single responsibility principle.

## Status Tracker

- [x] **Phase 0: Research and Architecture**
- [x] **Phase 1: Foundation**
- [x] **Phase 2: Browser Engine Core**
- [x] **Phase 3: Scraper Framework**
- [x] **Phase 4: Website Scrapers** (Devpost & Unstop operational)
- [x] **Phase 5: LLM Pipeline** (Groq primary + Gemini fallback, 503 exponential backoff)
- [x] **Phase 6: Exporters** (JSON file outputs in `scraper/data/outputs/`)
- [ ] **Phase 7: Database** (Current focus — SQLModel persistence layer)
- [ ] **Phase 8: Scheduler**
- [ ] **Phase 9: FastAPI Backend**
- [ ] **Phase 10: Deployment**

## Important Design Decisions & Constraints
1. **Patchright Only**: Do not use Playwright; use Patchright instead.
2. **Encapsulation**: `BaseScraper` manages `BrowserManager` but does not expose a direct browser property. Concrete classes must only interact with `self.page` and `self.browser_manager`.
3. **No Speculative Complexity**: Retries, pagination, rate limiting, and screenshots are deferred until subsequent phases.
4. **Context Integrity**: Verify existing files before suggesting modifications.
