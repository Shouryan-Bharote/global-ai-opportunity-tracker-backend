# Phase 0: Research and Architecture

## Status: ✅ COMPLETED

## Objective
Define the technology stack, high-level architecture, and modular design for the Global AI Opportunity Tracker backend.

## Deliverables
- Technology selection: Python 3.13+, Patchright, LiteLLM, Poetry, Pydantic v2+
- Architectural principles: Downward-only dependencies, composition over inheritance, SRP
- Layer definitions: Browser Engine → Scraper Framework → Parsers → LLM Pipeline → Exporters → Database → API
- Target platforms identified: Unstop, Hack2Skill, Devpost, Kaggle

## Key Decisions
1. **Patchright over Playwright**: Patchright chosen for enhanced stealth and anti-detection.
2. **LiteLLM for LLM orchestration**: Provider-agnostic abstraction supporting Gemini, Groq, OpenRouter.
3. **Composition over Inheritance**: Classes own components rather than inheriting them.
4. **Explicit Contracts**: Separate data models for each layer boundary (e.g., `RawOpportunity` vs `ParsedOpportunity`).

## Files Created
- Project Context Blueprint document
- Initial `context.md`
