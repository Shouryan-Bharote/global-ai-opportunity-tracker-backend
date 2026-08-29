# Current Phase

## Phase 4: Website Scrapers + LLM-Driven Parsing

### Sub-Phase Status

| Sub-Phase | Status | Description |
|-----------|--------|-------------|
| 4A: LLM Infrastructure | ✅ Done | LiteLLMClient, LLMManager, models, response parser, prompts |
| 4B: Selector Profile & Validation | ✅ Done | SelectorProfile, ExtractionField, OpportunityField, Validator |
| 4C: Parser Pipeline | ✅ Done | SelectorEngine, SelectorParser, OpportunityParser, Normalizer |
| 4D: Concrete Scrapers | ✅ Done | Unstop (✅ Done, 174 parsed), Devpost (✅ Done, infinite scroll fixed), Hack2Skill (⬜), Kaggle (⬜) |

### Current Focus
**Transition to Phase 6 / Phase 7 (Data Persistence & Database)**:
- Implement SQLModel models and database repository layer for persisting scraped opportunities.
- Implement UPSERT logic with deduplication on opportunity URLs/IDs.

### Next Steps
1. Create SQLModel schema and database persistence layer.
2. Replace local JSON file outputs with database storage.
3. Write unit test suite for `SelectorEngine` and `SelectorParser`.
4. (Optional) Detail page enrichment for Unstop/Devpost.

### Blocked By
- None
