# Component Library

## Overview
This document catalogs all major classes and components in the project, organized by domain layer.

---

## Browser Engine Layer

### `BrowserFactory` — `scraper/core/browser/factory.py`
Static utility responsible for creating Patchright objects.
- `start_playwright()` → Playwright instance
- `launch_browser()` → Browser instance
- `create_context()` → BrowserContext

### `BrowserManager` — `scraper/core/browser/manager.py`
Manages the Patchright browser lifecycle.
- `start()` → Initialize browser + context
- `close()` → Tear down all resources
- `new_page()` → Create a new Page
- Properties: `browser` (read-only), `context` (read-only)

### `BrowserLaunchOptions` — `scraper/core/browser/models.py`
Pydantic model for browser launch configuration (headless, viewport, args, etc.).

---

## Scraper Framework Layer

### `BaseScraper` — `scraper/scrapers/base/base_scraper.py`
Abstract base class for all scrapers. Supports async context manager.
- `start()` / `stop()` — Lifecycle
- `goto(url)` — Navigation
- `scrape()` — Abstract contract
- Properties: `page`, `browser_manager`

---

## Parser Pipeline

### `SelectorEngine` — `scraper/parsers/selector_engine.py`
Core extraction engine. Dispatches on `ExtractionType`:
- `text` → `locator.text_content()` with whitespace normalization
- `attribute` → `locator.get_attribute()`
- `html` → `locator.inner_html()`
- `list` → `locator.all_text_contents()`
- `table` → Header-based row parsing into `list[dict]`
- `json` → Text content with JSON validation

### `SelectorParser` — `scraper/parsers/selector_parser.py`
Orchestrates extraction using SelectorEngine + SelectorProfileValidator.

### `OpportunityParser` — `scraper/parsers/opportunity_parser.py`
Parses a raw `dict[str, object]` into a structured `Opportunity` model.

### `BaseParser` — `scraper/parsers/base_parser.py`
Abstract parser base class with validate → preprocess → parse lifecycle.

### `ParserUtils` — `scraper/parsers/parser_utils.py`
Static utilities: `safe_get()`, type coercion helpers.

### `Normalizer` — `scraper/parsers/normalizer.py`
Whitespace normalization, datetime parsing, boolean coercion.

---

## LLM Layer

### `LiteLLMClient` — `shared/llm/client.py`
Provider-agnostic client for LLM interactions via LiteLLM.

### `LLMManager` — `shared/llm/manager.py`
High-level orchestrator for LLM operations (e.g., `generate_selector_profile()`).

### `ResponseParser` — `shared/llm/response_parser.py`
Parses raw LLM text into Pydantic models (handles markdown fences, JSON extraction).

### `SelectorProfile` — `shared/llm/selector_profile.py`
Pydantic model representing LLM-generated selectors for a webpage.

### `SelectorProfileValidator` — `shared/llm/validator.py`
Validates SelectorProfile structure, field names, selector priorities.

---

## Domain Models

### `Opportunity` — `shared/models/opportunity.py`
Core domain model with 22+ fields representing an AI/ML opportunity.

### Enums — `shared/models/enums.py`
- `OpportunityType`, `OpportunityStatus`, `LocationType`, `DifficultyLevel`
- `PrizeType`, `Currency`, `OpportunitySource`, `OpportunityField`

### Supporting Models
- `Location` — `shared/models/location.py`
- `Organizer` — `shared/models/organizer.py`
- `Prize` — `shared/models/prize.py`
- `Timeline` — `shared/models/timeline.py`
- `Metadata` — `shared/models/metadata.py`
