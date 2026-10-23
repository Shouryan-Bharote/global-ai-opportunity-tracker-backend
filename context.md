# Project Context: Global AI Opportunity Tracker Backend

## Current Phase: Phase 10: Deployment (Completed)
The TrackIT backend is fully containerized with Docker, multi-container Docker Compose (FastAPI, PostgreSQL 16, and Scheduler Daemon), CI/CD pipelines, and ready for production deployment.

## Technology Stack & Guidelines
- **Language**: Python 3.13+
- **Browser Automation**: Patchright (async stealth Chromium)
- **API Framework**: FastAPI & Uvicorn
- **Database**: SQLModel / SQLAlchemy (SQLite for dev, PostgreSQL with psycopg2 for prod)
- **LLM Orchestration**: LiteLLM (Groq primary + Gemini fallback)
- **Scheduler**: APScheduler with concurrency and retry tracking
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
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
- [x] **Phase 7: Database** (SQLModel persistence layer with UPSERT deduplication)
- [x] **Phase 8: Scheduler** (APScheduler orchestrator & job run tracking)
- [x] **Phase 9: FastAPI Backend** (REST API with filtering, pagination, stats, docs)
- [x] **Phase 10: Deployment** (Dockerfile, docker-compose, CI/CD, deployment guide)

## Important Design Decisions & Constraints
1. **Patchright Only**: Do not use Playwright; use Patchright instead.
2. **Encapsulation**: `BaseScraper` manages `BrowserManager` but does not expose a direct browser property. Concrete classes must only interact with `self.page` and `self.browser_manager`.
3. **No Speculative Complexity**: Retries, pagination, rate limiting, and screenshots are deferred until subsequent phases.
4. **Context Integrity**: Verify existing files before suggesting modifications.
