# Global AI Opportunity Tracker — Backend (TrackIT)

A robust, resilient backend engine and intelligent scraper pipeline for tracking global Artificial Intelligence and Machine Learning opportunities (Hackathons, Competitions, Quizzes, Conferences, and Hiring Challenges).

Built with **Python 3.13+**, **Patchright** (undetectable anti-bot browser automation), **LiteLLM** (Groq primary with Gemini fallback for self-healing AI selector extraction), and **Pydantic v2**.

---

## 🌟 Key Features

- **Anti-Bot Browser Automation**: Powered by `Patchright` (undetected Playwright fork) to bypass Cloudflare and complex modern bot protections.
- **Self-Healing LLM Selector Generation**:
  - Automatically analyzes live DOM trees to generate CSS/XPath selectors.
  - Multi-provider fallback orchestration: **Groq** (`groq/compound-mini`) primary with automatic fallback to **Google Gemini** (`gemini-3.6-flash`).
  - Intelligent selector caching in local JSON profiles to avoid repeated LLM calls.
- **Specialized Concrete Scrapers**:
  - **Devpost Scraper**: Extracts AI/ML hackathons and challenges with dynamic infinite scroll handling.
  - **Unstop Scraper**: Multi-category scanning (`AI/ML`, `Data Science`, `Data Analytics`) across Hackathons, Competitions, Quizzes, and Conferences with modal overlay handling.
- **Clean Pydantic Data Models**: Normalized canonical opportunity models (`Opportunity`, `Timeline`, `Location`, `Organizer`, `Prize`).
- **Structured Error Handling & Resilient Execution**: Exponential backoff retries for transient 503/429 LLM errors, configurable safety nets, and headless/headful toggle modes.

---

## 🏗️ Architecture Overview

```
global-ai-opportunity-tracker-backend/
├── scraper/
│   ├── core/               # Browser management & anti-detection configuration
│   │   └── browser/        # Patchright lifecycle & launch options
│   ├── extractors/         # HTML & DOM extraction logic
│   ├── generators/        # LLM prompt builders & selector generators
│   ├── parsers/           # Selector parsing, Opportunity canonical parsing
│   └── scrapers/          # Platform-specific scrapers
│       ├── base/          # Abstract BaseScraper lifecycle
│       ├── devpost/       # Devpost scraper & profile caching
│       └── unstop/        # Unstop scraper & profile caching
├── shared/
│   ├── config/            # Pydantic Settings & environment variables
│   ├── core/              # Global models & domain types
│   ├── llm/               # LiteLLM client, multi-provider manager, response parser
│   └── logging/           # Colorized logger setup
├── examples/              # Runnable standalone scraper test scripts
└── tests/                 # Unit & integration test suites
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.13+**
- **Poetry** (package and dependency manager)

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/Shouryan-Bharote/global-ai-opportunity-tracker-backend.git
cd global-ai-opportunity-tracker-backend

# Install dependencies using Poetry
poetry install

# Install Patchright browser binaries
poetry run patchright install chromium
```

### 2. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and set your API keys:

```env
# Application
APP_NAME=TrackIT Backend
DEBUG=False
LOG_LEVEL=INFO
ENVIRONMENT=development

# LLM Providers (Groq primary, Gemini fallback)
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key

# Browser
HEADLESS=True
```

---

## 🧪 Running Scrapers

You can run individual scrapers via the provided example runner scripts:

### Devpost Scraper
```bash
poetry run python -m examples.scraper.run_devpost
```
*Extracts AI hackathons from Devpost with automated infinite scroll and saves results to `scraper/data/outputs/devpost_opportunities.json`.*

### Unstop Scraper
```bash
poetry run python -m examples.scraper.run_unstop
```
*Scrapes AI/ML events across Unstop categories and saves output to `scraper/data/outputs/unstop_opportunities.json`.*

---

## 🧪 Running Tests

Run the test suite using `pytest`:

```bash
poetry run pytest
```

---

## 🗺️ Roadmap

- [x] **Phase 1: Foundation & Core Configuration**
- [x] **Phase 2: Patchright Browser Core & Anti-Bot Engine**
- [x] **Phase 3: Base Scraper Lifecycle & Selector Parser Framework**
- [x] **Phase 4: Platform Concrete Scrapers** (Devpost & Unstop)
- [x] **Phase 5: Self-Healing Multi-Provider LLM Fallback (Groq + Gemini)**
- [ ] **Phase 6: Persistent Database Layer (SQLModel + SQLite/PostgreSQL)**
- [ ] **Phase 7: Background Task Scheduler & Automated Runs**
- [ ] **Phase 8: FastAPI REST API Endpoints & Search Filters**
- [ ] **Phase 9: Deployment & Production Containerization**

---

## 📄 License

This project is licensed under the terms of the GNU General Public License v3.0 (GNU GPLv3). See the [LICENSE](LICENSE) file for details.
