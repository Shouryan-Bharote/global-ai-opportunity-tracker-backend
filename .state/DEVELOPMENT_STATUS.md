# Development Status

## Last Updated: 2026-10-18

## Recent Changes

### 2026-10-18 — Phase 10: Production Deployment & Containerization
- **PostgreSQL Production Compatibility**:
  - Added conditional logic in [session.py](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/shared/database/session.py) so SQLite-only connect arguments (`check_same_thread`) are automatically omitted when connecting to PostgreSQL or other engines.
  - Added `psycopg2-binary` dependency in [pyproject.toml](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/pyproject.toml).
  - Added URL normalization in [settings.py](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/shared/config/settings.py) to automatically translate `postgres://` to `postgresql+psycopg2://` for Cloud PaaS providers (Render, Railway, Fly.io).
- **Docker Containerization**:
  - Authored production [Dockerfile](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/Dockerfile) with Python 3.13-slim, system dependencies, Poetry, Patchright stealth Chromium browser, and `/health` probe.
  - Authored [.dockerignore](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/.dockerignore) to exclude build caches, test artifacts, and local databases.
- **Multi-Container Docker Compose**:
  - Created [docker-compose.yml](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/docker-compose.yml) orchestrating `trackit-api` (FastAPI), `trackit-scheduler` (continuous scraper daemon), and `trackit-postgres` (PostgreSQL 16) with volume persistence.
  - Enhanced [job_scheduler.py](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/scraper/core/scheduler/job_scheduler.py) main entrypoint to support continuous daemon execution via `--scheduler` flag or `RUN_MODE=scheduler` environment variable.
  - Fixed APScheduler `AsyncIOScheduler` event loop attachment by wrapping `start_scheduler_async` in `asyncio.run()`, preventing `RuntimeError: no running event loop` on Python 3.12+.
- **Environment Configuration**:
  - Created [.env.docker](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/.env.docker) template for single-command Docker deployment.
  - Updated [.env.example](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/.env.example) with production PostgreSQL settings and cron scheduler configs.
- **CI/CD Pipeline**:
  - Implemented [.github/workflows/ci.yml](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/.github/workflows/ci.yml) for automated pytest execution and Docker build verification on push and PR.
- **Documentation**:
  - Authored comprehensive [docs/deployment.md](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/docs/deployment.md) covering local Docker Compose, VPS + Nginx reverse proxy with SSL, Cloud PaaS, and PostgreSQL backup/restore.
  - Updated [docs/phases/PHASE_10.md](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/docs/phases/PHASE_10.md) and [docs/phases/PHASE_07.md](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/docs/phases/PHASE_07.md) to completed.


