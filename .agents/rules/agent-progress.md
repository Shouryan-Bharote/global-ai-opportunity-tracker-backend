---
trigger: always_on
description: Rules for tracking and reporting development progress.
---

## Agent Progress

Rules:
- After completing any code changes, update `.state/DEVELOPMENT_STATUS.md` with what was done.
- After completing a phase milestone, update `.state/CURRENT_PHASE.md` and `context.md`.
- Log all architectural decisions in `.state/DECISIONS.md`.
- Log any discovered bugs or known issues in `.state/KNOWN_ISSUES.md`.
- When starting a new task, check `.state/TASK_QUEUE.md` for pending items.
- When completing a task, mark it done in `.state/TASK_QUEUE.md`.
- Read `.state/CURRENT_CONTEXT.md` at the start of every session for project orientation.
