# Task Queue

## Active
- [ ] **Build first concrete scraper** — Pick a platform (Unstop or Devpost recommended) and implement the full scraper class extending `BaseScraper`.
- [ ] **Write unit tests for parser layer** — `SelectorEngine`, `SelectorParser` need test coverage.

## Backlog
- [ ] End-to-end integration test: URL → `Opportunity` model
- [ ] Fix unused `elements` variable in `SelectorEngine._extract_list()`
- [ ] LLM response caching for selector profiles
- [ ] Prompt versioning for selector generation
- [ ] Multi-provider fallback (Gemini → Groq → OpenRouter)

## Completed
- [x] Add `OpportunityField(StrEnum)` to `shared/models/enums.py`
- [x] Update `ExtractionField.name` to use `OpportunityField`
- [x] Implement `SelectorEngine` extraction handlers
- [x] Integrate `SelectorParser` with `SelectorEngine` + `SelectorProfileValidator`
- [x] Update `SelectorProfileValidator` for enum compatibility
- [x] Create project documentation structure
