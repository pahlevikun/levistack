#!/usr/bin/env bash
# Restore Cursor / VS Code extensions from snapshots/vscode-extensions.txt
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

install_one() {
  local bin="$1"
  local ext="$2"
  if command -v "$bin" >/dev/null 2>&1; then
    "$bin" --install-extension "$ext"
  else
    echo "skip: $bin not on PATH ($ext)"
  fi
}

while read -r line; do
  [[ -z "$line" || "$line" == \#* ]] && continue
  ext="${line%%@*}"
  install_one cursor "$ext"
  install_one code "$ext"
done < "$ROOT/snapshots/vscode-extensions.txt"
