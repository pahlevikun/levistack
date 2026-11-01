#!/usr/bin/env bash
set -euo pipefail
# Re-clone git remotes recorded in snapshots/git-repos.tsv
ROOT="${CLONE_ROOT:-$HOME}"
while IFS=$'\t' read -r path origin branch head status; do
  [[ "$path" == path || "$path" == \#* ]] && continue
  [[ -z "${origin:-}" ]] && continue
  dest="$ROOT/$path"
  if [[ -d "$dest/.git" ]]; then
    echo "skip exists: $dest"
    continue
  fi
  mkdir -p "$(dirname "$dest")"
  echo "clone $origin -> $dest"
  git clone --filter=blob:none "$origin" "$dest"
done < "$(dirname "$0")/../snapshots/git-repos.tsv"

