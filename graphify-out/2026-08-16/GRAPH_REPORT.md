# Graph Report - global-ai-opportunity-tracker-backend  (2026-08-15)

## Corpus Check
- 106 files · ~15,791 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 677 nodes · 1001 edges · 79 communities (67 shown, 12 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 64 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5489a8c6`
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
- [[_COMMUNITY_.is_running|.is_running]]
- [[_COMMUNITY_PromptTemplates|PromptTemplates]]
- [[_COMMUNITY_.get|.get]]
- [[_COMMUNITY_formats.py|formats.py]]
- [[_COMMUNITY_llm.py|llm.py]]
- [[_COMMUNITY_scraper.py|scraper.py]]
- [[_COMMUNITY_trackit_backend|trackit_backend]]
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

## God Nodes (most connected - your core abstractions)
1. `OpportunityParser` - 31 edges
2. `SelectorEngine` - 20 edges
3. `BrowserLaunchOptions` - 19 edges
4. `Opportunity` - 18 edges
5. `BrowserManager` - 17 edges
6. `ParserUtils` - 17 edges
7. `BaseScraper` - 17 edges
8. `SelectorProfile` - 16 edges
9. `LiteLLMClient` - 15 edges
10. `LLMValidationError` - 15 edges

## Surprising Connections (you probably didn't know these)
- `ConcreteScraper` --uses--> `BrowserLaunchOptions`  [INFERRED]
  tests/scraper/scrapers/test_base_scraper.py → scraper/core/browser/models.py
- `OpportunityParser` --uses--> `DifficultyLevel`  [INFERRED]
  scraper/parsers/opportunity_parser.py → shared/models/enums.py
- `OpportunityParser` --uses--> `OpportunityStatus`  [INFERRED]
  scraper/parsers/opportunity_parser.py → shared/models/enums.py
- `OpportunityParser` --uses--> `OpportunityType`  [INFERRED]
  scraper/parsers/opportunity_parser.py → shared/models/enums.py
- `OpportunityParser` --uses--> `Location`  [INFERRED]
  scraper/parsers/opportunity_parser.py → shared/models/location.py

## Import Cycles
- None detected.

## Communities (79 total, 12 thin omitted)

### Community 0 - "manager.py"
Cohesion: 0.06
Nodes (53): ModelResponse, LiteLLMClient, Validates an LLM request before execution., Builds a TokenUsage object from a LiteLLM response., Client for interacting with LLM providers using LiteLLM., Generate a response from an LLM provider., LLMAuthenticationError, LLMError (+45 more)

### Community 1 - "OpportunityParser"
Cohesion: 0.14
Nodes (28): BaseModel, Currency, DifficultyLevel, LocationType, OpportunitySource, OpportunityStatus, OpportunityType, PrizeType (+20 more)

### Community 2 - "ParserUtils"
Cohesion: 0.05
Nodes (28): Normalizer, datetime, Prevents instantiation of the Normalizer class., Normalizes a value into a datetime., Normalizes a value into a trimmed, collapsed string., Normalizes various inputs into a clean list of strings., Normalizes a value into a boolean., Normalizes a value into an integer. (+20 more)

### Community 3 - "Selector"
Cohesion: 0.08
Nodes (29): ExtractionHandler, ExtractionResult, Locator, Page, Extract normalized text content from the first matched element., Extract an HTML attribute value from the first matched element., Extract the inner HTML of the first matched element., Extract text from all matched elements as a list. (+21 more)

### Community 4 - "BaseParser"
Cohesion: 0.17
Nodes (11): ABC, BaseParser, Abstract base class for all parsers in the scraping pipeline.      This class, Validate raw input before parsing.          Args:             data: The raw i, Preprocess raw input before parsing.          Args:             data: The raw, BaseSiteParser, Generic base class for website-specific parsers.      This class is responsibl, Convert website-specific raw data into a canonical opportunity mapping. (+3 more)

### Community 5 - "BaseScraper"
Cohesion: 0.11
Nodes (12): BaseException, BaseScraper, Execute website-specific scraping logic., Enter the asynchronous context manager.          Returns:             The scr, Abstract base class defining the contract and lifecycle for scrapers., Exit the asynchronous context manager., Access the browser lifecycle manager.          Returns:             The brows, Start the browser and create a new page. (+4 more)

### Community 6 - "BrowserLaunchOptions"
Cohesion: 0.19
Nodes (12): main(), BrowserFactory, Factory responsible for creating Patchright browser objects., BrowserManager, Manages the Patchright browser lifecycle., Initialize the BrowserManager.          Args:             options: Browser la, BrowserLaunchOptions, Convert the viewport into Patchright's expected format. (+4 more)

### Community 7 - "logger.py"
Cohesion: 0.16
Nodes (11): BaseSettings, ColoredFormatter, Handler, Logger, Global application settings.     Values are automatically loaded from the .env, Settings, LogLevel, get_console_formatter() (+3 more)

### Community 8 - "BrowserError"
Cohesion: 0.13
Nodes (10): Exception, BrowserContext, Page, Return the active browser instance.          Raises:             BrowserError, Return the active browser context.          Raises:             BrowserError:, Create a new page from the default browser context.          Raises:, BrowserError, Base exception for browser-related errors. (+2 more)

### Community 9 - "SelectorParser"
Cohesion: 0.23
Nodes (7): Page, Cleans up and normalizes the extracted data.          Performs lightweight norma, Orchestrates the extraction of data from a page using a SelectorProfile.      Ar, Parses the page using the loaded selector profile.          Args:             pa, Validates the selector profile using SelectorProfileValidator., Extract canonical opportunity fields from the page.          Instantiates a Sele, SelectorParser

### Community 10 - "ResponseParser"
Cohesion: 0.18
Nodes (10): Any, T, Loads a JSON string into a Python object., Validates parsed JSON against the specified Pydantic model., Generic parser for converting raw LLM responses into validated Pydantic models., Parses a raw LLM response into the specified Pydantic model.          Args:, Convenience method for parsing a SelectorProfile., Removes Markdown code fences from the response. (+2 more)

### Community 11 - "test_base_scraper.py"
Cohesion: 0.17
Nodes (14): ConcreteScraper, Verify goto delegates navigation to the page., Concrete subclass of BaseScraper for testing., Verify async context manager initializes and cleans up resources., Verify scraper instantiates BrowserManager with options., Verify page property raises BrowserError before start is called., Verify start initializes browser and creates a page., Verify stop closes page and browser resources. (+6 more)

### Community 12 - ".create_context"
Cohesion: 0.18
Nodes (8): Playwright, BrowserContext, Start the Patchright engine., Launch a Chromium browser instance., Create the default browser context., Start Patchright and launch the browser.          Raises:             Browser, Browser, BrowserEngine

### Community 46 - "Project Context Blueprint: Global AI Opportunity Tracker (Antigravity IDE)"
Cohesion: 0.22
Nodes (8): 1\. Project Mission and Scope, 2\. Core Development Philosophy, 3\. Completed Development Phases (Phases 0–2), 4\. Technical Architecture and File Structure, 5\. Phase 3 Directive: The Scraper Framework, 6\. Mandatory Coding Rules and Workflow Constraints, 7\. Implementation Roadmap, Project Context Blueprint: Global AI Opportunity Tracker (Antigravity IDE)

### Community 47 - "Project Context: Global AI Opportunity Tracker Backend"
Cohesion: 0.33
Nodes (5): Current Phase: Phase 4 (Website Scrapers), Important Design Decisions & Constraints, Project Context: Global AI Opportunity Tracker Backend, Status Tracker, Technology Stack & Guidelines

### Community 51 - "manager.py"
Cohesion: 0.10
Nodes (20): NoReturn, OpportunityParser, E, T, Validates the input before parsing.          Subclasses can override this meth, Hook for lightweight preprocessing before parsing.          Currently returns, Gets a value from the raw mapping using ParserUtils.safe_get()., Parses a boolean field, defaulting to False. (+12 more)

### Community 52 - "client.py"
Cohesion: 0.08
Nodes (25): `BaseParser` — `scraper/parsers/base_parser.py`, `BaseScraper` — `scraper/scrapers/base/base_scraper.py`, Browser Engine Layer, `BrowserFactory` — `scraper/core/browser/factory.py`, `BrowserLaunchOptions` — `scraper/core/browser/models.py`, `BrowserManager` — `scraper/core/browser/manager.py`, Component Library, Domain Models (+17 more)

### Community 53 - "models.py"
Cohesion: 0.17
Nodes (11): 1. Before Starting Work, 2. During Development, 3. After Completing Work, Branch Strategy, Coding Standards, Core Lifecycle, Development Process, Development Workflow (+3 more)

### Community 54 - "Phase 4: Website Scrapers + LLM-Driven Parsing"
Cohesion: 0.18
Nodes (10): 4A: LLM Infrastructure (✅ Completed), 4B: Selector Profile & Validation (✅ Completed), 4C: Parser Pipeline (✅ Completed), 4D: Concrete Scrapers (⬜ Not Started), Data Flow, Key Files, Objective, Phase 4: Website Scrapers + LLM-Driven Parsing (+2 more)

### Community 55 - "Core Features"
Cohesion: 0.20
Nodes (9): 1. Automated Web Scraping, 2. LLM-Driven Selector Generation, 3. Intelligent Data Extraction, 4. Structured Data Parsing, Core Features, Data Flow Diagram, Features and Flows, Opportunity Categories (+1 more)

### Community 56 - "Future Milestones"
Cohesion: 0.20
Nodes (9): Completed, Current Focus: Phase 4, Future Milestones, In Progress, Long-term (Phases 9–10), Medium-term (Phases 6–8), Phase Overview, Roadmap (+1 more)

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
Cohesion: 0.25
Nodes (7): Decision 001 — Patchright over Playwright, Decision 002 — LiteLLM for LLM Orchestration, Decision 003 — Composition over Inheritance, Decision 004 — OpportunityField Enum, Decision 005 — SelectorEngine Dispatch on ExtractionType, Decisions Log, Format

### Community 65 - "Phase 0: Research and Architecture"
Cohesion: 0.29
Nodes (6): Deliverables, Files Created, Key Decisions, Objective, Phase 0: Research and Architecture, Status: ✅ COMPLETED

### Community 66 - "Phase 1: Foundation"
Cohesion: 0.29
Nodes (6): Deliverables, Design Decisions, Key Files, Objective, Phase 1: Foundation, Status: ✅ COMPLETED

### Community 67 - "Phase 4: Website Scrapers + LLM-Driven Parsing"
Cohesion: 0.29
Nodes (6): Blocked By, Current Focus, Current Phase, Next Steps, Phase 4: Website Scrapers + LLM-Driven Parsing, Sub-Phase Status

### Community 68 - "Development Status"
Cohesion: 0.29
Nodes (6): 2026-08-15 — Parser Layer Integration, Build Status, Development Status, Last Updated: 2026-08-15, Next Actions, Recent Changes

### Community 69 - "Phase 5: LLM Pipeline (Advanced)"
Cohesion: 0.33
Nodes (5): Dependencies, Objective, Phase 5: LLM Pipeline (Advanced), Planned Work, Status: ⬜ NOT STARTED

### Community 70 - "Phase 6: Exporters"
Cohesion: 0.33
Nodes (5): Dependencies, Objective, Phase 6: Exporters, Planned Work, Status: ⬜ NOT STARTED

### Community 71 - "Phase 7: Database"
Cohesion: 0.33
Nodes (5): Dependencies, Objective, Phase 7: Database, Planned Work, Status: ⬜ NOT STARTED

### Community 72 - "Phase 8: Scheduler"
Cohesion: 0.33
Nodes (5): Dependencies, Objective, Phase 8: Scheduler, Planned Work, Status: ⬜ NOT STARTED

### Community 73 - "Phase 9: FastAPI Backend"
Cohesion: 0.33
Nodes (5): Dependencies, Objective, Phase 9: FastAPI Backend, Planned Work, Status: ⬜ NOT STARTED

### Community 74 - "Phase 10: Deployment"
Cohesion: 0.33
Nodes (5): Dependencies, Objective, Phase 10: Deployment, Planned Work, Status: ⬜ NOT STARTED

### Community 75 - "Known Issues"
Cohesion: 0.33
Nodes (5): Format, KI-001 — No Tests for Parser Layer, KI-002 — Deferred Browser Features, KI-003 — SelectorEngine `_extract_list` Has Unused Variable, Known Issues

### Community 76 - "Task Queue"
Cohesion: 0.40
Nodes (4): Active, Backlog, Completed, Task Queue

## Knowledge Gaps
- **166 isolated node(s):** `trackit_backend`, `DateFormat`, `LLM`, `Scraper`, `Agent Progress` (+161 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BrowserLaunchOptions` connect `BrowserLaunchOptions` to `OpportunityParser`, `test_base_scraper.py`, `.create_context`, `BaseScraper`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `OpportunityParser` connect `manager.py` to `OpportunityParser`, `ParserUtils`, `BaseParser`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `ParserUtils` connect `ParserUtils` to `OpportunityParser`, `manager.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `OpportunityParser` (e.g. with `BaseParser` and `ParserUtils`) actually correct?**
  _`OpportunityParser` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SelectorEngine` (e.g. with `ExtractionField` and `ExtractionType`) actually correct?**
  _`SelectorEngine` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `BrowserLaunchOptions` (e.g. with `BrowserFactory` and `BrowserManager`) actually correct?**
  _`BrowserLaunchOptions` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Opportunity` (e.g. with `OpportunityParser` and `BaseSiteParser`) actually correct?**
  _`Opportunity` has 11 INFERRED edges - model-reasoned connections that need verification._