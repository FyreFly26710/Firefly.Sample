---
name: common-git-issue
description: Handle GitHub issue-driven work. Use when an agent must read, refine, update, label, comment on, or execute against a GitHub issue as the source of truth.
---

# Common Git Issue

Use this skill as the entry point for GitHub issue work.

## GitHub Tooling

Use the GitHub CLI, `gh`, as the primary interface for issue work.
For issue reads and writes, use the GitHub helper.
The helper uses the matching GitHub App when shared credentials exist at `../github-apps/<agent-slug>/`.
If that folder is missing, the helper falls back to the current authenticated `gh` user.

Agent slugs:

- Codex: `codex-coder`
- ClaudeCode: `claudecode-coder`

Before GitHub operations, prefer:

```bash
gh auth status
gh repo view --json nameWithOwner,url,defaultBranchRef
```

For GitHub issue operations, use:

```bash
./.agents/scripts/with-github-app.sh <agent-slug> -- gh issue view <issue-number> --json number,title,body,labels,state,author,comments,assignees,milestone,projectItems,url
./.agents/scripts/with-github-app.sh <agent-slug> -- gh issue comment <issue-number> --body "..."
./.agents/scripts/with-github-app.sh <agent-slug> -- gh issue edit <issue-number> --add-label agent
```

Use `codex-coder` for Codex and `claudecode-coder` for ClaudeCode.

Use `gh issue view` and `gh issue comment` for issue reads and status writes through the wrapper.
Use `gh issue edit` for labels and issue body updates.
Use GraphQL through `gh api graphql` when REST or high-level `gh` commands do not expose enough detail.

Do not rely on browser-only GitHub workflows for automation.
If `gh` is unavailable or unauthenticated, stop and report the blocker.
Missing GitHub App credentials are not a blocker unless the task explicitly requires bot identity.

## Source Of Truth

The GitHub issue is the canonical task definition.
The maintainer-owned source section is `Dev Requirement`.

Developers may create an issue with only a title, or with a free-form body.
During `init`, preserve any existing free-form body by moving it under `Dev Requirement`.
After that, the developer should maintain only `Dev Requirement`.
Agents may update derived sections, but must not rewrite `Dev Requirement` unless the maintainer explicitly asks.

Every mode must start by fetching the full issue details and all issue comments, not only the latest comments.

Recommended commands:

```bash
./.agents/scripts/with-github-app.sh <agent-slug> -- gh issue view <issue-number> --json number,title,body,labels,state,author,comments,assignees,milestone,projectItems,url
./.agents/scripts/with-github-app.sh <agent-slug> -- gh issue view <issue-number> --comments
```

If the task references linked PRs, closing references, timeline events, or exact comment ids that are not available through `gh issue view`, use wrapped `gh api graphql` to fetch the missing data.

Extract:

- issue number
- issue title
- full issue body
- all issue comments
- current labels
- linked PRs or related issues
- dev requirement
- description
- goal
- scope
- acceptance criteria
- constraints

## Issue Body Contract

Use this section order when normalizing or updating an issue body:

```markdown
## Dev Requirement

Maintainer-owned request, notes, constraints, examples, links, or raw requirement text.

## Description

Agent-maintained summary of the request and relevant context.

## Goal

Agent-maintained one-sentence target outcome.

## Scope

Agent-maintained list of included and excluded areas.

## Acceptance Criteria

Agent-maintained checklist of observable completion criteria.

## Constraints

Agent-maintained constraints, risks, dependencies, and explicit non-goals.
```

Rules:

- `Dev Requirement` is the source material from the developer.
- `Description`, `Goal`, `Scope`, `Acceptance Criteria`, and `Constraints` are derived by the agent from the issue title, `Dev Requirement`, and all comments.
- `init` creates the structured body if it is missing.
- `reinit` refreshes the derived sections from `Dev Requirement` and all comments.
- `init` and `reinit` must not remove maintainer text.
- If the existing body is unstructured, move it verbatim under `Dev Requirement`.
- If `Dev Requirement` already exists, keep it intact and update only derived sections.
- If comments change the requirement, reflect the interpretation in derived sections and mention the source comment in the status comment when useful.

## Modes

Dev or another trusted coordinator may trigger the agent with one of these modes.

