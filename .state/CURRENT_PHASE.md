# Current Phase

## Phase 4: Website Scrapers + LLM-Driven Parsing

### Sub-Phase Status

| Sub-Phase | Status | Description |
|-----------|--------|-------------|
| 4A: LLM Infrastructure | ✅ Done | LiteLLMClient, LLMManager, models, response parser, prompts |
| 4B: Selector Profile & Validation | ✅ Done | SelectorProfile, ExtractionField, OpportunityField, Validator |
| 4C: Parser Pipeline | ✅ Done | SelectorEngine, SelectorParser, OpportunityParser, Normalizer |
| 4D: Concrete Scrapers | 🔄 In Progress | Unstop (✅ Done), Hack2Skill (⬜), Devpost (⬜), Kaggle (⬜) |

### Current Focus
**Sub-Phase 4D: Concrete Scrapers** — Next target scrapers: Devpost, Hack2Skill, Kaggle.

### Next Steps
1. Build second concrete scraper (Devpost or Hack2Skill).
2. Write unit test suite for `SelectorEngine` and `SelectorParser`.
3. Add detail page scraping to `UnstopScraper` (for full descriptions, prizes, timelines).

### Blocked By
- None
