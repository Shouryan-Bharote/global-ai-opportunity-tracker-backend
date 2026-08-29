# Development Status

## Last Updated: 2026-08-17

## Recent Changes

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
