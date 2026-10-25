#!/usr/bin/env bash
# Publish all pending draft notes on a GitLab MR (bulk_publish).
# Optional summary note and reviewer_state are passed as env vars:
#   SUMMARY_FILE  — path to markdown summary (optional)
#   REVIEWER_STATE — requested_changes | reviewed (optional; never use approved for bots)
#   INTERNAL      — true for internal-only summary note (optional)
set -euo pipefail

[ "$#" -eq 3 ] || {
  echo "usage: $0 <repo> <project_id> <mr_number>" >&2
  echo "  env: SUMMARY_FILE, REVIEWER_STATE, INTERNAL" >&2
  exit 1
}
repo="$1" project_id="$2" mr="$3"

args=()
if [ -n "${SUMMARY_FILE:-}" ] && [ -f "$SUMMARY_FILE" ]; then
  args+=(-f "note=$(cat "$SUMMARY_FILE")")
fi
if [ -n "${REVIEWER_STATE:-}" ]; then
  args+=(-f "reviewer_state=${REVIEWER_STATE}")
fi
if [ "${INTERNAL:-}" = "true" ]; then
  args+=(-f "internal=true")
fi

glab api -X POST "/projects/${project_id}/merge_requests/${mr}/draft_notes/bulk_publish" \
  --repo "$repo" "${args[@]}"
