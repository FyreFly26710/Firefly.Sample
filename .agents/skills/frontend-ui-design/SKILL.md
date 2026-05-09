---
name: frontend-ui-design
description: Design or refine frontend UI behavior, layout, visual hierarchy, accessibility, and interaction states for a project. Use when planning or implementing user-facing frontend screens.
---

# Frontend UI Design

Use this skill for user-facing UI work.

## Required Context

Read:

- root `AGENTS.md`
- local frontend or web `AGENTS.md`
- relevant product or design docs
- the issue goal, scope, acceptance criteria, and constraints

## Design Rules

- Build the actual workflow first, not a marketing page, unless the issue asks for marketing content.
- Use existing component libraries, tokens, and patterns before inventing new ones.
- Include loading, empty, error, disabled, and success states where the workflow needs them.
- Keep layouts responsive and stable across desktop and mobile widths.
- Avoid UI text that explains implementation details.
- Keep controls recognizable: icons for common tools, toggles for binary settings, tabs for view switching, menus for option sets, sliders or inputs for numeric values.
- Do not add broad visual redesigns unless the issue requests them.

## Handoff

In the issue or PR summary, include:

- screens or components changed
- states covered
- validation performed
- assumptions or unresolved design questions

