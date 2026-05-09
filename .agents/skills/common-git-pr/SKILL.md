---
name: common-git-pr
description: Prepare, update, review, or merge GitHub pull requests tied to source issues. Use when Codex is creating a PR, updating a PR body, responding to review comments, or finalizing an issue branch.
---

# Common Git PR

Use this skill for pull request work.

## GitHub Tooling

Use the GitHub CLI, `gh`, as the primary interface for PR work.
For PR reads and writes, use the GitHub helper.
The helper uses the matching GitHub App when shared credentials exist at `../github-apps/<agent-slug>/`.
If that folder is missing, the helper falls back to the current authenticated `gh` user.

Agent slugs:

- Codex: `codex-coder`
- ClaudeCode: `claudecode-coder`

Before PR operations, prefer:

```bash
gh auth status
gh repo view --json nameWithOwner,url,defaultBranchRef
```

For GitHub PR operations, use:

```bash
./.agents/scripts/with-github-app.sh codex-coder -- gh pr view <pr-number> --json number,title,body,state,url
./.agents/scripts/with-github-app.sh codex-coder -- gh pr comment <pr-number> --body "..."
./.agents/scripts/with-github-app.sh codex-coder -- gh pr create --title "..." --body-file <body-file>
```

Use `claudecode-coder` instead of `codex-coder` when the acting agent is ClaudeCode.

Use `gh pr view`, `gh pr create`, `gh pr edit`, `gh pr comment`, `gh pr checks`, `gh pr review`, and `gh pr merge` through the wrapper for PR work.
Use wrapped `gh api graphql` when thread-level review state, exact review comment ids, or timeline data are required.

If `gh` is unavailable or unauthenticated, stop and report the blocker.
Missing GitHub App credentials are not a blocker unless the task explicitly requires bot identity.

## PR Contract

One PR should normally map to one source issue.
The source issue number is the canonical work item id.

PR title format:

`<type>(<scope>): <description> (#<issue-number>)`

Allowed default types:

- `feat`
- `fix`
- `refactor`
- `test`
- `docs`
- `chore`
- `agent`

PR body should include:

`Closes #<issue-number>`

Use `Refs #<issue-number>` instead when the PR should not close the issue.

## Before Opening Or Updating A PR

- Confirm the branch belongs to the source issue.
- Confirm the branch is pushed.
- Confirm the PR is scoped to the issue.
- Run relevant validation or explain why validation could not be run.
- Summarize assumptions and risks.
- Link back to the source issue.

Preferred commands:

```bash
git -C worktrees/<branch> status --short
git -C worktrees/<branch> branch --show-current
git -C worktrees/<branch> push -u origin <branch>
./.agents/scripts/with-github-app.sh codex-coder -- gh pr view --json number,title,body,state,url,headRefName,baseRefName,reviewDecision,statusCheckRollup
./.agents/scripts/with-github-app.sh codex-coder -- gh pr create --draft --title "<type>(<scope>): <description> (#<issue-number>)" --body-file <body-file>
./.agents/scripts/with-github-app.sh codex-coder -- gh pr edit <pr-number> --body-file <body-file>
./.agents/scripts/with-github-app.sh codex-coder -- gh pr checks <pr-number>
```

## Review Comments

When responding to PR review comments:

- read the unresolved review comments and full issue context
- address actionable comments in focused commits
- do not rewrite unrelated code
- reply with what changed and what validation was run
- leave a clear note if a comment is intentionally not addressed

Prefer wrapped `gh api graphql` for unresolved review threads because plain `gh pr view` may not expose enough thread state.

## Merge Mode

Only merge when explicitly instructed by the maintainer or by a trusted OpenClaw mode that carries maintainer approval.

Before merge:

- ensure checks are passing or explicitly accepted
- ensure the PR still matches the source issue
- ensure the issue has a final status comment
- prefer squash merge unless the project docs say otherwise

Preferred command:

```bash
./.agents/scripts/with-github-app.sh codex-coder -- gh pr merge <pr-number> --squash --delete-branch
```

After merge, clean up from the main repo:

```bash
git checkout main
git fetch --prune
git worktree remove worktrees/<branch>
git branch -D <branch>
```
