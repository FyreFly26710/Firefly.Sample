# AGENTS.md

## Repository Role

This repository is designed for issue-driven agent collaboration.
GitHub issues define the requested work, and agents perform focused implementation work.

## Agent Modes

- Pair-work mode: Dev works directly with an agent on Dev's machine. Dev coordinates the work in chat, and the agent must respond in chat as well as update GitHub.

Use the same issue modes for issue-driven work: `init`, `reinit`, `plan`, `code`, and `merge`.
Use GitHub issues and PRs as the durable task log.

## GitHub Agent Bots

Agents should use the matching GitHub App bot for GitHub issue and pull request updates when shared app credentials are available.
If shared app credentials are not available, the helper falls back to the current authenticated `gh` user.

- Codex uses `codex-coder`.
- ClaudeCode uses `claudecode-coder`.

Use the local helper wrapper:

```bash
./.agents/scripts/with-github-app.sh <agent-slug> -- gh <...>
```

Examples:

```bash
./.agents/scripts/with-github-app.sh codex-coder -- gh issue comment 123 --body "..."
./.agents/scripts/with-github-app.sh claudecode-coder -- gh pr comment 123 --body "..."
```

Shared GitHub App files live beside project repositories at `../github-apps/<agent-slug>/`.
For a layout like `Repo/<project>`, this resolves to `Repo/github-apps/<agent-slug>/`.

## Core Principles

- Treat the GitHub issue as the source of truth for issue-driven work.
- Keep one issue mapped to one focused branch and one reviewable pull request.
- Prefer small, explicit changes over broad refactors.
- Follow local `AGENTS.md` files before introducing new conventions.
- Do not rename files, folders, APIs, or public contracts unless the issue requires it.
- Do not add dependencies unless the need is clear and documented.
- Keep assumptions visible in issue comments, PR summaries, or docs.
- Update docs when architecture, workflow, or delivery behavior changes materially.

## Repository Structure

- `.agents/skills/` contains reusable agent skills for issue handling, documentation lookup, PR work, planning, frontend work, and backend work.
- `.agents/scripts/` contains reusable agent helper scripts.
- `.github/` contains the pull request template.
- `src/client/web/` contains the web client area and its local `AGENTS.md`.
- `src/server/` contains the backend/server area and its local `AGENTS.md`.
- `docs/` contains project-facing product, architecture, and development planning documentation.

## Skill Naming Convention

Skills live under `.agents/skills/<scope>-<skill-desc>/SKILL.md`.

Use stable scope prefixes:

- `common-` for workflow and repository-wide skills.
- `frontend-` for general frontend work.
- `web-` for web-client architecture and implementation.
- `backend-` for server-side work.
- `agent-` for local agent coordination workflows.

Examples:

- `common-documentation-lookup`
- `common-git-issue`
- `common-git-pr`
- `frontend-ui-design`
- `web-architecture`
- `backend-tdd`
- `agent-pair-work-flow`

## Issue-Driven Workflow

For GitHub issue work:

1. Read the full issue details and all comments.
2. Read this file, relevant local `AGENTS.md` files, and relevant docs.
3. Ensure the workflow labels are correct.
4. If the issue is unclear, update derived issue sections or add a refinement comment before coding.
5. When implementation is requested, create or continue the issue branch and worktree.
6. Keep progress visible in GitHub issue or PR comments.
7. In pair-work mode, also respond clearly to Dev in chat.
8. Run relevant checks before handing work back.
9. Commit and push before ending any implementation chat.
10. Prepare a focused PR tied to the source issue.

Default issue delivery mode is `agent-only`.
Use `co-op` only when Dev explicitly requests collaborative pair work.
Keep `agent-only` and `co-op` mutually exclusive.

The agent and Dev should use the same branch, worktree, issue comments, labels, and PR rules for every issue.

## Branch And PR Rules

- Branch names should be `issue-<number>-<short-kebab-title>`.
- Issue worktrees should live at `worktrees/<branch-name>` when worktrees are used.
- PR titles should be `<type>(<scope>): <description> (#<issue-number>)`.
- PR bodies should include `Closes #<issue-number>` when the PR should close the issue.
- Use the source GitHub issue number as the canonical work item id.
- Do not use the PR number as a substitute for the issue number.

## Local Guidance

Child folders may define their own `AGENTS.md`.
When guidance conflicts, prefer the most specific `AGENTS.md` that applies to the files being changed, unless the root guidance defines a workflow rule.
