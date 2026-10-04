"""Shared loaders for registry and fictional catalogs."""

from __future__ import annotations

import json
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = SKILL_ROOT / "references" / "registry.json"
FICTIONAL_CATALOG_PATH = SKILL_ROOT / "references" / "fictional-catalog.json"


def load_registry(path: Path | None = None) -> dict:
    return json.loads((path or REGISTRY_PATH).read_text(encoding="utf-8"))


def load_fictional_catalog(path: Path | None = None) -> dict:
    return json.loads((path or FICTIONAL_CATALOG_PATH).read_text(encoding="utf-8"))


def fictional_fixture_ids(catalog: dict | None = None, path: Path | None = None) -> set[str]:
    data = catalog if catalog is not None else load_fictional_catalog(path)
    return {fixture["id"] for fixture in data.get("fixtures", [])}
