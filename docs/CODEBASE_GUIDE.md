# Codebase Guide

## Quick Reference

### Project Root
```
global-ai-opportunity-tracker-backend/
├── .agents/            # Agent rules and workflows
├── .state/             # Project state tracking
├── docs/               # Project documentation
│   ├── phases/         # Phase-by-phase docs
│   ├── architecture/   # Architecture diagrams
│   ├── deployment/     # Deployment guides
│   ├── research/       # Research notes
│   └── scraper/        # Scraper-specific docs
├── examples/           # Usage examples
├── graphify-out/       # Knowledge graph output
├── scraper/            # Main scraping package
├── shared/             # Shared utilities & models
└── tests/              # Test suite
```

### `scraper/` Package
```
scraper/
├── core/
│   ├── browser/        # Browser engine (Patchright)
│   │   ├── config.py       → Browser configuration
│   │   ├── factory.py      → Static browser object creation
│   │   ├── manager.py      → Browser lifecycle management
│   │   ├── models.py       → BrowserLaunchOptions model
│   │   ├── protocols.py    → Interface definitions
│   │   ├── session.py      → Session management (deferred)
│   │   └── stealth.py      → Stealth config (deferred)
│   ├── exceptions/
│   │   └── browser.py      → BrowserError hierarchy
│   ├── manager/
│   │   └── scraper_manager.py → Scraper orchestration
│   └── scheduler/
│       └── job_scheduler.py   → Job scheduling (deferred)
├── data/
│   ├── outputs/        # Exported data files
│   └── screenshots/    # Captured screenshots
├── exporters/          # Data export modules (deferred)
├── parsers/
│   ├── base_parser.py      → Abstract parser base class
│   ├── normalizer.py       → Data normalization utilities
│   ├── opportunity_parser.py → Dict → Opportunity parser
│   ├── parser_utils.py     → Safe get, type coercion
│   ├── selector_engine.py  → Core extraction engine
│   ├── selector_parser.py  → Profile → extracted data
│   └── site_parser.py      → Site-specific parser base
└── scrapers/
    ├── base/
    │   └── base_scraper.py → Abstract scraper base class
    ├── devpost/        # Devpost scraper (planned)
    ├── hack2skill/     # Hack2Skill scraper (planned)
    ├── kaggle/         # Kaggle scraper (planned)
    └── unstop/         # Unstop scraper (planned)
```

### `shared/` Package
```
shared/
├── config/
│   └── settings.py     → Pydantic BaseSettings (env-driven)
├── constants/
│   ├── browser.py      → Browser-related constants
│   ├── files.py        → File path constants
│   ├── formats.py      → Date/time format constants
│   ├── llm.py          → LLM provider constants
│   ├── logging.py      → Log level constants
│   └── scraper.py      → Scraper-related constants
├── database/           # Database utilities (planned)
├── exceptions/         # Base exception hierarchy
├── llm/
│   ├── client.py           → LiteLLMClient
│   ├── exceptions.py       → LLM exception hierarchy
│   ├── manager.py          → LLMManager orchestration
│   ├── models.py           → LLMRequest/Response/Task
│   ├── prompt_templates.py → Prompt management
│   ├── response_parser.py  → LLM response → Pydantic
│   ├── selector_profile.py → SelectorProfile models
│   └── validator.py        → SelectorProfileValidator
├── logger/             → Colored console logger
├── models/
│   ├── enums.py        → Domain enums + OpportunityField
│   ├── location.py     → Location model
│   ├── metadata.py     → Metadata model
│   ├── opportunity.py  → Core Opportunity model
│   ├── organizer.py    → Organizer model
│   ├── prize.py        → Prize model
│   └── timeline.py     → Timeline model
└── utils/              # Shared utilities
```

## Key Entry Points
- **Browser example**: `examples/browser/basic_browser.py`
- **Configuration**: `shared/config/settings.py` (reads `.env`)
- **Core model**: `shared/models/opportunity.py`

## Running Tests
```bash
poetry run pytest tests/ -v
```

## Environment Setup
```bash
# 1. Install dependencies
poetry install

# 2. Copy environment template
cp .env.example .env

# 3. Fill in API keys in .env
```
