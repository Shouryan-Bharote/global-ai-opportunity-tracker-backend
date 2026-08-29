# Phase 4: Website Scrapers + LLM-Driven Parsing

## Status: 🔄 IN PROGRESS

## Objective
Build the concrete website scrapers and the LLM-driven selector profile generation and extraction pipeline that connects scraping to structured data output.

## Sub-Phases

### 4A: LLM Infrastructure (✅ Completed)
- `LiteLLMClient` — provider-agnostic LLM interaction via LiteLLM
- `LLMManager` — orchestrates LLM operations including selector profile generation
- `LLMRequest` / `LLMResponse` / `LLMTask` models
- `ResponseParser` — parses raw LLM text into Pydantic models
- `PromptTemplates` — manages system/user prompts for selector generation
- Provider registry (`ProviderConfig`, `Providers`)
- LLM exception hierarchy (`LLMError`, `LLMAuthenticationError`, `LLMRateLimitError`, etc.)

### 4B: Selector Profile & Validation (✅ Completed)
- `SelectorProfile` — Pydantic model representing LLM-generated CSS/XPath selectors
- `ExtractionField` — individual field extraction config with typed `OpportunityField` names
- `Selector` — locator definition with priority, confidence, wait_for, timeout
- `SelectorProfileValidator` — validates profile structure and constraints
- `OpportunityField(StrEnum)` — constrains LLM outputs to valid Opportunity model fields

### 4C: Parser Pipeline (✅ Completed)
- `SelectorEngine` — core extraction engine dispatching on `ExtractionType` (text, attribute, html, list, table, json)
- `SelectorParser` — orchestrates field extraction using `SelectorEngine` + `SelectorProfileValidator`
- `BaseParser` — abstract parser base class
- `OpportunityParser` — parses extracted dict into `Opportunity` model
- `ParserUtils` — safe_get, type coercion utilities
- `Normalizer` — whitespace, datetime, boolean normalization
- `BaseSiteParser` — site-specific parser base

### 4D: Concrete Scrapers (✅ Completed Baseline)
- Unstop scraper (`scraper/scrapers/unstop/scraper.py` — multi-category scan, modal overlay dismissal)
- Devpost scraper (`scraper/scrapers/devpost/scraper.py` — dynamic infinite scroll handling)
- Hack2Skill scraper (Planned future expansion)
- Kaggle scraper (Planned future expansion)

## Key Files
| File | Purpose |
|------|---------|
| `shared/llm/client.py` | LiteLLM client |
| `shared/llm/manager.py` | LLM operation orchestration |
| `shared/llm/models.py` | Request/Response/Task models |
| `shared/llm/response_parser.py` | JSON parsing from LLM output |
| `shared/llm/prompt_templates.py` | Prompt management |
| `shared/llm/selector_profile.py` | SelectorProfile + ExtractionField models |
| `shared/llm/validator.py` | SelectorProfileValidator |
| `shared/llm/exceptions.py` | LLM exception hierarchy |
| `shared/models/enums.py` | OpportunityField + domain enums |
| `scraper/parsers/selector_engine.py` | Extraction engine |
| `scraper/parsers/selector_parser.py` | Orchestration parser |
| `scraper/parsers/base_parser.py` | Abstract parser base |
| `scraper/parsers/opportunity_parser.py` | Opportunity data parser |
| `scraper/parsers/parser_utils.py` | Parsing utilities |
| `scraper/parsers/normalizer.py` | Data normalizer |
| `scraper/parsers/site_parser.py` | Site-specific parser base |

## Data Flow
```
Website Page
    ↓ (Patchright)
BaseScraper.scrape()
    ↓ (HTML page)
LLMManager.generate_selector_profile()
    ↓ (sends page HTML to LLM)
SelectorProfile (LLM-generated CSS/XPath selectors)
    ↓
SelectorParser.parse(page)
    ↓ (uses SelectorEngine to extract fields)
dict[str, object] (raw extracted data)
    ↓
OpportunityParser.parse(data)
    ↓
Opportunity (structured Pydantic model)
```
