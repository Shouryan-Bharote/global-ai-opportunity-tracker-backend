# Graph Report - global-ai-opportunity-tracker-backend  (2026-08-15)

## Corpus Check
- 80 files · ~10,648 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 462 nodes · 812 edges · 54 communities (44 shown, 10 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 64 edges (avg confidence: 0.5)
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
- `SelectorParser` --uses--> `SelectorProfile`  [INFERRED]
  scraper/parsers/selector_parser.py → shared/llm/selector_profile.py
- `SelectorParser` --uses--> `SelectorProfileValidator`  [INFERRED]
  scraper/parsers/selector_parser.py → shared/llm/validator.py
- `BaseSiteParser` --uses--> `Opportunity`  [INFERRED]
  scraper/parsers/site_parser.py → shared/models/opportunity.py
- `test_init_with_options()` --calls--> `BrowserLaunchOptions`  [EXTRACTED]
  tests/scraper/scrapers/test_base_scraper.py → scraper/core/browser/models.py

## Import Cycles
- None detected.

## Communities (54 total, 10 thin omitted)

### Community 0 - "manager.py"
Cohesion: 0.15
Nodes (13): LLMProvider, Supported LLM providers., ProviderConfig, Providers, Configuration for a specific LLM provider., Central registry for supported LLM providers., Prevent instantiation., Returns the configuration for a provider.          Args:             provider (+5 more)

### Community 1 - "OpportunityParser"
Cohesion: 0.06
Nodes (48): BaseModel, NoReturn, OpportunityParser, E, T, Validates the input before parsing.          Subclasses can override this meth, Hook for lightweight preprocessing before parsing.          Currently returns, Gets a value from the raw mapping using ParserUtils.safe_get(). (+40 more)

### Community 2 - "ParserUtils"
Cohesion: 0.05
Nodes (28): Normalizer, datetime, Prevents instantiation of the Normalizer class., Normalizes a value into a datetime., Normalizes a value into a trimmed, collapsed string., Normalizes various inputs into a clean list of strings., Normalizes a value into a boolean., Normalizes a value into an integer. (+20 more)

### Community 3 - "Selector"
Cohesion: 0.07
Nodes (31): ExtractionHandler, ExtractionResult, Locator, Page, Extract normalized text content from the first matched element., Extract an HTML attribute value from the first matched element., Extract the inner HTML of the first matched element., Extract text from all matched elements as a list. (+23 more)

### Community 4 - "BaseParser"
Cohesion: 0.12
Nodes (13): ABC, BaseParser, T, Abstract base class for all parsers in the scraping pipeline.      This class, Parses the input data into the target model type.          Subclasses may invo, Validate raw input before parsing.          Args:             data: The raw i, Preprocess raw input before parsing.          Args:             data: The raw, BaseSiteParser (+5 more)

### Community 5 - "BaseScraper"
Cohesion: 0.11
Nodes (12): BaseException, BaseScraper, Execute website-specific scraping logic., Enter the asynchronous context manager.          Returns:             The scr, Abstract base class defining the contract and lifecycle for scrapers., Exit the asynchronous context manager., Access the browser lifecycle manager.          Returns:             The brows, Start the browser and create a new page. (+4 more)

### Community 6 - "BrowserLaunchOptions"
Cohesion: 0.19
Nodes (12): main(), BrowserFactory, Factory responsible for creating Patchright browser objects., BrowserManager, Manages the Patchright browser lifecycle., Initialize the BrowserManager.          Args:             options: Browser la, BrowserLaunchOptions, Convert the viewport into Patchright's expected format. (+4 more)

### Community 7 - "logger.py"
Cohesion: 0.18
Nodes (11): BaseSettings, ColoredFormatter, Handler, Logger, Global application settings.     Values are automatically loaded from the .env, Settings, LogLevel, get_console_formatter() (+3 more)

### Community 8 - "BrowserError"
Cohesion: 0.13
Nodes (10): Exception, BrowserContext, Page, Return the active browser instance.          Raises:             BrowserError, Return the active browser context.          Raises:             BrowserError:, Create a new page from the default browser context.          Raises:, BrowserError, Base exception for browser-related errors. (+2 more)

### Community 9 - "SelectorParser"
Cohesion: 0.23
Nodes (7): Page, Cleans up and normalizes the extracted data.          Performs lightweight norma, Orchestrates the extraction of data from a page using a SelectorProfile.      Ar, Parses the page using the loaded selector profile.          Args:             pa, Validates the selector profile using SelectorProfileValidator., Extract canonical opportunity fields from the page.          Instantiates a Sele, SelectorParser

### Community 10 - "ResponseParser"
Cohesion: 0.18
Nodes (9): LLMResponseParseError, Raised when the LLM response cannot be parsed., Any, T, Loads a JSON string into a Python object., Validates parsed JSON against the specified Pydantic model., Parses a raw LLM response into the specified Pydantic model.          Args:, Removes Markdown code fences from the response. (+1 more)

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
Cohesion: 0.14
Nodes (14): LLMValidationError, Raised when the LLM request or response is invalid., LLMManager, T, Parses an LLM response into the specified Pydantic model., Coordinates all LLM operations., Initializes the LLM manager., Generates a selector profile for a webpage. (+6 more)

### Community 52 - "client.py"
Cohesion: 0.24
Nodes (14): LiteLLMClient, Validates an LLM request before execution., Client for interacting with LLM providers using LiteLLM., Generate a response from an LLM provider., LLMAuthenticationError, LLMError, LLMProviderError, LLMRateLimitError (+6 more)

### Community 53 - "models.py"
Cohesion: 0.16
Nodes (11): ModelResponse, Builds a TokenUsage object from a LiteLLM response., Creates and sends an LLM request., LLMRequest, LLMResponse, LLMTask, Represents the token consumption for an LLM request and response., Represents a request sent to an LLM provider. (+3 more)

## Knowledge Gaps
- **18 isolated node(s):** `trackit_backend`, `DateFormat`, `LLM`, `Scraper`, `graphify` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BrowserLaunchOptions` connect `BrowserLaunchOptions` to `OpportunityParser`, `test_base_scraper.py`, `.create_context`, `BaseScraper`?**
  _High betweenness centrality (0.155) - this node is a cross-community bridge._
- **Why does `OpportunityParser` connect `OpportunityParser` to `ParserUtils`, `BaseParser`?**
  _High betweenness centrality (0.155) - this node is a cross-community bridge._
- **Why does `ParserUtils` connect `ParserUtils` to `OpportunityParser`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `OpportunityParser` (e.g. with `BaseParser` and `ParserUtils`) actually correct?**
  _`OpportunityParser` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SelectorEngine` (e.g. with `ExtractionField` and `ExtractionType`) actually correct?**
  _`SelectorEngine` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `BrowserLaunchOptions` (e.g. with `BrowserFactory` and `BrowserManager`) actually correct?**
  _`BrowserLaunchOptions` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Opportunity` (e.g. with `OpportunityParser` and `BaseSiteParser`) actually correct?**
  _`Opportunity` has 11 INFERRED edges - model-reasoned connections that need verification._