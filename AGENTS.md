# AI Agent Workspace Rules

## Read Before Anything Else
1. `AGENTS.md` (This file)
2. `memory.md` (For cross-session state)

## Core Rules
- Never use hardcoded absolute paths when relative workspace paths work.
- Always verify tool outputs before moving to the next step.
- If an execution fails, use systematic debugging rather than random guessing.
