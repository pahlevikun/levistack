#!/usr/bin/env python3
"""Unit tests for technique index routing and locale file presence."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
TECHNIQUE_INDEX = SKILL_ROOT / "references" / "techniques" / "index.json"
LOCALES_DIR = SKILL_ROOT / "references" / "techniques" / "locales"
REGISTRY_PATH = SKILL_ROOT / "references" / "registry.json"

sys_path = SKILL_ROOT / "scripts"
if str(sys_path) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(sys_path))

from catalog import fictional_fixture_ids  # noqa: E402

SKIP_LOCALE_LANGUAGES = fictional_fixture_ids()


def load_technique_index() -> dict:
    return json.loads(TECHNIQUE_INDEX.read_text(encoding="utf-8"))


class TechniqueRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index = load_technique_index()

    def test_index_schema_version(self) -> None:
        self.assertEqual(self.index["schema_version"], 1)

    def test_all_indexed_files_exist(self) -> None:
        missing: list[str] = []
        for section in ("generic", "generic_usecase", "locales"):
            for entry in self.index.get(section, []):
                rel = entry.get("file")
                if not rel:
                    missing.append(f"{section}: entry missing file")
                    continue
                if not (SKILL_ROOT / rel).is_file():
                    missing.append(rel)
        self.assertFalse(missing, f"missing technique files: {missing}")

    def test_locale_files_on_disk_are_indexed(self) -> None:
        indexed = {
            Path(entry["file"]).name
            for entry in self.index.get("locales", [])
            if entry.get("file")
        }
        on_disk = {path.name for path in LOCALES_DIR.glob("*.md")}
        unindexed = sorted(on_disk - indexed)
        self.assertFalse(unindexed, f"locale files not in index.json: {unindexed}")

    def test_locale_entries_have_language_ids(self) -> None:
        for entry in self.index.get("locales", []):
            langs = entry.get("languages")
            self.assertIsInstance(langs, list, f"locale {entry.get('id')} missing languages")
            self.assertTrue(langs, f"locale {entry.get('id')} has empty languages")

    def test_every_language_has_locale_indexed(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        indexed_ids = {entry.get("id") for entry in self.index.get("locales", [])}
        missing: list[str] = []
        for lang in registry.get("languages", []):
            lang_id = lang["id"]
            if lang_id in SKIP_LOCALE_LANGUAGES:
                continue
            if lang_id not in indexed_ids:
                missing.append(lang_id)
        self.assertFalse(missing, f"languages without locale index entry: {missing}")


if __name__ == "__main__":
    unittest.main()
