#!/usr/bin/env python3
"""Look up a language name, alias, or region in registry.json and fictional-catalog.json."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

from catalog import load_fictional_catalog, load_registry

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REGISTRY = SCRIPT_DIR.parent / "references" / "registry.json"
DEFAULT_FICTIONAL = SCRIPT_DIR.parent / "references" / "fictional-catalog.json"
LEGACY_REGISTRY = SCRIPT_DIR.parent / "references" / "languages" / "languages.json"


def normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    without_marks = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    lowered = without_marks.casefold()
    return re.sub(r"[^a-z0-9]+", " ", lowered).strip()


def load_languages(registry_path: Path | None = None) -> list[dict]:
    registry = load_registry(registry_path or DEFAULT_REGISTRY)
    return registry.get("languages", [])


def load_fictional_fixtures(catalog_path: Path | None = None) -> list[dict]:
    catalog = load_fictional_catalog(catalog_path or DEFAULT_FICTIONAL)
    return catalog.get("fixtures", [])


def find_languages(languages: list[dict], query: str, limit: int = 12) -> list[dict]:
    needle = normalize(query)
    if not needle:
        return []

    scored: list[tuple[int, int, dict]] = []
    for index, language in enumerate(languages):
        primary = [normalize(item) for item in [language["id"], language["name"], *language.get("aliases", [])]]
        locations = [normalize(item) for item in language.get("macroregions", []) + language.get("provinces", [])]
        score = 99
        if needle in primary:
            score = 0
        elif any(value.startswith(needle) for value in primary):
            score = 1
        elif any(needle in value for value in primary):
            score = 2
        elif locations and needle in locations:
            score = 3
        elif locations and any(needle in value for value in locations):
            score = 4
        if score < 99:
            scored.append((score, index, language))

    scored.sort(key=lambda item: (item[0], item[1]))
    return [item[2] for item in scored[:limit]]


def find_fictional_fixtures(fixtures: list[dict], query: str, limit: int = 12) -> list[dict]:
    needle = normalize(query)
    if not needle:
        return []

    scored: list[tuple[int, int, dict]] = []
    for index, fixture in enumerate(fixtures):
        primary = [normalize(item) for item in [fixture["id"], fixture["name"], *fixture.get("aliases", [])]]
        score = 99
        if needle in primary:
            score = 0
        elif any(value.startswith(needle) for value in primary):
            score = 1
        elif any(needle in value for value in primary):
            score = 2
        if score < 99:
            scored.append((score, index, fixture))

    scored.sort(key=lambda item: (item[0], item[1]))
    return [item[2] for item in scored[:limit]]


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    query = " ".join(args).strip()
    if not query:
        print(
            "Usage: python3 scripts/find_language.py <name|alias|region>",
            file=sys.stderr,
        )
        return 2

    languages = load_languages()
    results = find_languages(languages, query)
    if not results:
        fixtures = load_fictional_fixtures()
        results = find_fictional_fixtures(fixtures, query)
        if not results:
            print(f"No registry or fictional-catalog match for: {query}")
            return 0
        for fixture in results:
            aliases = fixture.get("aliases") or []
            alias_bit = f"; alias: {', '.join(aliases)}" if aliases else ""
            status = fixture.get("status", "")
            print(
                f"{fixture['id']}\t{fixture['name']}\tfictional {status}\t"
                f"{fixture.get('purpose', 'honesty-eval')}{alias_bit}"
            )
        return 0

    for language in results:
        aliases = language.get("aliases") or []
        alias_bit = f"; alias: {', '.join(aliases)}" if aliases else ""
        provinces = language.get("provinces") or []
        macroregions = language.get("macroregions") or []
        locations = ", ".join(provinces if provinces else macroregions)
        location_bit = f"\t{locations}" if locations else "\t"
        umbrella = "umbrella " if language.get("umbrella") else ""
        status = language.get("support", {}).get("status", "")
        print(f"{language['id']}\t{language['name']}\t{umbrella}{status}{location_bit}{alias_bit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
