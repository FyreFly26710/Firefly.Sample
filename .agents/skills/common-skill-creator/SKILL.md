---
name: common-skill-creator
description: Create or update repository-local agent skills under .agents/skills using the repository naming convention. Use when a project needs a new reusable workflow, architecture, or delivery skill.
---

# Common Skill Creator

Use this skill when adding or updating a local skill.

## Location

Skills live at:

`.agents/skills/<scope>-<skill-desc>/SKILL.md`

Use lowercase kebab-case names.

## Scope Prefixes

- `common-`: repository-wide workflow skills
- `agent-`: OpenClaw/Codex coordination skills
- `frontend-`: frontend delivery and design skills
- `web-`: web app architecture and implementation skills
- `backend-`: backend delivery and architecture skills
- `infra-`: deployment, CI, and runtime skills

## Skill Shape

Each skill should include frontmatter:

```yaml
---
name: scope-skill-desc
description: One sentence explaining when to use the skill.
---
```

Then include:

- purpose
- when to use
- required read order
- concrete rules
- expected output or handoff

## Quality Rules

- Keep skills operational, not aspirational.
- Put project-specific decisions in the project skill or local `AGENTS.md`, not in generic skills.
- Prefer short checklists over long essays.
- Avoid duplicating root `AGENTS.md` unless the skill needs an exact workflow rule.
- Update `AGENTS.md` if adding a new stable naming convention.

