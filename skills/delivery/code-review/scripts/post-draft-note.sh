#!/usr/bin/env bash
# Post a general (non-inline) draft note on a GitLab MR.
set -euo pipefail

[ "$#" -eq 4 ] || {
  echo "usage: $0 <repo> <project_id> <mr_number> <body_file>" >&2
  exit 1
}
repo="$1" project_id="$2" mr="$3" body_file="$4"

jq -n --rawfile note "$body_file" '{note: $note}' \
  | glab api -X POST "/projects/${project_id}/merge_requests/${mr}/draft_notes" --repo "$repo" --input -
