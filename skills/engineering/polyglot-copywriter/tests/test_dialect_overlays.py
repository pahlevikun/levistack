#!/usr/bin/env python3
"""Tests for regional dialect overlays in polyglot-copywriter registry."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = SKILL_ROOT / "references" / "registry.json"


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


class DialectOverlayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry()
        cls.languages = {lang["id"]: lang for lang in cls.registry["languages"]}

    def test_every_overlay_file_exists(self) -> None:
        for language in self.registry["languages"]:
            for overlay in language.get("overlays", []):
                rel = overlay["file"]
                path = SKILL_ROOT / rel
                self.assertTrue(
                    path.is_file(),
                    f"{language['id']} overlay {overlay['id']}: missing {rel}",
                )

    def test_no_duplicate_overlay_ids_per_language(self) -> None:
        for language in self.registry["languages"]:
            overlay_ids = [overlay["id"] for overlay in language.get("overlays", [])]
            self.assertEqual(
                len(overlay_ids),
                len(set(overlay_ids)),
                f"{language['id']}: duplicate overlay ids {overlay_ids}",
            )

    def test_japanese_has_kansai_and_tokyo(self) -> None:
        japanese = self.languages["japanese"]
        overlay_ids = {o["id"] for o in japanese.get("overlays", [])}
        self.assertIn("kansai", overlay_ids)
        self.assertIn("tokyo", overlay_ids)

    def test_japanese_kansai_overlay_is_regional(self) -> None:
        japanese = self.languages["japanese"]
        kansai = next(o for o in japanese["overlays"] if o["id"] == "kansai")
        self.assertEqual(kansai["type"], "regional")
        self.assertEqual(kansai["status"], "validated")

    def test_new_regional_overlays_have_type_regional_or_slang_or_mix(self) -> None:
        allowed = {"regional", "slang", "mix"}
        for language in self.registry["languages"]:
            for overlay in language.get("overlays", []):
                self.assertIn(
                    overlay["type"],
                    allowed,
                    f"{language['id']}/{overlay['id']}: invalid type {overlay['type']}",
                )

    def test_dialect_coverage_doc_exists(self) -> None:
        path = SKILL_ROOT / "references" / "dialect-coverage.md"
        self.assertTrue(path.is_file(), "missing references/dialect-coverage.md")


if __name__ == "__main__":
    unittest.main()
