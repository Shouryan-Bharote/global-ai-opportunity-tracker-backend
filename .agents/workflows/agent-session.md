---
name: agent-session
description: Workflow for starting a new agent coding session
---

# Workflow: Agent Session Startup

Follow this procedure at the start of every new coding session:

## Step 1: Read Current Context
Read `.state/CURRENT_CONTEXT.md` to understand the project state.

## Step 2: Check Current Phase
Read `.state/CURRENT_PHASE.md` for the active phase and its sub-tasks.

## Step 3: Check Task Queue
Read `.state/TASK_QUEUE.md` for pending work items.

## Step 4: Check Known Issues
Scan `.state/KNOWN_ISSUES.md` for blockers or gotchas.

## Step 5: Review Recent Decisions
Scan `.state/DECISIONS.md` for recent architectural decisions.

## Step 6: Begin Work
Start implementing the next task from the queue or address user request.

## Step 7: Update State
After completing work, update:
- `.state/DEVELOPMENT_STATUS.md`
- `.state/TASK_QUEUE.md`
- `.state/CURRENT_PHASE.md` (if milestone reached)
- `context.md` (if phase status changed)
