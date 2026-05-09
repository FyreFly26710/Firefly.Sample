#!/usr/bin/env bash

set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <agent-slug> [owner/repo] -- <command...>" >&2
  echo "Example: $0 codex-coder -- gh issue comment 114 --body 'Hello'" >&2
  echo "Example: $0 codex-coder owner/repo -- gh issue view 114 --repo owner/repo" >&2
  exit 1
fi

agent_slug="$1"
shift 1

repo_slug=""

if [[ "$1" != "--" ]]; then
  repo_slug="$1"
  shift 1
fi

if [[ $# -lt 2 || "$1" != "--" ]]; then
  echo "Expected '--' before the command to run." >&2
  exit 1
fi

shift 1

repo_root="$(git rev-parse --show-toplevel)"
repo_parent="$(dirname "$repo_root")"
shared_app_dir="$repo_parent/github-apps/$agent_slug"
app_info_path="$shared_app_dir/app-info.json"

if [[ ! -f "$app_info_path" ]]; then
  echo "GitHub App credentials not found at $app_info_path; using current gh user auth." >&2
  "$@"
  exit $?
fi

token_cmd=("$repo_root/.agents/scripts/github-app-token.sh" "$agent_slug")

if [[ -n "$repo_slug" ]]; then
  token_cmd+=("$repo_slug")
fi

app_token="$("${token_cmd[@]}")"

GH_TOKEN="$app_token" \
GITHUB_TOKEN="$app_token" \
"$@"

