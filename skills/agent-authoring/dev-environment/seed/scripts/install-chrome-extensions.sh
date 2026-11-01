#!/usr/bin/env bash
# Chrome has no official CLI installer. Open the Web Store page for each ID.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TSV="$ROOT/snapshots/chrome-extensions.tsv"

echo "Opening Chrome Web Store pages. Click Add to Chrome for each."
tail -n +2 "$TSV" | while IFS=$'\t' read -r id _ver name; do
  [[ -z "$id" ]] && continue
  url="https://chrome.google.com/webstore/detail/${id}"
  echo "$name  $url"
  open "$url"
done
