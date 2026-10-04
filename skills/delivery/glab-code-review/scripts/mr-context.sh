#!/usr/bin/env bash
set -euo pipefail

[ "$#" -eq 2 ] || { echo "usage: $0 <repo> <mr_number>" >&2; exit 1; }
repo="$1" mr="$2"
project_id=$(glab api graphql -f query="query { project(fullPath: \"${repo}\") { id } }" \
  | jq -r '.data.project.id' | sed 's#gid://gitlab/Project/##')
refs=$(glab api "/projects/${project_id}/merge_requests/${mr}" --repo "$repo")
base_sha=$(jq -r '.diff_refs.base_sha' <<<"$refs")
start_sha=$(jq -r '.diff_refs.start_sha' <<<"$refs")
head_sha=$(jq -r '.diff_refs.head_sha' <<<"$refs")
printf 'PROJECT_ID=%s\nBASE_SHA=%s\nSTART_SHA=%s\nHEAD_SHA=%s\n' \
  "$project_id" "$base_sha" "$start_sha" "$head_sha"
