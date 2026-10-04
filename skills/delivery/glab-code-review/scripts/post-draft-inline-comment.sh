#!/usr/bin/env bash
# Post an inline draft note on a GitLab MR (visible only to you until published).
set -euo pipefail

[ "$#" -eq 9 ] || {
  echo "usage: $0 <repo> <project_id> <mr_number> <file_path> <line_number> <base_sha> <start_sha> <head_sha> <body_file>" >&2
  exit 1
}
repo="$1" project_id="$2" mr="$3" file="$4" line="$5"
base_sha="$6" start_sha="$7" head_sha="$8" body_file="$9"

jq -n --rawfile note "$body_file" \
  --arg base_sha "$base_sha" --arg start_sha "$start_sha" --arg head_sha "$head_sha" \
  --arg path "$file" --argjson line "$line" \
  '{note: $note, position: {base_sha: $base_sha, start_sha: $start_sha, head_sha: $head_sha,
    position_type: "text", new_path: $path, new_line: $line}}' \
  | glab api -X POST "/projects/${project_id}/merge_requests/${mr}/draft_notes" --repo "$repo" --input -
