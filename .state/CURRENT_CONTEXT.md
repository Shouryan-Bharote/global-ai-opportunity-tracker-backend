# Current Context

## Project
**Global AI Opportunity Tracker** — Backend

## What This Project Does
Automates the lifecycle of AI-related professional opportunities by scraping websites, using LLMs to generate extraction selectors, parsing data into structured models, and exposing results via a REST API.

## Tech Stack
- **Language**: Python 3.13+
- **Browser Automation**: Patchright (stealth Chromium)
- **LLM Orchestration**: LiteLLM (Gemini, Groq, OpenRouter)
- **Data Validation**: Pydantic v2+
- **Package Management**: Poetry
- **Testing**: pytest

## Current Phase
**Phase 4: Website Scrapers + LLM-Driven Parsing**

## What's Been Built
- ✅ Foundation (config, logger, constants, models)
- ✅ Browser Engine (BrowserFactory, BrowserManager, Patchright integration)
- ✅ Scraper Framework (BaseScraper with async context manager)
- ✅ LLM Infrastructure (LiteLLMClient with 503 retries, LLMManager with Groq→Gemini fallback, ResponseParser)
- ✅ Selector Profile system (SelectorProfile, ExtractionField, Selector, OpportunityField)
- ✅ Parser Pipeline (SelectorEngine, SelectorParser, OpportunityParser, Normalizer)
- ✅ Concrete Scrapers (Devpost with infinite scroll & Unstop multi-category AI scraper)

## What's Next
- ⬜ Database Persistence Layer (SQLModel + SQLite / PostgreSQL storage & UPSERT deduplication)
- ⬜ Parser unit test suite (SelectorEngine, SelectorParser)
- ⬜ Hack2Skill & Kaggle scrapers (future expansion)

## Key Rules
1. **Patchright only** — never use Playwright directly
2. **Downward-only dependencies** — upper layers depend on lower, never reverse
3. **Composition over inheritance** — own components, don't inherit them
4. **No speculative complexity** — only build what's needed for the current phase
