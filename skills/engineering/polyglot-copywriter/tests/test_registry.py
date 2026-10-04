#!/usr/bin/env python3
"""Unit tests for polyglot-copywriter references/registry.json."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = SKILL_ROOT / "references" / "registry.json"


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


class RegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry()

    def test_schema_version_is_2(self) -> None:
        self.assertEqual(self.registry["schema_version"], 2)

    def test_every_language_is_validated(self) -> None:
        for language in self.registry["languages"]:
            status = language["support"]["status"]
            self.assertEqual(
                status,
                "validated",
                f"{language['id']}: expected validated, got {status}",
            )

    def test_every_language_pack_exists(self) -> None:
        for language in self.registry["languages"]:
            pack = language["support"]["pack"]
            path = SKILL_ROOT / pack
            self.assertTrue(path.is_file(), f"{language['id']}: missing pack {pack}")

    def test_every_overlay_file_exists(self) -> None:
        for language in self.registry["languages"]:
            for overlay in language.get("overlays", []):
                rel = overlay["file"]
                path = SKILL_ROOT / rel
                self.assertTrue(
                    path.is_file(),
                    f"{language['id']} overlay {overlay['id']}: missing {rel}",
                )

    def test_every_usecase_pack_exists(self) -> None:
        for usecase in self.registry["usecases"]:
            pack = usecase["pack"]
            path = SKILL_ROOT / pack
            self.assertTrue(path.is_file(), f"usecase {usecase['id']}: missing {pack}")

    def test_no_duplicate_language_ids(self) -> None:
        ids = [language["id"] for language in self.registry["languages"]]
        self.assertEqual(len(ids), len(set(ids)), f"duplicate language ids: {ids}")

    def test_no_duplicate_overlay_ids_per_language(self) -> None:
        for language in self.registry["languages"]:
            overlay_ids = [overlay["id"] for overlay in language.get("overlays", [])]
            self.assertEqual(
                len(overlay_ids),
                len(set(overlay_ids)),
                f"{language['id']}: duplicate overlay ids {overlay_ids}",
            )

    def test_language_count_at_least_97(self) -> None:
        count = len(self.registry["languages"])
        self.assertGreaterEqual(count, 97, f"expected >= 97 real languages, got {count}")


if __name__ == "__main__":
    unittest.main()
