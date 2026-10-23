# Decisions Log

## Format
Each decision follows this format:
- **Date**: When the decision was made
- **Decision**: What was decided
- **Rationale**: Why this choice was made
- **Alternatives**: What was considered but rejected

---

## Decision 001 — Patchright over Playwright
- **Date**: Phase 0
- **Decision**: Use Patchright instead of Playwright for browser automation.
- **Rationale**: Enhanced stealth and anti-detection capabilities.
- **Alternatives**: Playwright (rejected — lacks stealth features).

## Decision 002 — LiteLLM for LLM Orchestration
- **Date**: Phase 0
- **Decision**: Use LiteLLM as the LLM provider abstraction layer.
- **Rationale**: Provider-agnostic API supporting Gemini, Groq, OpenRouter without vendor lock-in.
- **Alternatives**: Direct provider SDKs (rejected — would require separate integrations per provider).

## Decision 003 — Composition over Inheritance
- **Date**: Phase 0
- **Decision**: Prefer composition over deep inheritance hierarchies.
- **Rationale**: More flexible, testable, and avoids tight coupling. Example: `BaseScraper` owns a `BrowserManager` rather than inheriting browser capabilities.
- **Alternatives**: Inheritance-based design (rejected — creates rigid hierarchies).

## Decision 004 — OpportunityField Enum
- **Date**: Phase 4B (2026-08-15)
- **Decision**: Change `ExtractionField.name` from `str` to `OpportunityField(StrEnum)`.
- **Rationale**: Prevents LLM from hallucinating invalid field names. Pydantic rejects invalid values at parse time.
- **Alternatives**: Keep as `str` with runtime validation (rejected — enum is more robust and self-documenting).

## Decision 005 — SelectorEngine Dispatch on ExtractionType
- **Date**: Phase 4C (2026-08-15)
- **Decision**: SelectorEngine dispatches on `ExtractionType` (text/html/attribute/list/table/json), not `SelectorType` (css/xpath).
- **Rationale**: `SelectorType` determines how to locate elements; `ExtractionType` determines what data to extract. These are orthogonal concerns. The locator handles css vs xpath; the handler handles what to extract.
- **Alternatives**: Dispatch on SelectorType (rejected — conflates locator strategy with extraction strategy).

## Decision 006 — Primary/Fallback LLM Manager
- **Date**: Phase 4D (2026-08-17)
- **Decision**: Configure `LLMManager` with primary provider (`groq/groq/compound-mini`) and automatic fallback (`gemini/gemini-3.6-flash`).
- **Rationale**: Groq provides ultra-fast inference and generous free tier rate limits. Gemini serves as a reliable fallback during provider outages or model availability shifts.
- **Alternatives**: Single provider without fallback (rejected — prone to scraping pipeline halts when rate-limited).

## Decision 007 — Devpost Infinite Scroll via Keyboard Press
- **Date**: Phase 4D (2026-08-17)
- **Decision**: Use `page.keyboard.press("End")` instead of `?page=N` URL parameters or instantaneous `window.scrollTo` calls in `DevpostScraper`.
- **Rationale**: Devpost ignores page URL parameters for hackathon listings and uses client-side infinite scroll. Smooth keyboard events reliably trigger the DOM's IntersectionObserver to load new cards incrementally.
- **Alternatives**: `window.scrollTo(0, document.body.scrollHeight)` (rejected — jumps straight to footer without triggering intersection events past page 2).

## Decision 008 — Session Persistence and Relative API Client Resolution
- **Date**: 2026-10-13
- **Decision**: Configure `expire_on_commit=False` on `Session` instantiation in [session.py](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/shared/database/session.py) and strip leading slashes from sub-resource paths in Flutter `HttpEventRepository`.
- **Rationale**: SQLAlchemy defaults to expiring all object attributes on `commit()`. When the session closes, detached instances accessed outside the context manager or serialized by Pydantic / FastAPI fail with `DetachedInstanceError` or serialize to empty dicts `{}`. In Dart Dio, relative paths with a leading slash (`'/opportunities'`) override the baseUrl path prefix (`/api/v1`) per RFC 3986 URI resolution; removing the leading slash preserves the `/api/v1/opportunities` endpoint.
- **Alternatives**: Keeping sessions open indefinitely (rejected — leaks database connections). Using manual model conversion before session commit (rejected — cumbersome across multiple repository methods).

## Decision 009 — Decoupled Multi-Container Deployment & PostgreSQL Normalization
- **Date**: Phase 10 (2026-10-18)
- **Decision**: Decouple the backend into `trackit-api` (FastAPI web server), `trackit-scheduler` (APScheduler scraper daemon), and `trackit-postgres` (PostgreSQL 16) with automated health probes and conditional `check_same_thread` filtering.
- **Rationale**: Running scrapers with stealth browser automation inside the web server process risks starving HTTP workers of CPU/memory and causing request latency spikes. Decoupling the scheduler into a background container preserves API responsiveness. Normalizing `postgres://` to `postgresql+psycopg2://` ensures instant compatibility with managed databases on cloud PaaS (Render, Railway, Fly.io).
- **Alternatives**: Monolithic single-container running both uvicorn and scheduler in the same event loop (rejected — browser automation CPU spikes can degrade API response times).

