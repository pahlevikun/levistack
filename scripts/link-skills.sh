#!/usr/bin/env bash
# Dev helper: symlink every skills/<group>/<skill> into ~/.claude/skills and ~/.agents/skills.
# Skips targets that already exist and are not symlinks, so it never clobbers real installs.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
for target in "$HOME/.claude/skills" "$HOME/.agents/skills"; do
  mkdir -p "$target"
  for skill in "$root"/skills/*/*/; do
    [ -f "$skill/SKILL.md" ] || continue
    name="$(basename "$skill")"
    dest="$target/$name"
    if [ -e "$dest" ] && [ ! -L "$dest" ]; then
      echo "skip (exists, not a symlink): $dest"
      continue
    fi
    ln -sfn "${skill%/}" "$dest"
    echo "linked: $dest"
  done
done
