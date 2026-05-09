---
name: web-architecture
description: Plan or modify web application structure, routing, state, API boundaries, testing, and build conventions. Use for web-client architecture and implementation decisions.
---

# Web Architecture

Use this skill for web client structure and implementation patterns.

## Read First

- root `AGENTS.md`
- `src/client/web/AGENTS.md`
- relevant docs under `docs/`
- existing package, routing, state, and test files

## Architecture Rules

- Keep entry points and route files thin.
- Keep feature-owned behavior inside feature folders.
- Keep API calls behind typed client modules.
- Prefer local component or feature state before global state.
- Keep shared components genuinely reusable.
- Avoid broad scaffolding before the feature needs it.
- Keep validation commands documented in the local `AGENTS.md`.

## Planning Guidance

When planning web work, identify:

- routes or screens affected
- state ownership
- API contracts needed
- user-visible states
- validation commands
- likely regression risks

