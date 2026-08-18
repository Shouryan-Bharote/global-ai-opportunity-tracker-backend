# Development Workflow

## Core Lifecycle
Every module follows the **Design → Implement → Test → Refactor** cycle.

## Branch Strategy
- `main` — Stable, tested code
- Feature branches for new phases or components

## Development Process

### 1. Before Starting Work
1. Read `context.md` for current phase and status
2. Read `.state/CURRENT_PHASE.md` for the active phase details
3. Check `.state/TASK_QUEUE.md` for pending work items
4. Review relevant `docs/phases/PHASE_XX.md` for requirements

### 2. During Development
1. Follow the architecture rules (downward-only dependencies)
2. Use type hints on all functions and methods
3. Use Pydantic v2+ for all data models
4. Use Google-style docstrings
5. Run `graphify update .` after code changes to keep the knowledge graph current

### 3. After Completing Work
1. Run tests: `poetry run pytest tests/ -v`
2. Update `.state/DEVELOPMENT_STATUS.md`
3. Update `.state/CURRENT_PHASE.md` if sub-tasks were completed
4. Update `context.md` status tracker
5. Log any decisions in `.state/DECISIONS.md`
6. Log any known issues in `.state/KNOWN_ISSUES.md`

## Coding Standards

### Mandatory
- **Python 3.13+** required
- **Type hints** on all function signatures
- **Pydantic v2+** for all data models
- **Google-style docstrings** for public APIs
- **Patchright** only — never use Playwright directly
- **LiteLLM** for LLM provider abstraction

### Prohibited
- Cross-layer imports (e.g., scraper importing from exporters)
- Speculative features not justified by current phase requirements
- Deep inheritance chains — prefer composition
- Redundant logging where lifecycle managers already log

## Testing
```bash
# Run all tests
poetry run pytest tests/ -v

# Run specific test file
poetry run pytest tests/scraper/scrapers/test_base_scraper.py -v

# Run with coverage
poetry run pytest tests/ --cov=scraper --cov=shared -v
```
