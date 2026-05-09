---
name: common-documentation-lookup
description: Find and read the repository guidance needed before planning or editing. Use when Codex needs to understand project docs, AGENTS.md files, architecture notes, PRD material, or local conventions before acting.
---

# Common Documentation Lookup

Use this skill before planning or implementation when the task depends on repository context.

## Read Order

1. Root `AGENTS.md`.
2. The nearest child `AGENTS.md` for each touched area.
3. The full GitHub issue body and all comments when the task is issue-driven.
4. Relevant docs under `docs/`.
5. Relevant README files near the touched code.
6. External library or framework documentation when local docs are insufficient.

## Lookup Rules

- Prefer local repository docs over assumptions.
- Prefer the most specific `AGENTS.md` that applies to the files being changed.
- If docs conflict, call out the conflict and use the most local guidance unless a root workflow rule applies.
- If required docs are missing, continue with existing code patterns and note the documentation gap.
- Do not bulk-read unrelated docs; read enough to make the current task safe.

## External Documentation

When external package, framework, or API behavior matters, prefer Context7 if it is configured in Codex on the server.
If Context7 is not configured, use official documentation through the available approved tooling or report that server setup is missing when fresh external docs are required.

Do not invent current library behavior from memory when version-sensitive docs are needed.

Current server expectation:

- `gh` should be used for GitHub issue and PR data.
- Context7 is optional but recommended for external library documentation once configured as a Codex MCP server.

## Output Expectations

When this skill is used for issue work, summarize:

- relevant project rules
- relevant area-specific rules
- docs that were read
- missing or ambiguous guidance

Keep the summary short enough to fit naturally in an issue comment, PR body, or final handoff.
