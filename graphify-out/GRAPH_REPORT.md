# Graph Report - d:/Programming/Python/Global AI opportunity Tracker/global-ai-opportunity-tracker-backend  (2026-07-02)

## Corpus Check
- Corpus is ~10,084 words - fits in a single context window. You may not need a graph.

## Summary
- 440 nodes · 764 edges · 46 communities (39 shown, 7 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 54 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]

## God Nodes (most connected - your core abstractions)
1. `OpportunityParser` - 31 edges
2. `BrowserLaunchOptions` - 19 edges
3. `Opportunity` - 18 edges
4. `BrowserManager` - 17 edges
5. `ParserUtils` - 17 edges
6. `BaseScraper` - 17 edges
7. `Selector` - 16 edges
8. `SelectorEngine` - 15 edges
9. `LiteLLMClient` - 15 edges
10. `LLMValidationError` - 15 edges

## Surprising Connections (you probably didn't know these)
- `ConcreteScraper` --uses--> `BrowserLaunchOptions`  [INFERRED]
  tests/scraper/scrapers/test_base_scraper.py → scraper/core/browser/models.py
- `SelectorParser` --uses--> `SelectorProfile`  [INFERRED]
  scraper/parsers/selector_parser.py → shared/llm/selector_profile.py
- `BaseSiteParser` --uses--> `Opportunity`  [INFERRED]
  scraper/parsers/site_parser.py → shared/models/opportunity.py
- `test_init_with_options()` --calls--> `BrowserLaunchOptions`  [EXTRACTED]
  tests/scraper/scrapers/test_base_scraper.py → scraper/core/browser/models.py
- `OpportunityParser` --uses--> `DifficultyLevel`  [INFERRED]
  scraper/parsers/opportunity_parser.py → shared/models/enums.py

## Import Cycles
- None detected.

## Communities (46 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (53): ModelResponse, LiteLLMClient, Validates an LLM request before execution., Builds a TokenUsage object from a LiteLLM response., Client for interacting with LLM providers using LiteLLM., Generate a response from an LLM provider., LLMAuthenticationError, LLMError (+45 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (48): BaseModel, NoReturn, OpportunityParser, E, T, Validates the input before parsing.          Subclasses can override this meth, Hook for lightweight preprocessing before parsing.          Currently returns, Gets a value from the raw mapping using ParserUtils.safe_get(). (+40 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (28): Normalizer, datetime, Prevents instantiation of the Normalizer class., Normalizes a value into a datetime., Normalizes a value into a trimmed, collapsed string., Normalizes various inputs into a clean list of strings., Normalizes a value into a boolean., Normalizes a value into an integer. (+20 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (25): ExtractionHandler, Handler, Locator, Page, TODO:         - Return list of elements or count, TODO:         - Extract from script tags or JSON-LD, TODO:         - Parse table elements into list of dicts, TODO:         - Iterate over multiple elements         - Return collection (+17 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (13): ABC, BaseParser, T, Abstract base class for all parsers in the scraping pipeline.      This class, Parses the input data into the target model type.          Subclasses may invo, Validate raw input before parsing.          Args:             data: The raw i, Preprocess raw input before parsing.          Args:             data: The raw, BaseSiteParser (+5 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (12): BaseException, BaseScraper, Execute website-specific scraping logic., Enter the asynchronous context manager.          Returns:             The scr, Abstract base class defining the contract and lifecycle for scrapers., Exit the asynchronous context manager., Access the browser lifecycle manager.          Returns:             The brows, Start the browser and create a new page. (+4 more)

### Community 6 - "Community 6"
Cohesion: 0.19
Nodes (12): main(), BrowserFactory, Factory responsible for creating Patchright browser objects., BrowserManager, Manages the Patchright browser lifecycle., Initialize the BrowserManager.          Args:             options: Browser la, BrowserLaunchOptions, Convert the viewport into Patchright's expected format. (+4 more)

### Community 7 - "Community 7"
Cohesion: 0.19
Nodes (10): BaseSettings, ColoredFormatter, Logger, Global application settings.     Values are automatically loaded from the .env, Settings, LogLevel, get_console_formatter(), get_console_handler() (+2 more)

### Community 8 - "Community 8"
Cohesion: 0.13
Nodes (10): Exception, BrowserContext, Page, Return the active browser instance.          Raises:             BrowserError, Return the active browser context.          Raises:             BrowserError:, Create a new page from the default browser context.          Raises:, BrowserError, Base exception for browser-related errors. (+2 more)

### Community 9 - "Community 9"
Cohesion: 0.16
Nodes (10): Page, Architecture:     Page     ↓     SelectorParser     ↓     SelectorEngine     ↓, Parses the page using the loaded selector profile., Performs lightweight validation of the selector profile., # TODO: Implement more robust validation, Extract canonical opportunity fields from the page.          Returns:, # TODO:, Cleans up and normalizes the extracted data. (+2 more)

### Community 10 - "Community 10"
Cohesion: 0.18
Nodes (10): Any, T, Loads a JSON string into a Python object., Validates parsed JSON against the specified Pydantic model., Generic parser for converting raw LLM responses into validated Pydantic models., Parses a raw LLM response into the specified Pydantic model.          Args:, Convenience method for parsing a SelectorProfile., Removes Markdown code fences from the response. (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.17
Nodes (14): ConcreteScraper, Verify goto delegates navigation to the page., Concrete subclass of BaseScraper for testing., Verify async context manager initializes and cleans up resources., Verify scraper instantiates BrowserManager with options., Verify page property raises BrowserError before start is called., Verify start initializes browser and creates a page., Verify stop closes page and browser resources. (+6 more)

### Community 12 - "Community 12"
Cohesion: 0.18
Nodes (8): Playwright, BrowserContext, Start the Patchright engine., Launch a Chromium browser instance., Create the default browser context., Start Patchright and launch the browser.          Raises:             Browser, Browser, BrowserEngine

## Knowledge Gaps
- **4 isolated node(s):** `trackit_backend`, `DateFormat`, `LLM`, `Scraper`
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `OpportunityParser` connect `Community 1` to `Community 2`, `Community 4`?**
  _High betweenness centrality (0.175) - this node is a cross-community bridge._
- **Why does `BrowserLaunchOptions` connect `Community 6` to `Community 1`, `Community 11`, `Community 12`, `Community 5`?**
  _High betweenness centrality (0.171) - this node is a cross-community bridge._
- **Why does `SelectorProfile` connect `Community 0` to `Community 9`, `Community 10`, `Community 3`, `Community 1`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `OpportunityParser` (e.g. with `BaseParser` and `ParserUtils`) actually correct?**
  _`OpportunityParser` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `BrowserLaunchOptions` (e.g. with `BrowserFactory` and `BrowserManager`) actually correct?**
  _`BrowserLaunchOptions` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Opportunity` (e.g. with `OpportunityParser` and `BaseSiteParser`) actually correct?**
  _`Opportunity` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BrowserManager` (e.g. with `BrowserFactory` and `BrowserLaunchOptions`) actually correct?**
  _`BrowserManager` has 2 INFERRED edges - model-reasoned connections that need verification._