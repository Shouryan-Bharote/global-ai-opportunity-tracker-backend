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
- ✅ LLM Infrastructure (LiteLLMClient, LLMManager, ResponseParser)
- ✅ Selector Profile system (SelectorProfile, ExtractionField, Selector, OpportunityField)
- ✅ Parser Pipeline (SelectorEngine, SelectorParser, OpportunityParser, Normalizer)

## What's Next
- ⬜ Concrete website scrapers (Unstop, Hack2Skill, Devpost, Kaggle)
- ⬜ End-to-end integration testing

## Key Rules
1. **Patchright only** — never use Playwright directly
2. **Downward-only dependencies** — upper layers depend on lower, never reverse
3. **Composition over inheritance** — own components, don't inherit them
4. **No speculative complexity** — only build what's needed for the current phase
