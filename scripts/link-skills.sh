#!/usr/bin/env bash
# Dev helper: symlink the catalog into local agent tools. Every link points back at this repo, so a
# `git pull` updates every tool at once. Skips targets that exist and are not symlinks, so it never
# clobbers a real install.
#
#   ./scripts/link-skills.sh                 # Claude Code + ~/.agents (default, also read by Codex)
#   ./scripts/link-skills.sh --cursor        # Cursor: ~/.cursor/skills and ~/.cursor/agents
#   ./scripts/link-skills.sh --trae          # Trae: ~/.trae/{skills,agents,rules}
#   ./scripts/link-skills.sh --antigravity   # Antigravity app and IDE: ~/.gemini/config/plugins/levistack
#   ./scripts/link-skills.sh --all           # every target above
#   add --dry-run to print what would change
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"

claude=0 agents=0 cursor=0 trae=0 antigravity=0 dry=0
for arg in "$@"; do
  case "$arg" in
    --claude) claude=1 ;;
    --agents) agents=1 ;;
    --cursor) cursor=1 ;;
    --trae) trae=1 ;;
    --antigravity) antigravity=1 ;;
    --all) claude=1 agents=1 cursor=1 trae=1 antigravity=1 ;;
    --dry-run) dry=1 ;;
    -h|--help) sed -n '2,11p' "$0"; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done
if [ $((claude + agents + cursor + trae + antigravity)) -eq 0 ]; then claude=1 agents=1; fi

# link <source> <dest>: one symlink, never over a real file or folder.
link() {
  local src="$1" dest="$2"
  if [ -e "$dest" ] && [ ! -L "$dest" ]; then
    echo "skip (exists, not a symlink): $dest"
    return
  fi
  if [ "$dry" -eq 1 ]; then echo "would link: $dest -> $src"; return; fi
  mkdir -p "$(dirname "$dest")"
  ln -sfn "$src" "$dest"
  echo "linked: $dest"
}

# Skills are linked flat (one folder per skill), the layout every tool reads.
link_skills() {
  local target="$1" skill
  for skill in "$root"/skills/*/*/; do
    [ -f "$skill/SKILL.md" ] || continue
    link "${skill%/}" "$target/$(basename "$skill")"
  done
}

link_agents() {
  local target="$1" prefix="$2" agent
  for agent in "$root"/agents/*.md; do
    link "$agent" "$target/$prefix$(basename "$agent")"
  done
}

# Only the always-on core rules: the same set the session-start hook injects.
link_core_rules() {
  local target="$1" prefix="$2" rule
  for rule in "$root"/rules/core/*.md; do
    grep -q '^alwaysApply: true' "$rule" || continue
    link "$rule" "$target/$prefix$(basename "$rule")"
  done
}

if [ "$claude" -eq 1 ]; then link_skills "$HOME/.claude/skills"; fi
if [ "$agents" -eq 1 ]; then link_skills "$HOME/.agents/skills"; fi

# Cursor reads personal skills from ~/.cursor/skills. Rules come with the Cursor plugin, not from here.
if [ "$cursor" -eq 1 ]; then
  link_skills "$HOME/.cursor/skills"
  link_agents "$HOME/.cursor/agents" "levistack-"
fi

if [ "$trae" -eq 1 ]; then
  link_skills "$HOME/.trae/skills"
  link_agents "$HOME/.trae/agents" "levistack-"
  link_core_rules "$HOME/.trae/rules" "levistack-"
fi

if [ "$antigravity" -eq 1 ]; then
  plugin="$HOME/.gemini/config/plugins/levistack"
  link "$root/plugin.json" "$plugin/plugin.json"
  link_skills "$plugin/skills"
  link_agents "$plugin/agents" ""
  link_core_rules "$plugin/rules" ""
fi
