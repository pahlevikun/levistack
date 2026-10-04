#!/usr/bin/env python3
"""Scaffold a new use-case pack and append one row to references/registry.json."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = SKILL_ROOT / "references" / "registry.json"
TEMPLATE = SKILL_ROOT / "references" / "_template" / "usecase" / "pack.md"
USECASE_ROOT = SKILL_ROOT / "references" / "usecases"


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def save_registry(registry: dict) -> None:
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def scaffold(usecase_id: str, aliases: list[str], status: str = "validated", default_register: str = "santai") -> None:
    if not usecase_id.replace("-", "").isalnum():
        raise SystemExit(f"Invalid use case id: {usecase_id}")
    dest_dir = USECASE_ROOT / usecase_id
    if dest_dir.exists():
        raise SystemExit(f"Use case folder already exists: {dest_dir}")
    dest_dir.mkdir(parents=True)
    text = TEMPLATE.read_text(encoding="utf-8")
    text = text.replace("{usecase_id}", usecase_id).replace("{status}", status).replace("{default_register}", default_register)
    (dest_dir / "pack.md").write_text(text, encoding="utf-8")

    registry = load_registry()
    usecases = registry.setdefault("usecases", [])
    if any(entry.get("id") == usecase_id for entry in usecases):
        raise SystemExit(f"Use case id already in registry: {usecase_id}")
    usecases.append(
        {
            "id": usecase_id,
            "aliases": aliases,
            "status": status,
            "pack": f"references/usecases/{usecase_id}/pack.md",
            "default_register": default_register,
        }
    )
    save_registry(registry)
    print(f"Scaffolded {dest_dir / 'pack.md'} and registered {usecase_id} ({status}).")


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) < 1:
        print("Usage: python3 scripts/new_usecase.py <id> [alias1 alias2 ...]", file=sys.stderr)
        return 2
    usecase_id = args[0]
    aliases = args[1:] if len(args) > 1 else []
    scaffold(usecase_id, aliases)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
