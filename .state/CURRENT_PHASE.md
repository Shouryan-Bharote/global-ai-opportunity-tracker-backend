# Current Phase

## Phase 4: Website Scrapers + LLM-Driven Parsing

### Sub-Phase Status

| Sub-Phase | Status | Description |
|-----------|--------|-------------|
| 4A: LLM Infrastructure | ✅ Done | LiteLLMClient, LLMManager, models, response parser, prompts |
| 4B: Selector Profile & Validation | ✅ Done | SelectorProfile, ExtractionField, OpportunityField, Validator |
| 4C: Parser Pipeline | ✅ Done | SelectorEngine, SelectorParser, OpportunityParser, Normalizer |
| 4D: Concrete Scrapers | ⬜ Not Started | Unstop, Hack2Skill, Devpost, Kaggle |

### Current Focus
**Sub-Phase 4D: Concrete Scrapers** — Build platform-specific scrapers that inherit from `BaseScraper` and use the LLM-driven selector/parser pipeline.

### Next Steps
1. Pick first target platform (recommended: Unstop or Devpost)
2. Implement concrete scraper class extending `BaseScraper`
3. Integrate with `LLMManager` for selector generation
4. Wire up `SelectorParser` → `OpportunityParser` pipeline
5. Test end-to-end: URL → `Opportunity` model

### Blocked By
- Nothing — all infrastructure is in place
