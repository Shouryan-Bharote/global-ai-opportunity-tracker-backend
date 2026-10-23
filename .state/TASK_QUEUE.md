# Task Queue

## Active
- [ ] **Write unit tests for parser layer** — `SelectorEngine`, `SelectorParser` test coverage.

## Completed
- [x] Implement `DevpostScraper` and `DevpostProfileManager` with dynamic infinite scroll handling
- [x] Implement `UnstopScraper` and `UnstopProfileManager` (174 unique AI opportunities parsed across 3 categories)
- [x] End-to-end verification of Unstop scraper (18 live opportunities parsed)
- [x] Fix `OpportunityParser._postprocess()` bug
- [x] Fix `SelectorEngine` timeout issue
- [x] Add auto-dismissal for Unstop login popup modal
- [x] Add `OpportunityField(StrEnum)` enum
- [x] Create project documentation and state infrastructure
- [x] **Phase 10: Dockerization** — Create production `Dockerfile` with Python 3.13-slim, system deps, and stealth Chromium pre-installed.
- [x] **Phase 10: Multi-Container Docker Compose** — Orchestrate `api`, `scheduler`, and PostgreSQL 16 `db` with automated health probes and volume persistence.
- [x] **Phase 10: Database Multi-Engine Portability** — Add `psycopg2-binary`, filter SQLite-only connect args when using PostgreSQL, and auto-normalize PaaS `postgres://` connection strings.
- [x] **Phase 10: CI/CD Pipeline** — Set up GitHub Actions workflow (`.github/workflows/ci.yml`) for pytest execution and Docker build validation.
- [x] **Phase 10: Deployment Documentation** — Create `docs/deployment.md` for local Docker, VPS + Nginx SSL, and Cloud PaaS deployments.

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
