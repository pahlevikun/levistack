#!/usr/bin/env bash
# Refresh laptop-setup snapshots from the live machine. Does not commit.
# Sanitizes token, key, and password values on copy.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="/opt/homebrew/bin:$HOME/.local/bin:$PATH"

log() { printf '\n==> %s\n' "$*"; }
note() { printf '    %s\n' "$*"; }

sanitize_text() {
  python3 - "$1" <<'PY'
import re, sys
from pathlib import Path
p = Path(sys.argv[1])
t = p.read_text(encoding="utf-8", errors="replace")
def keep_name(m):
    name = m.group(1)
    return f'export {name}="${{{name}:-}}"  # set in the environment; do not commit the value'
t = re.sub(r'export ([A-Za-z0-9_]*(?:TOKEN|KEY|SECRET|PASSWORD)[A-Za-z0-9_]*)="[^"$]+"', keep_name, t)
p.write_text(t, encoding="utf-8")
PY
}

copy_home() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  cp "$src" "$dest"
  sanitize_text "$dest"
}

log "zsh / Oh My Zsh"
copy_home "$HOME/.zshrc" "$REPO/home/.zshrc"
copy_home "$HOME/.oh-my-zsh/custom/dev-aliases.zsh" "$REPO/home/.oh-my-zsh/custom/dev-aliases.zsh"
copy_home "$HOME/.oh-my-zsh/custom/legacy-shortcuts.zsh" "$REPO/home/.oh-my-zsh/custom/legacy-shortcuts.zsh"
{
  for p in "$HOME/.oh-my-zsh/custom/plugins"/*; do
    [[ -d "$p/.git" ]] || continue
    echo "$(basename "$p") $(git -C "$p" remote get-url origin 2>/dev/null || true)"
  done
} > "$REPO/snapshots/omz-plugins.txt"

log "ssh / git (no private keys)"
copy_home "$HOME/.ssh/config" "$REPO/home/.ssh/config"
mkdir -p "$REPO/home/.ssh"
for pub in "$HOME/.ssh/"*.pub; do
  [[ -f "$pub" ]] || continue
  cp "$pub" "$REPO/home/.ssh/$(basename "$pub")"
done
[[ -f "$HOME/.ssh/known_hosts" ]] && cp "$HOME/.ssh/known_hosts" "$REPO/home/.ssh/known_hosts"
copy_home "$HOME/.gitconfig" "$REPO/home/.gitconfig"
copy_home "$HOME/.gitignore_global" "$REPO/home/.gitignore_global"

log "Cursor / VS Code extensions"
{
  echo "# Visual Studio Code.app is installed."
  echo "# Cursor \`cursor --list-extensions --show-versions\`"
  cursor --list-extensions --show-versions 2>/dev/null || true
} > "$REPO/snapshots/vscode-extensions.txt"

{
  echo "# ~/.cursor/plugins/local"
  ls -1 "$HOME/.cursor/plugins/local" 2>/dev/null || true
  echo
  echo "# ~/.cursor/plugins/cache (marketplace)"
  ls -1 "$HOME/.cursor/plugins/cache" 2>/dev/null || true
} > "$REPO/snapshots/cursor-plugins-local.txt"

log "Chrome extensions"
python3 - "$REPO/snapshots/chrome-extensions.tsv" <<'PY'
import json, sys
from pathlib import Path
out = Path(sys.argv[1])
root = Path.home() / "Library/Application Support/Google/Chrome/Default/Extensions"
rows = ["id\tversion\tname"]
if root.exists():
    for ext in sorted(root.iterdir()):
        if not ext.is_dir() or ext.name.startswith("."):
            continue
        vers = sorted(p for p in ext.iterdir() if p.is_dir() and not p.name.startswith("."))
        if not vers:
            continue
        man_path = vers[-1] / "manifest.json"
        name, ver = ext.name, vers[-1].name
        if man_path.exists():
            data = json.loads(man_path.read_text(encoding="utf-8", errors="replace"))
            name = data.get("name") or name
            ver = data.get("version") or ver
            loc = data.get("default_locale")
            if isinstance(name, str) and name.startswith("__MSG_"):
                key = name[6:-2]
                for cand in (loc, "en", "en_US"):
                    msgp = vers[-1] / "_locales" / cand / "messages.json" if cand else None
                    if msgp and msgp.exists():
                        msg = json.loads(msgp.read_text())
                        hit = msg.get(key) or msg.get(key.lower())
                        if hit and hit.get("message"):
                            name = hit["message"]
                            break
        rows.append(f"{ext.name}\t{ver}\t{name}")
out.write_text("\n".join(rows) + "\n")
PY

log "GUI apps"
ls /Applications | sort > "$REPO/snapshots/applications.txt"

log "Brewfile vscode lines from live Cursor"
python3 - "$REPO/Brewfile" <<'PY'
import pathlib, re, subprocess, sys
brewfile = pathlib.Path(sys.argv[1])
text = brewfile.read_text()
try:
    exts = subprocess.check_output(["cursor", "--list-extensions"], text=True, stderr=subprocess.DEVNULL).splitlines()
except Exception:
    raise SystemExit(0)
wanted = [f'vscode "{e.strip()}"' for e in exts if e.strip()]
existing = set(re.findall(r'^vscode "([^"]+)"', text, re.M))
to_add = [line for line in wanted if line.split('"')[1] not in existing]
if to_add:
    brewfile.write_text(text.rstrip() + "\n" + "\n".join(to_add) + "\n")
    print("added", to_add)
else:
    print("Brewfile vscode lines already current")
PY

log "refresh skill seed"
refresh_skill_seed() {
  local skill_dir="$1"
  local skill_seed="$skill_dir/seed"
  mkdir -p "$skill_seed"
  rsync -a --delete \
    --exclude '.git/' \
    --exclude 'private/' \
    --exclude '.cursor/' \
    --exclude '.DS_Store' \
    "$REPO/" "$skill_seed/"
}
if [[ -d "$REPO/.cursor/skills/dev-environment" ]]; then
  refresh_skill_seed "$REPO/.cursor/skills/dev-environment"
fi
if [[ -d "$REPO/.cursor/skills/mac-dev-workstation" ]]; then
  refresh_skill_seed "$REPO/.cursor/skills/mac-dev-workstation"
fi

log "done"
note "Review git diff. Do not commit private keys or tokens."
note "Commit only if the user asked."