### 2026-10-13 — Physical Device Networking Fix
- **Root Cause Identified**: App was running on a real Android phone (device `10BG2C1L17008CT`), not an emulator. The old `env_config.dart` remapped `localhost → 10.0.2.2` for **all** Android devices, breaking the connection on physical devices where `10.0.2.2` doesn't resolve to the PC.
- **Fixed [`env_config.dart`](file:///d:/My Projects/Major Project/global-ai-opportunity-tracker-app/lib/core/config/env_config.dart)**: Now uses `device_info_plus` to detect physical vs emulator. Physical devices keep `localhost` (tunneled via `adb reverse`); emulators remap to `10.0.2.2`.
- **Added `device_info_plus 13.3.0`** dependency for device type detection.
- **Set up `adb reverse tcp:8000 tcp:8000`**: Tunnels phone's `localhost:8000` → PC's `localhost:8000`.
- **Verified**: Dio logs confirm `GET http://localhost:8000/api/v1/opportunities → 200 OK` on the physical device.


- **Diagnosed and resolved** root causes for "no data in frontend":
  1. **SQLAlchemy Session Expiration**: Added `expire_on_commit=False` in [shared/database/session.py](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/shared/database/session.py) to prevent `DetachedInstanceError` and empty dictionaries `[{}, {}]` when serializing `OpportunityDB` instances.
  2. **JSON Column Types**: Added `Any, Dict` imports and updated JSON column annotations in [shared/database/models.py](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/shared/database/models.py) to eliminate Pydantic serialization errors.
  3. **Dio Relative URL Resolution**: Fixed leading slash in [http_event_repository.dart](file:///d:/My%20Projects/Major%20Project/global-ai-opportunity-tracker-app/lib/features/events/repositories/http_event_repository.dart) by switching `'/opportunities'` to `'opportunities'` and ensuring trailing slash on base URL, preventing Dio from discarding the `/api/v1` path prefix.
  4. **Android Emulator IP Translation**: Updated [env_config.dart](file:///d:/My%20Projects/Major%20Project/global-ai-opportunity-tracker-app/lib/core/config/env_config.dart) to automatically map `localhost` to `10.0.2.2` when running on Android emulators.
  5. **Frontend Filter Fallback**: Updated [home_provider.dart](file:///d:/My%20Projects/Major%20Project/global-ai-opportunity-tracker-app/lib/features/home/providers/home_provider.dart) so "Today's Events" includes ongoing events and falls back to all opportunities when none start strictly today; relaxed location filter so online events aren't discarded when device location is on; made category tags case-insensitive.
- **Verified**: `GET /api/v1/opportunities` returns status 200 with 20 items populated, and `flutter analyze` passes with 0 issues.

### 2026-10-13 — Phase 9: FastAPI Backend REST API
- **Implemented** complete FastAPI backend application in [api/main.py](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/api/main.py) with lifespan schema creation and CORS support.
- **Created** [api/routers/opportunities.py](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/api/routers/opportunities.py) exposing:
  - `GET /api/v1/opportunities`: paginated filtering by keyword `q`, `type`, `status`, `source`, `tag`, `is_remote_friendly`, `is_featured`.
  - `GET /api/v1/opportunities/stats`: summary distribution across platforms, types, and statuses.
  - `GET /api/v1/opportunities/{id}`: opportunity detail query.
- **Created** [api/routers/jobs.py](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/api/routers/jobs.py) exposing:
  - `GET /api/v1/jobs`: paginated scraper run execution history.
  - `POST /api/v1/jobs/trigger`: on-demand background scraper job dispatch.
- **Created** [api/schemas.py](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/api/schemas.py) providing `PaginatedResponse[T]`, `StatsResponse`, and `HealthResponse`.
- **Created** `tests/api/test_api.py` with 5 integration tests covering health, search, stats, 404 handling, and job listing (12/12 test suite passing).

### 2026-10-13 — Scheduler & Persistence Layer Hardening
- **Fixed** database table initialization by introducing `init_db()` in [session.py](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/shared/database/session.py) invoked on scraper start.
- **Fixed** `OpportunityRepository` serialization: resolved `dict.json()` AttributeError, implemented Pydantic v2 `model_dump()`, and stored sub-models into JSON columns correctly.
- **Fixed** SQLModel / SQLAlchemy `ValueError: Datetime values must have timezone information` by switching all `datetime.utcnow()` instances to timezone-aware `datetime.now(timezone.utc)`.
- **Fixed** Unstop card parsing title selector failures: updated [hackathon_listing.json](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/scraper/scrapers/unstop/profiles/hackathon_listing.json) to extract titles from both `<h3>` and `<h2>` elements (`h2`, `h3`, `.double-wrap`, `.cptn h2/h3`).
- **Verified** Devpost scraper (27/27 parsed and stored) and Unstop scraper (19 opportunities parsed on page 1 without title validation failures).

### 2026-10-12 — Database Persistence Layer & Scheduler Implementation
- **Implemented** SQLModel database persistence layer with UPSERT deduplication in `shared/database/`.
- **Created** `Opportunity` SQLModel model matching `shared/models/opportunity.py`.
- **Built** database session manager supporting SQLite (dev) and PostgreSQL (prod) via `shared/database/session.py`.
- **Developed** repository layer with `upsert_opportunity()` method in `shared/database/repository.py`.
- **Updated** Devpost and Unstop scrapers to use repository instead of writing JSON files.
- **Created** scraper orchestrator and scheduler in `scraper/core/scheduler/job_scheduler.py` using APScheduler.
- **Configured** default schedule for nightly runs at 2:00 AM.
- **Added** execution statistics logging (opportunities scraped, inserted, updated, errors).
- **Ensured** clean browser session handling and graceful shutdown.

### 2026-10-12 — Universal LLM Provider System
- **Added** `LLMProvider.NVIDIA` and `LLMProvider.CUSTOM` to the `LLMProvider` enum in `shared/llm/models.py`.
- **Rewrote** `shared/llm/providers.py`: replaced hardcoded static `_CONFIGS` dict with a dynamic `_build_registry()` factory that reads all provider configs directly from `settings`. Registry is lazily built and can be force-reloaded via `Providers._reload()`.
- **Added** `Providers.resolve_chain()`: returns an ordered list of providers that have API keys configured. Respects the new `LLM_PROVIDER_CHAIN` env var (comma-separated) for explicit ordering; falls back to auto-detection (Groq → OpenRouter → NVIDIA → Gemini → Custom).
- **Updated** `shared/llm/manager.py`: replaced the hardcoded two-step Groq→Gemini fallback with a dynamic loop over `Providers.resolve_chain()`. All N providers are tried in order; raises `LLMError` only after all are exhausted.
- **Updated** `shared/llm/client.py`: passes `api_base=provider_config.base_url` to `acompletion()`, enabling NVIDIA NIM and custom base-URL endpoints.
- **Updated** `shared/config/settings.py`: added `nvidia_api_key`, `nvidia_base_url`, `nvidia_default_model`, `custom_api_key`, `custom_base_url`, `custom_provider_name`, `custom_default_model`, and `llm_provider_chain` settings.
- **Updated** `.env.example`: documents all new provider env vars.

### 2026-08-17 — LLM Infrastructure Hardening & Scraper Bug Fixes
- **Switched** default LLM provider for both scrapers: **Groq = primary**, **Gemini = automatic fallback** (implemented in `LLMManager.generate_selector_profile()`).
- **Updated** Groq model to `groq/groq/compound-mini` (non-reasoning, no `<think>` tags).
- **Updated** Gemini model to `gemini/gemini-3.6-flash` (latest available per Google API).
- **Added** `_strip_thinking_tags()` to `ResponseParser` — strips `<think>...</think>` blocks from Qwen/DeepSeek-R1 style reasoning models.
- **Added** `_extract_markdown_code_block()` to `ResponseParser` — prioritises `\`\`\`json` code blocks over bare text to avoid misidentifying XPath/HTML fragments as JSON.
- **Added** 503 retry with exponential backoff (2s/4s/8s, max 3 attempts) to `LiteLLMClient` via `ServiceUnavailableError` catch.
- **Manually authored** `scraper/scrapers/devpost/profiles/devpost_selectors.json` — bypasses LLM dependency entirely for Devpost, based on confirmed DOM inspection.
- **Fixed** `DevpostScraper`: 
  - Missing `SelectorProfile` import.
  - Protocol-relative image URL normalization (`//cdn…` → `https://cdn…`).
  - Added warning when no cards found.
  - **Replaced** URL-based pagination (`?page=N`) with **Infinite Scrolling** via DOM manipulation. Devpost ignores the page parameter and uses infinite scrolling, which previously caused the scraper to only extract the first 9 cards repeatedly. Now correctly extracts all dynamically loaded cards.
- **Fixed** `UnstopScraper` (5 bugs):
  - Missing `SelectorProfile` import.
  - `scrape()` was calling `goto()` before `start()` — browser was uninitialised (crash on first run outside `async with`).
  - `fields=[f.value for f in _TARGET_FIELDS]` — `_TARGET_FIELDS` was typed as `list[str]`, calling `.value` on strings → AttributeError.
  - `event_type.rstrip("s")` → `"quizzes"` became `"quizze"` — replaced with `_EVENT_TYPE_MAP` lookup dict.
  - Added return type annotation on `_get_or_generate_profile`.
  - Protocol-relative image URL normalization added.
- **Created** comprehensive project `README.md` document covering architecture, setup, environment configuration, scraper runners, testing, and phase roadmaps.

## Recent Changes

### 2026-08-16 — Unstop Concrete Scraper Implementation (Phase 4D Baseline)
- **Implemented** `UnstopScraper` in `scraper/scrapers/unstop/scraper.py` extending `BaseScraper`.
- **Implemented** `UnstopProfileManager` in `scraper/scrapers/unstop/profile_manager.py` for JSON profile caching.
- **Implemented** popup modal auto-dismissal (`_dismiss_login_modal()`) for Unstop's login overlays.
- **Fixed** `SelectorEngine` timeouts (reduced default from 30s to 3s per locator query) to prevent long hangs on missing optional fields.
- **Fixed** `OpportunityParser._postprocess()` bug.
- **Fixed** Gemini model names (`gemini-3.5-flash` / `gemini-3.1-pro`) and `GEMINI_API_KEY` configuration.
### 2026-08-16 — Unstop Multi-Category AI Scraper & Pagination Fixes (Phase 4D Baseline)
- **Implemented** multi-category AI/ML filtering (`artificial-intelligence-machine-learning`, `data-analytics`, `data-science`).
- **Expanded** event type iteration across `hackathons`, `competitions`, `quizzes`, and `conferences`.
- **Implemented** JavaScript DOM modal overlay purging in `_dismiss_login_modal()` to eliminate pointer event interception during pagination.
- **Implemented** `BrowserManager.close()` exception safeguards for clean manual window shutdowns.
### 2026-08-16 — Devpost Concrete Scraper Implementation & Profile Folder Relocation (Phase 4D Milestone)
- **Relocated** all `SelectorProfile` cached JSON files into their respective scraper folders (`scraper/scrapers/unstop/profiles/` and `scraper/scrapers/devpost/profiles/`).
- **Implemented** `DevpostScraper` in `scraper/scrapers/devpost/scraper.py` extending `BaseScraper`.
- **Implemented** `DevpostProfileManager` in `scraper/scrapers/devpost/profile_manager.py` storing profiles in local `profiles/` subdirectory.
- **Scraped** and validated **27 global AI hackathons** from Devpost saved to `scraper/data/outputs/devpost_opportunities.json`.
- **Updated** Graphify knowledge graph (770 nodes, 1255 edges).

## Build Status
- ✅ All imports clean
- ✅ No circular dependencies
- ✅ Unstop multi-category AI scraper live validation passing (174/174 parsed)
- ✅ Devpost AI scraper live validation passing (27/27 parsed)
- ✅ Graphify knowledge graph current (769 nodes, 1254 edges)

## Next Actions
See `.state/TASK_QUEUE.md`
