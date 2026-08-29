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
- **Phases 0–5 Completed**: Foundation, Browser Engine, Base Scraper Framework, LLM Infrastructure (Groq primary + Gemini fallback), Selector Profiles & Validation, Parser Pipeline, and Concrete Scrapers (Unstop & Devpost).
- **Current Focus**: Transitioning from file-based JSON output to persistent database storage (SQLModel).

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
