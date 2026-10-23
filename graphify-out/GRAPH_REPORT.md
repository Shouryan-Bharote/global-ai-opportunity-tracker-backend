# Graph Report - global-ai-opportunity-tracker-backend  (2026-10-18)

## Corpus Check
- 136 files · ~126,801 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1115 nodes · 1827 edges · 98 communities (86 shown, 12 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 151 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f3131dc9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_manager.py|manager.py]]
- [[_COMMUNITY_OpportunityParser|OpportunityParser]]
- [[_COMMUNITY_ParserUtils|ParserUtils]]
- [[_COMMUNITY_Selector|Selector]]
- [[_COMMUNITY_BaseParser|BaseParser]]
- [[_COMMUNITY_BaseScraper|BaseScraper]]
- [[_COMMUNITY_BrowserLaunchOptions|BrowserLaunchOptions]]
- [[_COMMUNITY_logger.py|logger.py]]
- [[_COMMUNITY_BrowserError|BrowserError]]
- [[_COMMUNITY_SelectorParser|SelectorParser]]
- [[_COMMUNITY_ResponseParser|ResponseParser]]
- [[_COMMUNITY_test_base_scraper.py|test_base_scraper.py]]
- [[_COMMUNITY_.create_context|.create_context]]
- [[_COMMUNITY_BrowserLaunchOptions|BrowserLaunchOptions]]
- [[_COMMUNITY_PromptTemplates|PromptTemplates]]
- [[_COMMUNITY_.get|.get]]
- [[_COMMUNITY_formats.py|formats.py]]
- [[_COMMUNITY_llm.py|llm.py]]
- [[_COMMUNITY_scraper.py|scraper.py]]
- [[_COMMUNITY_trackit_backend|trackit_backend]]
- [[_COMMUNITY_job_scheduler.py|job_scheduler.py]]
- [[_COMMUNITY___init__.py|__init__.py]]
- [[_COMMUNITY___init__.py|__init__.py]]
- [[_COMMUNITY_scraper.py|scraper.py]]
- [[_COMMUNITY_Project Context Blueprint Global AI Opportunity Tracker (Antigravity IDE)|Project Context Blueprint: Global AI Opportunity Tracker (Antigravity IDE)]]
- [[_COMMUNITY_Project Context Global AI Opportunity Tracker Backend|Project Context: Global AI Opportunity Tracker Backend]]
- [[_COMMUNITY_graphify|graphify.md]]
- [[_COMMUNITY_graphify|graphify.md]]
- [[_COMMUNITY_README|README.md]]
- [[_COMMUNITY_manager.py|manager.py]]
- [[_COMMUNITY_client.py|client.py]]
- [[_COMMUNITY_models.py|models.py]]
- [[_COMMUNITY_Phase 4 Website Scrapers + LLM-Driven Parsing|Phase 4: Website Scrapers + LLM-Driven Parsing]]
- [[_COMMUNITY_Core Features|Core Features]]
- [[_COMMUNITY_Future Milestones|Future Milestones]]
- [[_COMMUNITY_Workflow Agent Session Startup|Workflow: Agent Session Startup]]
- [[_COMMUNITY_Architecture|Architecture]]
- [[_COMMUNITY_Codebase Guide|Codebase Guide]]
- [[_COMMUNITY_Global AI Opportunity Tracker — Backend|Global AI Opportunity Tracker — Backend]]
- [[_COMMUNITY_Current Context|Current Context]]
- [[_COMMUNITY_Phase 2 Browser Engine Core|Phase 2: Browser Engine Core]]
- [[_COMMUNITY_Phase 3 Scraper Framework|Phase 3: Scraper Framework]]
- [[_COMMUNITY_Decisions Log|Decisions Log]]
- [[_COMMUNITY_Phase 0 Research and Architecture|Phase 0: Research and Architecture]]
- [[_COMMUNITY_Phase 1 Foundation|Phase 1: Foundation]]
- [[_COMMUNITY_Phase 4 Website Scrapers + LLM-Driven Parsing|Phase 4: Website Scrapers + LLM-Driven Parsing]]
- [[_COMMUNITY_Development Status|Development Status]]
- [[_COMMUNITY_Phase 5 LLM Pipeline (Advanced)|Phase 5: LLM Pipeline (Advanced)]]
- [[_COMMUNITY_Phase 6 Exporters|Phase 6: Exporters]]
- [[_COMMUNITY_Phase 7 Database|Phase 7: Database]]
- [[_COMMUNITY_Phase 8 Scheduler|Phase 8: Scheduler]]
- [[_COMMUNITY_Phase 9 FastAPI Backend|Phase 9: FastAPI Backend]]
- [[_COMMUNITY_Phase 10 Deployment|Phase 10: Deployment]]
- [[_COMMUNITY_Known Issues|Known Issues]]
- [[_COMMUNITY_Task Queue|Task Queue]]
- [[_COMMUNITY_.parse|.parse]]
- [[_COMMUNITY_agent-progress|agent-progress.md]]
- [[_COMMUNITY_.parse|.parse]]
- [[_COMMUNITY_debug_unstop_selectors.py|debug_unstop_selectors.py]]
- [[_COMMUNITY_Selector|Selector]]
- [[_COMMUNITY_OpportunityField|OpportunityField]]
- [[_COMMUNITY_test_api.py|test_api.py]]
- [[_COMMUNITY_🚀 What Would You Like to Do Next|🚀 What Would You Like to Do Next?]]
- [[_COMMUNITY_SelectorProfileValidator|SelectorProfileValidator]]
- [[_COMMUNITY_debug_unstop_pagination.py|debug_unstop_pagination.py]]
- [[_COMMUNITY_🎉 174 Unique AI Opportunities Collected!|🎉 174 Unique AI Opportunities Collected!]]
- [[_COMMUNITY_Hackathon Project Proposal|Hackathon Project Proposal]]
- [[_COMMUNITY_LLMManager|LLMManager]]
- [[_COMMUNITY_SelectorProfile|SelectorProfile]]
- [[_COMMUNITY_Agent_Chat_Export|Agent_Chat_Export.md]]
- [[_COMMUNITY_Question 2 Who provided the selectors for pagination, cookies, and login popups|Question 2: Who provided the selectors for pagination, cookies, and login popups?]]
- [[_COMMUNITY_File tree|File tree.md]]

