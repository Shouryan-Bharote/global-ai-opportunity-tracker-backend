# Features and Flows

## Core Features

### 1. Automated Web Scraping
- Uses Patchright (Chromium-based) for stealth browser automation
- `BaseScraper` provides lifecycle management for all scrapers
- Concrete scrapers implement platform-specific extraction logic

### 2. LLM-Driven Selector Generation
- Sends page HTML to LLM (Gemini/Groq/OpenRouter) via LiteLLM
- LLM generates `SelectorProfile` with CSS/XPath selectors per field
- Selectors include priority, confidence, wait_for, and timeout metadata
- `OpportunityField` enum constrains outputs to valid fields only

### 3. Intelligent Data Extraction
- `SelectorEngine` executes selectors in priority order with automatic fallback
- Supports 6 extraction types: text, attribute, html, list, table, json
- `SelectorParser` orchestrates the extraction pipeline
- `SelectorProfileValidator` ensures profile integrity before extraction

### 4. Structured Data Parsing
- `OpportunityParser` converts raw extracted dicts into `Opportunity` models
- `Normalizer` handles datetime, boolean, integer, and string normalization
- `ParserUtils` provides safe access and type coercion utilities

---

## Data Flow Diagram

```
┌──────────────┐
│  Target URL  │
└──────┬───────┘
       ↓
┌──────────────┐     ┌───────────────┐
│ BaseScraper  │────→│ BrowserManager│
│   .goto()    │     │  (Patchright)  │
└──────┬───────┘     └───────────────┘
       ↓
┌──────────────┐     ┌───────────────┐
│  LLMManager  │────→│ LiteLLMClient │
│  .generate() │     │ (Gemini/Groq) │
└──────┬───────┘     └───────────────┘
       ↓
┌──────────────┐
│SelectorProfile│ (CSS/XPath selectors per field)
└──────┬───────┘
       ↓
┌──────────────┐     ┌───────────────┐
│SelectorParser│────→│SelectorEngine │
│   .parse()   │     │  (extraction)  │
└──────┬───────┘     └───────────────┘
       ↓
┌──────────────┐
│  dict[str,   │ (raw key-value pairs)
│    object]   │
└──────┬───────┘
       ↓
┌──────────────────┐
│OpportunityParser │
│     .parse()     │
└──────┬───────────┘
       ↓
┌──────────────┐
│  Opportunity │ (structured Pydantic model)
└──────────────┘
```

## Target Platforms
| Platform | Status | Description |
|----------|--------|-------------|
| Unstop | ⬜ Planned | Hackathons, competitions, quizzes |
| Hack2Skill | ⬜ Planned | Hackathons, innovation challenges |
| Devpost | ⬜ Planned | Hackathons, software competitions |
| Kaggle | ⬜ Planned | ML competitions, datasets |

## Opportunity Categories
Hackathon, Competition, Conference, Workshop, Fellowship, Internship, Scholarship, Grant, Research Program, Bootcamp, Course, Challenge, Other
