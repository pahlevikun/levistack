#!/usr/bin/env python3
"""Every registry overlay must have a profile (except documented exceptions)."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = SKILL_ROOT / "references" / "registry.json"
PROFILE_INDEX_PATH = SKILL_ROOT / "references" / "profiles" / "index.json"

sys_path = SKILL_ROOT / "scripts"
if str(sys_path) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(sys_path))

from catalog import fictional_fixture_ids  # noqa: E402

NO_OVERLAY_EXCEPTIONS = fictional_fixture_ids()


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def load_profile_index() -> dict:
    return json.loads(PROFILE_INDEX_PATH.read_text(encoding="utf-8"))


class ProfileCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry()
        cls.profile_index = load_profile_index()
        cls.profile_keys = {
            (entry["language_id"], entry["overlay_id"])
            for entry in cls.profile_index.get("profiles", [])
        }

    def test_profile_index_files_exist(self) -> None:
        missing: list[str] = []
        for entry in self.profile_index.get("profiles", []):
            rel = entry.get("file")
            if not rel or not (SKILL_ROOT / rel).is_file():
                missing.append(rel or "<no file>")
        self.assertFalse(missing, f"missing profile files: {missing}")

    def test_every_overlay_has_profile(self) -> None:
        missing: list[str] = []
        for lang in self.registry.get("languages", []):
            lang_id = lang["id"]
            if lang_id in NO_OVERLAY_EXCEPTIONS:
                continue
            for overlay in lang.get("overlays") or []:
                oid = overlay["id"]
                key = (lang_id, oid)
                if key not in self.profile_keys:
                    missing.append(f"{lang_id}:{oid}")
        self.assertFalse(missing, f"overlays without profiles: {missing}")

    def test_profile_points_to_valid_overlay(self) -> None:
        overlay_keys: set[tuple[str, str]] = set()
        for lang in self.registry.get("languages", []):
            lang_id = lang["id"]
            for overlay in lang.get("overlays") or []:
                overlay_keys.add((lang_id, overlay["id"]))
        orphan: list[str] = []
        for entry in self.profile_index.get("profiles", []):
            key = (entry.get("language_id"), entry.get("overlay_id"))
            if key not in overlay_keys:
                orphan.append(f"{key[0]}:{key[1]}")
        self.assertFalse(orphan, f"profiles without registry overlay: {orphan}")


if __name__ == "__main__":
    unittest.main()
