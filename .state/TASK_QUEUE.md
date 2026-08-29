# Task Queue

## Active
- [ ] **SQLModel Database Persistence Layer** — Define SQLModel models, database session management, and UPSERT deduplication (`scraper/storage/` or `shared/db/`).
- [ ] **Write unit tests for parser layer** — `SelectorEngine`, `SelectorParser` test coverage.

## Backlog
- [ ] Unstop detail-page scraping (enriching listing cards with deep descriptions, timelines, and prize breakdowns)
- [ ] LLM response caching for selector profiles
- [ ] Hack2Skill scraper
- [ ] Kaggle competitions scraper

## Completed
- [x] Implement `DevpostScraper` and `DevpostProfileManager` with dynamic infinite scroll handling
- [x] Implement `UnstopScraper` and `UnstopProfileManager` (174 unique AI opportunities parsed across 3 categories)
- [x] End-to-end verification of Unstop scraper (18 live opportunities parsed)
- [x] Fix `OpportunityParser._postprocess()` bug
- [x] Fix `SelectorEngine` timeout issue
- [x] Add auto-dismissal for Unstop login popup modal
- [x] Add `OpportunityField(StrEnum)` enum
- [x] Create project documentation and state infrastructure
