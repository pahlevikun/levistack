#!/usr/bin/env bash
# List pending draft notes on a GitLab MR (author's unpublished comments).
set -euo pipefail

[ "$#" -eq 3 ] || {
  echo "usage: $0 <repo> <project_id> <mr_number>" >&2
  exit 1
}
repo="$1" project_id="$2" mr="$3"

glab api "/projects/${project_id}/merge_requests/${mr}/draft_notes" --repo "$repo" \
  | jq '[.[] | {id, author: .author.username, created_at, resolved, note: .note[0:120]}]'
