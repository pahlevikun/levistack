#!/usr/bin/env python3
"""Scaffold a new language pack and append one row to references/registry.json."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = SKILL_ROOT / "references" / "registry.json"
TEMPLATE_ROOT = SKILL_ROOT / "references" / "_template" / "language"
LANG_ROOT = SKILL_ROOT / "references" / "languages"


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def save_registry(registry: dict) -> None:
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def scaffold(lang_id: str, name: str, iso: str = "", status: str = "validated") -> None:
    if not lang_id.replace("-", "").isalnum():
        raise SystemExit(f"Invalid language id: {lang_id}")
    dest = LANG_ROOT / lang_id
    if dest.exists():
        raise SystemExit(f"Language folder already exists: {dest}")

    shutil.copytree(TEMPLATE_ROOT, dest)
    replacements = {
        "{language_id}": lang_id,
        "{language_name}": name,
        "{status}": status,
        "{overlay_id}": "example",
        "{overlay_type}": "regional",
    }
    for path in dest.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for key, value in replacements.items():
            text = text.replace(key, value)
        path.write_text(text, encoding="utf-8")
    overlay_example = dest / "overlays" / "_overlay.md"
    if overlay_example.exists():
        overlay_example.unlink()

    registry = load_registry()
    languages = registry.setdefault("languages", [])
    if any(entry.get("id") == lang_id for entry in languages):
        raise SystemExit(f"Language id already in registry: {lang_id}")
    languages.append(
        {
            "id": lang_id,
            "iso": iso,
            "name": name,
            "aliases": [],
            "umbrella": False,
            "support": {
                "status": status,
                "pack": f"references/languages/{lang_id}/pack.md",
            },
            "registers": ["baku", "profesional", "santai"],
            "speech_levels": [],
            "overlays": [],
        }
    )
    save_registry(registry)
    print(f"Scaffolded {dest} and registered {lang_id} ({status}).")


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) < 2:
        print("Usage: python3 scripts/new_language.py <id> <Name> [iso] [status]", file=sys.stderr)
        return 2
    lang_id, name = args[0], args[1]
    iso = args[2] if len(args) > 2 else ""
    status = args[3] if len(args) > 3 else "validated"
    scaffold(lang_id, name, iso=iso, status=status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
