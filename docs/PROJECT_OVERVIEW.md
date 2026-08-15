# Project Overview

## Global AI Opportunity Tracker — Backend

### Mission
A production-quality, modular backend designed to automate the lifecycle of AI-related professional opportunities. The system transforms raw web data from fragmented sources into a structured, actionable data pipeline.

### What It Does
1. **Scrapes** targeted websites for AI/ML opportunities (hackathons, competitions, conferences, etc.)
2. **Uses LLMs** to intelligently generate CSS/XPath selectors for data extraction
3. **Normalizes** raw scraped data into unified internal formats
4. **Structures** the data via LLM-powered cleaning, categorization, and validation
5. **Stores** processed opportunities in a structured database
6. **Exposes** the data through a high-performance FastAPI REST API

### Tech Stack
| Component | Technology |
|-----------|-----------|
| Language | Python 3.13+ |
| Browser Automation | Patchright (stealth Chromium) |
| LLM Orchestration | LiteLLM (Gemini, Groq, OpenRouter) |
| Data Validation | Pydantic v2+ |
| Package Management | Poetry |
| Testing | pytest |
| API Framework | FastAPI (planned) |
| Database | TBD (planned) |

### Target Platforms
- **Primary**: Unstop, Hack2Skill, Devpost, Kaggle
- **Categories**: Hackathons, Competitions, Conferences, Workshops, Research Programs, Scholarships, and more

### Current Status
- **Phase 4** in progress (Website Scrapers + LLM-Driven Parsing)
- Phases 0–3 completed (Foundation, Browser Engine, Scraper Framework)
- LLM infrastructure, selector profiles, and parser pipeline implemented
- Concrete website scrapers are next

### Getting Started
```bash
# Install dependencies
poetry install

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run tests
poetry run pytest tests/ -v
```