## God Nodes (most connected - your core abstractions)
1. `Antigravity Agent Chat Export` - 125 edges
2. `OpportunityParser` - 38 edges
3. `BrowserLaunchOptions` - 32 edges
4. `SelectorProfile` - 32 edges
5. `DevpostScraper` - 29 edges
6. `UnstopScraper` - 27 edges
7. `OpportunityDB` - 26 edges
8. `Opportunity` - 25 edges
9. `LiteLLMClient` - 24 edges
10. `LLMProvider` - 23 edges

## Surprising Connections (you probably didn't know these)
- `TriggerResponse` --uses--> `ScraperOrchestrator`  [INFERRED]
  api/routers/jobs.py → scraper/core/scheduler/job_scheduler.py
- `TriggerResponse` --uses--> `OpportunityRepository`  [INFERRED]
  api/routers/jobs.py → shared/database/repository.py
- `ConcreteScraper` --uses--> `BrowserLaunchOptions`  [INFERRED]
  tests/scraper/scrapers/test_base_scraper.py → scraper/core/browser/models.py
- `test_page_property_error_before_start()` --indirect_call--> `BrowserError`  [INFERRED]
  tests/scraper/scrapers/test_base_scraper.py → scraper/core/exceptions/browser.py
- `test_stop_lifecycle()` --indirect_call--> `BrowserError`  [INFERRED]
  tests/scraper/scrapers/test_base_scraper.py → scraper/core/exceptions/browser.py

## Import Cycles
- None detected.

## Communities (98 total, 12 thin omitted)

### Community 0 - "manager.py"
Cohesion: 0.18
Nodes (21): LiteLLMClient, Validates an LLM request before execution., Client for interacting with LLM providers using LiteLLM., Generate a response from an LLM provider.          Retries automatically on 50, Execute a single LLM API call (no retry logic)., LLMAuthenticationError, LLMError, LLMProviderError (+13 more)

### Community 1 - "OpportunityParser"
Cohesion: 0.02
Nodes (125): 1. No Hardcoded Selectors, 1. Root Cause & Fix: Card-Scoped Selectors, 2. Seeing the Browser Window Live, 2. The LLM Generates the Selectors, 3. Fast and Cheap Execution, 4. Self-Healing, 5. What the Concrete Scraper Actually Does, `.agents/` — **2 files added** (+117 more)

