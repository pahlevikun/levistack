#!/usr/bin/env bash
# First run: materialize the snapshot repo from this skill's seed.
# Upsert: create missing files, keep files already in the dest repo.
set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SEED="$SKILL_ROOT/seed"
DEST="${LAPTOP_SETUP_ROOT:-$HOME/laptop-setup}"

if [[ ! -d "$SEED" ]]; then
  echo "error: skill seed missing at $SEED" >&2
  exit 1
fi

mkdir -p "$DEST"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --ignore-existing \
    --exclude '.git/' \
    --exclude 'private/' \
    --exclude '.cursor/' \
    --exclude '.DS_Store' \
    "$SEED/" "$DEST/"
else
  (cd "$SEED" && find . -type f ! -path './.git/*' ! -path './private/*' -print0) |
    while IFS= read -r -d '' rel; do
      rel="${rel#./}"
      if [[ ! -e "$DEST/$rel" ]]; then
        mkdir -p "$DEST/$(dirname "$rel")"
        cp "$SEED/$rel" "$DEST/$rel"
      fi
    done
fi

chmod +x "$DEST/apply.sh" "$DEST/scripts/"*.sh "$DEST/scripts/"*.py 2>/dev/null || true

# Live $HOME layout (clone slots + zsh/cursor/agents). mkdir -p is upsert.
HOME_DIRS=""
for cand in "$SEED/structure/home-dirs.txt" "$SEED/snapshots/home-dirs.txt"; do
  [[ -f "$cand" ]] && HOME_DIRS="$cand" && break
done
if [[ -n "$HOME_DIRS" ]]; then
  while IFS= read -r rel || [[ -n "${rel:-}" ]]; do
    [[ -z "$rel" || "$rel" == \#* ]] && continue
    mkdir -p "$HOME/$rel" || true
  done < "$HOME_DIRS"
fi

if [[ ! -d "$DEST/.git" ]]; then
  git -C "$DEST" init --template= >/dev/null
  echo "initialized git repo at $DEST"
fi

echo "$DEST"
