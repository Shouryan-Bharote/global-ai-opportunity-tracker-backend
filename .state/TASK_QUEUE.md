# Task Queue

## Active
- [ ] **Build Devpost Concrete Scraper** — AI hackathons & global challenges scraper (`scraper/scrapers/devpost/`).
- [ ] **Write unit tests for parser layer** — `SelectorEngine`, `SelectorParser` test coverage.

## Backlog
- [ ] Unstop detail-page scraping (enriching listing cards with deep descriptions, timelines, and prize breakdowns)
- [ ] LLM response caching for selector profiles
- [ ] Multi-provider fallback strategy (Groq → Gemini → OpenRouter)

## Completed
- [x] Implement `DevpostScraper` and `DevpostProfileManager` (27 global AI hackathons parsed)
- [x] Implement `UnstopScraper` and `UnstopProfileManager` (174 unique AI opportunities parsed)
- [x] End-to-end verification of Unstop scraper (18 live opportunities parsed)
- [x] Fix `OpportunityParser._postprocess()` bug
- [x] Fix `SelectorEngine` timeout issue
- [x] Add auto-dismissal for Unstop login popup modal
- [x] Add `OpportunityField(StrEnum)` enum
- [x] Create project documentation and state infrastructure
