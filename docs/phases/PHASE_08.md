# Phase 8: Scheduler

## Status: ⬜ NOT STARTED

## Objective
Automate scraping runs with a job scheduler that manages timing, concurrency, and error recovery.

## Planned Work
- Job scheduler implementation (`scraper/core/scheduler/job_scheduler.py`)
- Cron-like scheduling for periodic scrapes
- Concurrency control (max parallel scrapers)
- Error recovery and retry scheduling
- Job status tracking and reporting

## Dependencies
- Phase 4 (scrapers) and Phase 7 (database) must be complete
