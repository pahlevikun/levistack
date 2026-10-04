#!/usr/bin/env python3
"""Unit tests for polyglot-copywriter README.md."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
README_PATH = SKILL_ROOT / "README.md"
REGISTRY_PATH = SKILL_ROOT / "references" / "registry.json"


class ReadmeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_readme_exists(self) -> None:
        self.assertTrue(README_PATH.is_file())

    def test_contains_required_keywords(self) -> None:
        lowered = self.readme.casefold()
        self.assertIn("languages", lowered)
        self.assertIn("use cases", lowered)
        has_validate = (
            "validate_skill" in lowered
            or "python3 scripts/validate_skill.py" in self.readme
        )
        self.assertTrue(has_validate, "README must mention validate_skill or its command")

    def test_language_count_matches_registry(self) -> None:
        registry_count = len(self.registry["languages"])
        table_match = re.search(r"\|\s*Languages(?:\s*\(real\))?\s*\|\s*(\d+)\s*\|", self.readme)
        self.assertIsNotNone(table_match, "README missing | Languages | N | table row")
        self.assertEqual(int(table_match.group(1)), registry_count)


if __name__ == "__main__":
    unittest.main()
