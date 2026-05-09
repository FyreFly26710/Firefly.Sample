---
name: backend-tdd
description: Implement backend behavior with focused tests first or alongside the change. Use when server-side behavior, APIs, persistence, validation, or integration contracts are changed.
---

# Backend TDD

Use this skill for backend behavior changes.

## Read First

- root `AGENTS.md`
- `src/server/AGENTS.md`
- relevant backend docs
- existing tests for the touched area

## Test Strategy

- Start from the behavior described in the issue acceptance criteria.
- Prefer focused tests that fail for the missing behavior.
- Keep tests close to the owning service or module.
- Cover regression risk when fixing a bug.
- Avoid broad snapshot or fixture churn.
- Use integration tests when boundaries, persistence, auth, or external contracts are the point of the change.

## Implementation Rules

- Keep API contracts explicit.
- Keep validation and error behavior intentional.
- Keep persistence changes scoped to the owning area.
- Do not add infrastructure or messaging complexity unless the issue needs it.
- Keep test data readable and minimal.

## Finish

Before handoff:

- run relevant backend tests or explain why not
- summarize changed behavior
- note any migration, configuration, or deployment impact

