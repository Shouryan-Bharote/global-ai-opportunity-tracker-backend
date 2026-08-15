# Known Issues

## Format
- **ID**: Issue identifier
- **Severity**: Critical / High / Medium / Low
- **Description**: What the issue is
- **Workaround**: If any
- **Status**: Open / Resolved

---

## KI-001 — No Tests for Parser Layer
- **Severity**: Medium
- **Description**: `SelectorEngine` and `SelectorParser` have no unit tests yet. Tests exist for `BaseScraper` but not the parser pipeline.
- **Workaround**: Manual verification via import checks.
- **Status**: Open

## KI-002 — Deferred Browser Features
- **Severity**: Low
- **Description**: Session management, proxy support, User-Agent rotation, screenshots, and multi-context support are intentionally deferred. These should not be implemented until a concrete scraper requires them.
- **Workaround**: N/A (by design)
- **Status**: Open (deferred)

## KI-003 — SelectorEngine `_extract_list` Has Unused Variable
- **Severity**: Low
- **Description**: In `selector_engine.py`, `_extract_list()` calls `locator.all()` storing to `elements` but doesn't use it (uses `all_text_contents()` instead).
- **Workaround**: The method works correctly; the unused variable is harmless.
- **Status**: Open
