# Firefly Agent Templates

This repository is a starter template for projects that use GitHub issues and agent-assisted development.

## Intent

- Keep project-specific guidance close to the code.
- Keep reusable agent workflow skills in `.agents/skills`.
- Use GitHub issues as the source of truth for task scope.
- Let Dev coordinate directly with Codex or ClaudeCode in pair-work mode.
- Let agents implement focused issue branches and prepare pull requests.
- Keep `docs/` project-facing, like PRD, architecture, and development planning docs.

## Structure

- `AGENTS.md` contains generic repository guidance.
- `.agents/skills/` contains reusable workflow skills.
- `.github/` contains the pull request template.
- `.agents/scripts/` contains GitHub App helper wrappers for agent bot identity, with fallback to the current `gh` user when app credentials are missing.
- `src/client/web/AGENTS.md` is the placeholder for web-specific guidance.
- `src/server/AGENTS.md` is the placeholder for backend-specific guidance.
- `docs/` contains project-facing product, architecture, and development planning docs.

## Project Setup

After creating a new project from this template:

1. Replace placeholder project names and repository URLs.
2. Fill in `src/client/web/AGENTS.md` with the chosen frontend stack.
3. Fill in `src/server/AGENTS.md` with the chosen backend stack.
4. Add product docs and architecture docs under `docs/`.
5. Optionally configure shared GitHub App files under `../github-apps/<agent-slug>/`.
6. Create GitHub issues freely. Title-only issues are valid; `init` will structure the issue body.
