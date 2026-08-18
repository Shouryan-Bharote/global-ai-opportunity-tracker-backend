# Phase 1: Foundation

## Status: ✅ COMPLETED

## Objective
Set up the project skeleton, dependency management, logging, configuration, and shared utilities.

## Deliverables
- Poetry project with `pyproject.toml` and `poetry.lock`
- Shared configuration via Pydantic `BaseSettings` (loaded from `.env`)
- Structured logger with colored console output
- Constants modules for browser, files, formats, LLM, logging, and scraper settings
- Exception hierarchy foundation

## Key Files
| File | Purpose |
|------|---------|
| `pyproject.toml` | Project metadata and dependencies |
| `shared/config/settings.py` | `Settings` class — env-driven configuration |
| `shared/logger/__init__.py` | Logger setup with `ColoredFormatter` |
| `shared/constants/browser.py` | Browser-related constants |
| `shared/constants/files.py` | File path constants |
| `shared/constants/formats.py` | Date/time format constants |
| `shared/constants/llm.py` | LLM provider constants |
| `shared/constants/logging.py` | Log level constants |
| `shared/constants/scraper.py` | Scraper-related constants |
| `shared/models/enums.py` | Domain enums (OpportunityType, OpportunityStatus, etc.) |

## Design Decisions
- `Settings` uses `BaseSettings` for automatic `.env` loading.
- Logger supports both file and console handlers.
- Constants are organized by domain to avoid a single monolithic file.