- `init`: fetch full issue details and all comments, ensure labels, inspect relevant docs, create or refresh the structured issue body, prepare branch/worktree when useful, and do not edit implementation files.
- `reinit`: fetch full issue details and all comments, ensure labels, refresh the derived sections from `Dev Requirement` and comments, and do not code unless explicitly asked.
- `plan`: write or update an implementation plan in the issue. Do not code.
- `code`: implement the issue on the issue branch, validate, push, and prepare review.
- `merge`: create or update the PR and merge only when the workflow and maintainer instruction allow it.

If the mode is missing, infer conservatively from the prompt and issue state.
When unsure, do `init` or `plan`, not `code`.

## Status Comments

Keep GitHub visible as the durable work log.

Use concise comments for:

- `in progress`: the agent has picked up the issue and states the branch/session context.
- `blocked`: the agent cannot continue without clarification, access, failing dependency, or a decision.
- `ready for review`: implementation and validation are complete enough for maintainer review.

Do not send large implementation details only to chat or an external coordinator.
Write durable status to GitHub so the maintainer can review remotely.
In pair-work mode, also respond to Dev in chat with the same status, branch/worktree path, validation result, and next action.

## Labels

Every mode must inspect current labels and ensure workflow labels are correct before continuing.

When labels are available, keep these aligned:

- always keep `agent` on agent-assisted issues
- optionally keep a runtime label such as `codex` or `claudecode` when the repository uses runtime-specific labels
- default to `agent-only` for agent-assisted issues
- use `co-op` only when Dev explicitly requests collaborative pair work
- keep `agent-only` and `co-op` mutually exclusive
- use exactly one current state label: `in-progress`, `blocked`, or `ready-for-review`

Recommended mode-to-label behavior:

- `init`: add `agent` and `agent-only`; remove `co-op`; do not add a state label unless the run starts active work that needs tracking.
- `reinit`: add `agent` and `agent-only`; remove `co-op`; preserve the current state label unless the issue becomes blocked.
- `plan`: add `agent`, `agent-only`, and `in-progress`; remove `co-op`, `blocked`, and `ready-for-review`.
- `code`: add `agent`, `agent-only`, and `in-progress`; remove `co-op`, `blocked`, and `ready-for-review`.
- `merge`: add `agent` and `agent-only`; remove `co-op`; keep or set the state based on merge readiness.
- explicit co-op request: add `agent` and `co-op`; remove `agent-only`; then apply the requested state label.
- blocked in any mode: add `blocked`; remove `in-progress` and `ready-for-review`.
- ready for review: add `ready-for-review`; remove `in-progress` and `blocked`.

If label operations fail, continue and mention the failure in the issue status comment or final summary.

Preferred commands:

```bash
./.agents/scripts/with-github-app.sh <agent-slug> -- gh issue edit <issue-number> --add-label agent --add-label agent-only --remove-label co-op
./.agents/scripts/with-github-app.sh <agent-slug> -- gh issue edit <issue-number> --add-label in-progress --remove-label blocked --remove-label ready-for-review
./.agents/scripts/with-github-app.sh <agent-slug> -- gh issue edit <issue-number> --add-label blocked --remove-label in-progress --remove-label ready-for-review
./.agents/scripts/with-github-app.sh <agent-slug> -- gh issue edit <issue-number> --add-label ready-for-review --remove-label in-progress --remove-label blocked
./.agents/scripts/with-github-app.sh <agent-slug> -- gh issue edit <issue-number> --add-label co-op --remove-label agent-only
```

If a label does not exist, create it when the repository permissions allow it, or report the missing label as setup work.

## Branch And Worktree Rules

For implementation work, use:

`issue-<number>-<short-kebab-title>`

Create or reuse a git worktree for issue work:

```bash
mkdir -p worktrees
git worktree add worktrees/<branch-name> <branch-name>
```

Work inside `worktrees/<branch-name>` for issue implementation.
Commit and push before ending every implementation chat so Dev can review progress remotely.

Do not use PR numbers as work item ids.
The issue number remains the canonical id.

## Pair-Work Mode

Pair-work mode runs the same issue modes and GitHub workflow, with Dev directly coordinating the agent in chat.

In pair-work mode:

- Dev provides the project, issue number, and mode directly in chat.
- The agent still fetches full issue details and all comments first.
- The agent still updates labels, issue body, comments, branch, worktree, commits, pushes, and PRs.
- The agent also responds in chat with concise progress and blockers.
- GitHub remains the durable source of truth, while chat is the immediate collaboration channel.

## Blocking Rules

Block instead of guessing when:

- the goal is unclear
- acceptance criteria are missing for a risky change
- the requested scope conflicts with repository rules
- credentials, APIs, or external systems are unavailable
- implementation would require broad unrelated refactoring
