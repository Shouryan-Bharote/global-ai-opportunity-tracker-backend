# Roadmap

## Phase Overview

| Phase | Name | Status | Description |
|-------|------|--------|-------------|
| 0 | Research & Architecture | ✅ Done | Tech stack, design, planning |
| 1 | Foundation | ✅ Done | Poetry, logger, config, constants, models |
| 2 | Browser Engine Core | ✅ Done | Patchright integration, BrowserManager |
| 3 | Scraper Framework | ✅ Done | BaseScraper abstraction |
| 4 | Website Scrapers | 🔄 In Progress | Concrete scrapers + LLM-driven parsing |
| 5 | LLM Pipeline (Advanced) | ⬜ Planned | Caching, retries, multi-provider fallback |
| 6 | Exporters | ⬜ Planned | JSON, CSV export |
| 7 | Database | ⬜ Planned | Persistence, deduplication |
| 8 | Scheduler | ⬜ Planned | Automated job scheduling |
| 9 | FastAPI Backend | ⬜ Planned | REST API exposure |
| 10 | Deployment | ⬜ Planned | Docker, CI/CD, monitoring |

## Current Focus: Phase 4

### Completed
- [x] LLM Infrastructure (LiteLLMClient, LLMManager, models, response parser)
- [x] Selector Profile system (SelectorProfile, ExtractionField, Selector)
- [x] Validation (SelectorProfileValidator, OpportunityField enum)
- [x] Parser pipeline (SelectorEngine, SelectorParser, OpportunityParser)

### In Progress
- [ ] Concrete website scrapers (Unstop, Hack2Skill, Devpost, Kaggle)

## Future Milestones

### Short-term (Phases 4–5)
- Complete at least one working concrete scraper (e.g., Unstop)
- End-to-end test: URL → Opportunity model
- LLM response caching to reduce costs

### Medium-term (Phases 6–8)
- Export pipeline for structured data
- Database persistence with deduplication
- Automated scheduling for periodic scrapes

### Long-term (Phases 9–10)
- FastAPI REST API with search, filtering, pagination
- Docker deployment with CI/CD
- Monitoring and alerting