### Community 2 - "ParserUtils"
Cohesion: 0.05
Nodes (28): Normalizer, datetime, Prevents instantiation of the Normalizer class., Normalizes a value into a datetime., Normalizes a value into a trimmed, collapsed string., Normalizes various inputs into a clean list of strings., Normalizes a value into a boolean., Normalizes a value into an integer. (+20 more)

### Community 3 - "Selector"
Cohesion: 0.08
Nodes (29): ExtractionHandler, ExtractionResult, Locator, Page, Extract normalized text content from the first matched element., Extract an HTML attribute value from the first matched element., Extract the inner HTML of the first matched element., Extract text from all matched elements as a list. (+21 more)

### Community 4 - "BaseParser"
Cohesion: 0.12
Nodes (13): ABC, BaseParser, T, Abstract base class for all parsers in the scraping pipeline.      This class, Parses the input data into the target model type.          Subclasses may invo, Validate raw input before parsing.          Args:             data: The raw i, Preprocess raw input before parsing.          Args:             data: The raw, BaseSiteParser (+5 more)

### Community 5 - "BaseScraper"
Cohesion: 0.11
Nodes (12): BaseException, BaseScraper, Execute website-specific scraping logic., Enter the asynchronous context manager.          Returns:             The scr, Abstract base class defining the contract and lifecycle for scrapers., Exit the asynchronous context manager., Initialize the scraper.          Args:             options: Configuration opt, Start the browser and create a new page. (+4 more)

### Community 6 - "BrowserLaunchOptions"
Cohesion: 0.19
Nodes (11): main(), Devpost Scraper End-to-End Runner.  Run with:     poetry run python -m exampl, main(), Unstop Scraper End-to-End Runner.  Run with:     poetry run python -m example, BrowserFactory, Factory responsible for creating Patchright browser objects., BrowserLaunchOptions, Convert the viewport into Patchright's expected format. (+3 more)

### Community 7 - "logger.py"
Cohesion: 0.16
Nodes (11): BaseSettings, ColoredFormatter, Handler, Logger, Global application settings.     Values are automatically loaded from the .env, Settings, LogLevel, get_console_formatter() (+3 more)

### Community 8 - "BrowserError"
Cohesion: 0.15
Nodes (9): Exception, BrowserContext, Page, Return the active browser context.          Raises:             BrowserError:, Create a new page from the default browser context.          Raises:, BrowserError, Base exception for browser-related errors., Page (+1 more)

### Community 9 - "SelectorParser"
Cohesion: 0.17
Nodes (10): Page, Cleans up and normalizes the extracted data.          Performs lightweight nor, Orchestrates the extraction of data from a page using a SelectorProfile., Parses the page using the loaded selector profile.          Args:, Validates the selector profile using SelectorProfileValidator., Extract canonical opportunity fields from the page.          Instantiates a Se, SelectorParser, Represents a complete selector profile for a webpage. (+2 more)

### Community 10 - "ResponseParser"
Cohesion: 0.14
Nodes (14): LLMResponseParseError, Raised when the LLM response cannot be parsed., Any, T, Extracts the first complete JSON object or array., Loads a JSON string into a Python object., Validates parsed JSON against the specified Pydantic model., Generic parser for converting raw LLM responses into validated Pydantic models. (+6 more)

### Community 11 - "test_base_scraper.py"
Cohesion: 0.17
Nodes (14): ConcreteScraper, Verify goto delegates navigation to the page., Concrete subclass of BaseScraper for testing., Verify async context manager initializes and cleans up resources., Verify scraper instantiates BrowserManager with options., Verify page property raises BrowserError before start is called., Verify start initializes browser and creates a page., Verify stop closes page and browser resources. (+6 more)

### Community 12 - ".create_context"
Cohesion: 0.15
Nodes (9): Playwright, BrowserContext, Start the Patchright engine., Launch a Chromium browser instance., Create the default browser context., Return the active browser instance.          Raises:             BrowserError, Start Patchright and launch the browser.          Raises:             Browser, Browser (+1 more)

