#!/usr/bin/env python3
"""Keep dest; add keys/plugins that dest is missing from src."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def merge_missing(src, dest):
    if isinstance(src, dict) and isinstance(dest, dict):
        out = dict(dest)
        for key, val in src.items():
            if key not in out:
                out[key] = val
            else:
                out[key] = merge_missing(val, out[key])
        return out
    if isinstance(src, list) and isinstance(dest, list):
        seen = list(dest)
        for item in src:
            if item not in seen:
                seen.append(item)
        return seen
    return dest


def plugins_from(text: str) -> list[str]:
    match = re.search(r"plugins=\((.*?)\)", text, re.S)
    if not match:
        return []
    return [tok for tok in match.group(1).split() if tok and not tok.startswith("#")]


def union_zshrc_plugins(src_text: str, dest_text: str) -> str:
    src_plugins = plugins_from(src_text)
    dest_plugins = plugins_from(dest_text)
    if not src_plugins:
        return dest_text
    seen = list(dest_plugins)
    for name in src_plugins:
        if name not in seen:
            seen.append(name)
    if seen == dest_plugins:
        return dest_text
    block = "plugins=(\n" + "".join(f"  {name}\n" for name in seen) + ")"
    if re.search(r"plugins=\((.*?)\)", dest_text, re.S):
        return re.sub(r"plugins=\((.*?)\)", block, dest_text, count=1, flags=re.S)
    return dest_text.rstrip() + "\n\n" + block + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 4 or argv[1] not in {"json", "zshrc-plugins"}:
        print("usage: upsert.py json|zshrc-plugins SRC DEST", file=sys.stderr)
        return 2
    kind, src_path, dest_path = argv[1], Path(argv[2]), Path(argv[3])
    src = src_path.read_text(encoding="utf-8")
    dest = dest_path.read_text(encoding="utf-8") if dest_path.exists() else ""
    if kind == "json":
        src_obj = json.loads(src)
        dest_obj = json.loads(dest) if dest.strip() else {}
        merged = merge_missing(src_obj, dest_obj)
        dest_path.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
        return 0
    dest_path.write_text(union_zshrc_plugins(src, dest), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
