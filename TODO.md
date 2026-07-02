# Task TODO - SelectorEngine architectural refactor

- [x] Refactor `scraper/parsers/selector_engine.py`:

  - [x] Add `ExtractionHandler` type alias near top of file.
  - [x] Remove dispatch dictionary from `__init__`.
  - [x] Add private `@property _dispatch_map` returning mapping.
  - [x] Update typing of dispatch map to use `ExtractionHandler`.
  - [x] Add `_locator(self, selector: SelectorDefinition)` helper (unused).
  - [x] Improve unsupported selector `ValueError` message to include invalid type and supported types list.

  - [x] Replace `raise e` with bare `raise` in exception handling while preserving `logger.exception()`.

  - [x] Keep extraction methods as TODOs / `NotImplementedError`.
  - [x] Preserve public API, logging, imports/doc style.


