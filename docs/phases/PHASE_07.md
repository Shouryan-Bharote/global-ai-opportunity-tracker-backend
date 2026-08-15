# Phase 7: Database

## Status: ⬜ NOT STARTED

## Objective
Implement persistent storage for scraped opportunities with deduplication and update tracking.

## Planned Work
- Database schema design for Opportunity storage
- ORM or query builder integration
- Deduplication logic (by source_url or composite key)
- Update detection (has opportunity data changed since last scrape?)
- Migration system

## Dependencies
- Phase 4 must be complete (Opportunity model finalized)