### Community 13 - "BrowserLaunchOptions"
Cohesion: 0.20
Nodes (7): main(), BrowserManager, Returns True if the browser is currently running., Manages the Patchright browser lifecycle., Initialize the BrowserManager.          Args:             options: Browser la, Close all browser resources., Access the browser lifecycle manager.          Returns:             The brows

### Community 15 - ".get"
Cohesion: 0.11
Nodes (19): Initialize DevpostScraper.          Args:             options: Browser launch, LLMProvider, Supported LLM providers.      Built-in providers (Gemini, Groq, OpenRouter, NV, _build_registry(), ProviderConfig, Providers, Dynamic LLM provider registry.  Supports any OpenAI-compatible provider throug, Prevent instantiation — this is a pure namespace class. (+11 more)

### Community 27 - "job_scheduler.py"
Cohesion: 0.13
Nodes (11): main(), Run all scrapers sequentially (for testing) and return a list of statistics., Start the asynchronous scheduler to run scrapers at the given cron expression., Synchronous entrypoint that runs the async scheduler in an active event loop., Job function to be called by the scheduler., Run the orchestrator either as a scheduled daemon or a one-off batch., Orchestrates running of scrapers and stores results in the database., Run Unstop scraper and return opportunities. (+3 more)

### Community 31 - "__init__.py"
Cohesion: 0.12
Nodes (15): Session, OpportunityRepository, Any, Repository for OpportunityDB and JobRun with UPSERT and advanced filtering., Return job history records ordered from most recent to oldest., Aggregate stats across opportunities and sources., Insert or update an opportunity based on its ID or source URL.          Returns, Convert an OpportunityCreate into a flat dict suitable for OpportunityDB. (+7 more)

### Community 34 - "__init__.py"
Cohesion: 0.10
Nodes (21): 1. Category Filtering, 2. Multi-Event Type Iteration, 3. Deduplication, 🤖 Antigravity Agent, 🤖 Antigravity Agent, 🤖 Antigravity Agent, 🤖 Antigravity Agent, 🤖 Antigravity Agent (+13 more)

### Community 36 - "scraper.py"
Cohesion: 0.16
Nodes (11): Locator, Construct the category-filtered listing URL for a given event type.          E, Execute the full Unstop scraping pipeline across all target event types., Attempt to dismiss a cookie consent banner if visible., Attempt to dismiss login popup modal if visible., Wait for at least one opportunity card to appear on the page., Return a Locator pointing to all opportunity cards on the current page., Load the saved SelectorProfile or generate a new one via the LLM.          Ret (+3 more)

### Community 46 - "Project Context Blueprint: Global AI Opportunity Tracker (Antigravity IDE)"
Cohesion: 0.22
Nodes (8): 1\. Project Mission and Scope, 2\. Core Development Philosophy, 3\. Completed Development Phases (Phases 0–2), 4\. Technical Architecture and File Structure, 5\. Phase 3 Directive: The Scraper Framework, 6\. Mandatory Coding Rules and Workflow Constraints, 7\. Implementation Roadmap, Project Context Blueprint: Global AI Opportunity Tracker (Antigravity IDE)

### Community 47 - "Project Context: Global AI Opportunity Tracker Backend"
Cohesion: 0.33
Nodes (5): Current Phase: Phase 10: Deployment (Completed), Important Design Decisions & Constraints, Project Context: Global AI Opportunity Tracker Backend, Status Tracker, Technology Stack & Guidelines

### Community 50 - "README.md"
Cohesion: 0.14
Nodes (13): 1. Clone & Install Dependencies, 2. Environment Configuration, 🏗️ Architecture Overview, Devpost Scraper, 🚀 Getting Started, Global AI Opportunity Tracker — Backend (TrackIT), 🌟 Key Features, 📄 License (+5 more)

### Community 51 - "manager.py"
Cohesion: 0.06
Nodes (65): BaseModel, NoReturn, Run Devpost scraper and return opportunities., OpportunityParser, E, T, Validates the input before parsing.          Subclasses can override this meth, Hook for lightweight preprocessing before parsing.          Currently returns (+57 more)

### Community 52 - "client.py"
Cohesion: 0.08
Nodes (25): `BaseParser` — `scraper/parsers/base_parser.py`, `BaseScraper` — `scraper/scrapers/base/base_scraper.py`, Browser Engine Layer, `BrowserFactory` — `scraper/core/browser/factory.py`, `BrowserLaunchOptions` — `scraper/core/browser/models.py`, `BrowserManager` — `scraper/core/browser/manager.py`, Component Library, Domain Models (+17 more)

### Community 53 - "models.py"
Cohesion: 0.17
Nodes (11): 1. Before Starting Work, 2. During Development, 3. After Completing Work, Branch Strategy, Coding Standards, Core Lifecycle, Development Process, Development Workflow (+3 more)

### Community 54 - "Phase 4: Website Scrapers + LLM-Driven Parsing"
Cohesion: 0.18
Nodes (10): 4A: LLM Infrastructure (✅ Completed), 4B: Selector Profile & Validation (✅ Completed), 4C: Parser Pipeline (✅ Completed), 4D: Concrete Scrapers (✅ Completed Baseline), Data Flow, Key Files, Objective, Phase 4: Website Scrapers + LLM-Driven Parsing (+2 more)

### Community 55 - "Core Features"
Cohesion: 0.20
Nodes (9): 1. Automated Web Scraping, 2. LLM-Driven Selector Generation, 3. Intelligent Data Extraction, 4. Structured Data Parsing, Core Features, Data Flow Diagram, Features and Flows, Opportunity Categories (+1 more)

### Community 56 - "Future Milestones"
Cohesion: 0.20
Nodes (9): Completed, Current Focus: Phase 6 / 7 (Database & Persistence), Future Milestones, In Progress, Long-term (Phases 9–10), Medium-term (Phases 6–8), Phase Overview, Roadmap (+1 more)

### Community 57 - "Workflow: Agent Session Startup"
Cohesion: 0.22
Nodes (8): Step 1: Read Current Context, Step 2: Check Current Phase, Step 3: Check Task Queue, Step 4: Check Known Issues, Step 5: Review Recent Decisions, Step 6: Begin Work, Step 7: Update State, Workflow: Agent Session Startup

### Community 58 - "Architecture"
Cohesion: 0.22
Nodes (8): Architecture, Data Flow, Dependency Rules, Layer Diagram, Module Boundaries, Overview, `scraper/` — Scraping domain, `shared/` — Cross-cutting concerns

### Community 59 - "Codebase Guide"
Cohesion: 0.22
Nodes (8): Codebase Guide, Environment Setup, Key Entry Points, Project Root, Quick Reference, Running Tests, `scraper/` Package, `shared/` Package

### Community 60 - "Global AI Opportunity Tracker — Backend"
Cohesion: 0.22
Nodes (8): Current Status, Getting Started, Global AI Opportunity Tracker — Backend, Mission, Project Overview, Target Platforms, Tech Stack, What It Does

### Community 61 - "Current Context"
Cohesion: 0.22
Nodes (8): Current Context, Current Phase, Key Rules, Project, Tech Stack, What's Been Built, What's Next, What This Project Does

### Community 62 - "Phase 2: Browser Engine Core"
Cohesion: 0.25
Nodes (7): Architecture, Deferred Features, Deliverables, Key Files, Objective, Phase 2: Browser Engine Core, Status: ✅ COMPLETED

### Community 63 - "Phase 3: Scraper Framework"
Cohesion: 0.25
Nodes (7): API Contract, Deliverables, Design Constraints, Key Files, Objective, Phase 3: Scraper Framework, Status: ✅ COMPLETED

### Community 64 - "Decisions Log"
Cohesion: 0.17
Nodes (11): Decision 001 — Patchright over Playwright, Decision 002 — LiteLLM for LLM Orchestration, Decision 003 — Composition over Inheritance, Decision 004 — OpportunityField Enum, Decision 005 — SelectorEngine Dispatch on ExtractionType, Decision 006 — Primary/Fallback LLM Manager, Decision 007 — Devpost Infinite Scroll via Keyboard Press, Decision 008 — Session Persistence and Relative API Client Resolution (+3 more)

### Community 65 - "Phase 0: Research and Architecture"
Cohesion: 0.29
Nodes (6): Deliverables, Files Created, Key Decisions, Objective, Phase 0: Research and Architecture, Status: ✅ COMPLETED

### Community 66 - "Phase 1: Foundation"
Cohesion: 0.29
Nodes (6): Deliverables, Design Decisions, Key Files, Objective, Phase 1: Foundation, Status: ✅ COMPLETED

### Community 67 - "Phase 4: Website Scrapers + LLM-Driven Parsing"
Cohesion: 0.29
Nodes (6): Blocked By, Current Focus, Current Phase, Next Steps, Phase 10: Deployment (Completed), Sub-Phase Status

### Community 68 - "Development Status"
Cohesion: 0.12
Nodes (16): 2026-08-16 — Devpost Concrete Scraper Implementation & Profile Folder Relocation (Phase 4D Milestone), 2026-08-16 — Unstop Concrete Scraper Implementation (Phase 4D Baseline), 2026-08-16 — Unstop Multi-Category AI Scraper & Pagination Fixes (Phase 4D Baseline), 2026-08-17 — LLM Infrastructure Hardening & Scraper Bug Fixes, 2026-10-12 — Database Persistence Layer & Scheduler Implementation, 2026-10-12 — Universal LLM Provider System, 2026-10-13 — Phase 9: FastAPI Backend REST API, 2026-10-13 — Physical Device Networking Fix (+8 more)

### Community 69 - "Phase 5: LLM Pipeline (Advanced)"
Cohesion: 0.33
Nodes (5): Dependencies, Objective, Phase 5: LLM Pipeline (Advanced), Planned Work, Status: ⬜ NOT STARTED

### Community 70 - "Phase 6: Exporters"
Cohesion: 0.33
Nodes (5): Dependencies, Objective, Phase 6: Exporters, Planned Work, Status: ⬜ NOT STARTED

### Community 71 - "Phase 7: Database"
Cohesion: 0.33
Nodes (5): Delivered Work, Dependencies, Objective, Phase 7: Database, Status: ✅ COMPLETED

### Community 72 - "Phase 8: Scheduler"
Cohesion: 0.29
Nodes (6): Completed Work, Dependencies, Objective, Phase 8: Scheduler, Planned Work, Status: ✅ COMPLETED

### Community 73 - "Phase 9: FastAPI Backend"
Cohesion: 0.33
Nodes (5): Delivered Work, Dependencies, Objective, Phase 9: FastAPI Backend, Status: ✅ COMPLETED

### Community 74 - "Phase 10: Deployment"
Cohesion: 0.33
Nodes (5): Delivered Work, Dependencies, Objective, Phase 10: Deployment, Status: ✅ COMPLETED

### Community 75 - "Known Issues"
Cohesion: 0.33
Nodes (5): Format, KI-001 — No Tests for Parser Layer, KI-002 — Deferred Browser Features, KI-003 — SelectorEngine `_extract_list` Has Unused Variable, Known Issues

### Community 76 - "Task Queue"
Cohesion: 0.33
Nodes (5): Active, Backlog, Completed, Completed, Task Queue

### Community 77 - ".parse"
Cohesion: 0.17
Nodes (10): LLMTask, Supported tasks for LLM operations., PromptBuilder, Any, Builds a prompt for the given task., Returns the template for the specified task., Formats a template variable before insertion., Builds prompts from predefined templates. (+2 more)

### Community 79 - ".parse"
Cohesion: 0.40
Nodes (5): main(), LLM Connectivity Smoke Test.  Run with:     poetry run python examples/llm/te, Test connectivity for a single LLM provider., Run connectivity test for all configured providers., test_provider()

### Community 81 - "Selector"
Cohesion: 0.08
Nodes (28): create_app(), lifespan(), Lifecycle hook: initialize database tables and resources on startup., Application factory for the TrackIT REST API., _execute_scraper_background(), list_job_runs(), Retrieve execution history for all scrapers., Run scrapers asynchronously in the background. (+20 more)

### Community 82 - "OpportunityField"
Cohesion: 0.33
Nodes (4): ModelResponse, Builds a TokenUsage object from a LiteLLM response., Represents the token consumption for an LLM request and response., TokenUsage

### Community 83 - "test_api.py"
Cohesion: 0.12
Nodes (15): 1. Architecture Overview, 2. Quickstart: Local Docker Deployment, 3. Production Deployment Scenarios, 4. Database Management & Backups, 5. Security & Operational Checklist, Automatic Schema Creation, Deployment Guide — TrackIT Backend, Option A: Virtual Private Server (VPS / AWS EC2 / DigitalOcean) (+7 more)

### Community 84 - "🚀 What Would You Like to Do Next?"
Cohesion: 0.17
Nodes (12): 🤖 Antigravity Agent, 🤖 Antigravity Agent, 🤖 Antigravity Agent, 🤖 Antigravity Agent, 🤖 Antigravity Agent, 🤖 Antigravity Agent, 🤖 Antigravity Agent, 🤖 Antigravity Agent (+4 more)

### Community 85 - "SelectorProfileValidator"
Cohesion: 0.19
Nodes (6): Loads and saves the Unstop SelectorProfile to a local JSON file.      Keeping, Load the SelectorProfile from disk.          Returns:             The loaded, Save a SelectorProfile to disk.          Args:             profile: The profi, Delete the cached profile, forcing regeneration on the next run., UnstopProfileManager, Initialize UnstopScraper.          Args:             options: Browser launch

### Community 87 - "🎉 174 Unique AI Opportunities Collected!"
Cohesion: 0.18
Nodes (11): 🎉 174 Unique AI Opportunities Collected!, 🤖 Antigravity Agent, 🤖 Antigravity Agent, 📈 Dataset Growth, Graphify Update Summary:, 🧩 How does it work? (Architecture Breakdown), Next Steps: What would you like to build now?, 🧑 User (+3 more)

### Community 88 - "Hackathon Project Proposal"
Cohesion: 0.18
Nodes (10): 1. The Problem, 2. The Solution, 3. What Makes It Interesting (The AI Angle), 4. Architecture Highlights, 5. Technology Stack, 6. Current Progress (Honest Status), 7. Why This Fits a Hackathon, 8. Future Vision (+2 more)

### Community 89 - "LLMManager"
Cohesion: 0.19
Nodes (9): LLMManager, T, Creates and sends an LLM request., Parses an LLM response into the specified Pydantic model., Coordinates all LLM operations., Initializes the LLM manager., Generates a selector profile for a webpage.          Tries providers in the or, GenerationMetadata (+1 more)

### Community 91 - "SelectorProfile"
Cohesion: 0.17
Nodes (7): Path, DevpostProfileManager, Handles loading and saving the Devpost SelectorProfile to disk., Initialize DevpostProfileManager.          Args:             file_path: Path, Load the cached SelectorProfile from disk if it exists.          Returns:, Save a SelectorProfile to disk.          Args:             profile: The valid, Delete the cached profile file if it exists.

### Community 93 - "Agent_Chat_Export.md"
Cohesion: 0.25
Nodes (7): 🤖 Antigravity Agent, 📂 Check Your Output File, 📊 Dataset Breakdown, 🔥 Full Multi-Category AI/ML Dataset Extracted (79 Unique Opportunities!), 🛠️ Key Components Built & Fixed, 📊 Live Scrape Summary, 🎉 Milestone Achieved: Unstop Scraper is Live & Working!

## Knowledge Gaps
- **383 isolated node(s):** `trackit_backend`, `DateFormat`, `LLM`, `Scraper`, `Agent Progress` (+378 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `OpportunityParser` connect `manager.py` to `ParserUtils`, `BaseParser`, `scraper.py`, `.get`, `SelectorProfileValidator`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `BrowserLaunchOptions` connect `BrowserLaunchOptions` to `scraper.py`, `BaseScraper`, `test_base_scraper.py`, `.create_context`, `BrowserLaunchOptions`, `.get`, `manager.py`, `SelectorProfileValidator`, `job_scheduler.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `ParserUtils` connect `ParserUtils` to `manager.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `OpportunityParser` (e.g. with `BaseParser` and `ParserUtils`) actually correct?**
  _`OpportunityParser` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `BrowserLaunchOptions` (e.g. with `BrowserFactory` and `BrowserManager`) actually correct?**
  _`BrowserLaunchOptions` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `SelectorProfile` (e.g. with `SelectorParser` and `DevpostProfileManager`) actually correct?**
  _`SelectorProfile` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `DevpostScraper` (e.g. with `BrowserLaunchOptions` and `OpportunityParser`) actually correct?**
  _`DevpostScraper` has 15 INFERRED edges - model-reasoned connections that need verification._