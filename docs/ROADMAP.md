# Roadmap

## Phase Overview

| Phase | Name | Status | Description |
|-------|------|--------|-------------|
| 0 | Research & Architecture | ✅ Done | Tech stack, design, planning |
| 1 | Foundation | ✅ Done | Poetry, logger, config, constants, models |
| 2 | Browser Engine Core | ✅ Done | Patchright integration, BrowserManager |
| 3 | Scraper Framework | ✅ Done | BaseScraper abstraction |
| 4 | Website Scrapers | ✅ Done | Concrete scrapers (Unstop, Devpost) + LLM-driven parsing |
| 5 | LLM Pipeline (Advanced) | ✅ Done | Multi-provider fallback (Groq + Gemini), 503 retries |
| 6 | Exporters & Persistence | 🔄 In Progress | JSON export, SQLModel persistence & deduplication |
| 7 | Database Layer | ⬜ Planned | Relational models, session management, migrations |
| 8 | Scheduler | ⬜ Planned | Automated job scheduling |
| 9 | FastAPI Backend | ⬜ Planned | REST API exposure |
| 10 | Deployment | ⬜ Planned | Docker, CI/CD, monitoring |

## Current Focus: Phase 6 / 7 (Database & Persistence)

### Completed
- [x] LLM Infrastructure (LiteLLMClient with 503 retries, LLMManager with fallback, ResponseParser)
- [x] Selector Profile system (SelectorProfile, ExtractionField, Selector)
- [x] Validation (SelectorProfileValidator, OpportunityField enum)
- [x] Parser pipeline (SelectorEngine, SelectorParser, OpportunityParser)
- [x] Concrete website scrapers:
  - [x] **Unstop**: Multi-category AI scan across 4 event types (174 opportunities)
  - [x] **Devpost**: AI/ML hackathon scraper with dynamic infinite scroll handling
- [x] JSON export pipeline (`scraper/data/outputs/`)

### In Progress
- [ ] SQLModel database persistence layer & UPSERT deduplication

## Future Milestones

### Short-term (Phases 6–7)
- Define SQLModel Opportunity and related relational tables.
- Implement database session manager and repository CRUD/UPSERT methods.
- Write unit test suite for parser layer (`SelectorEngine`, `SelectorParser`).

### Medium-term (Phases 6–8)
- Export pipeline for structured data
- Database persistence with deduplication
- Automated scheduling for periodic scrapes

### Long-term (Phases 9–10)
- FastAPI REST API with search, filtering, pagination
- Docker deployment with CI/CD
- Monitoring and alerting
