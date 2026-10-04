#!/usr/bin/env python3
"""Unit tests for polyglot-copywriter eval and language scripts."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = SKILL_ROOT / "scripts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


evaluate_output = load_module("evaluate_output", SCRIPTS / "evaluate_output.py")
find_language = load_module("find_language", SCRIPTS / "find_language.py")
validate_skill = load_module("validate_skill", SCRIPTS / "validate_skill.py")


class EvaluateOutputTests(unittest.TestCase):
    def test_preserve_and_first_paragraph(self) -> None:
        case = {
            "id": "demo",
            "checks": {
                "preserve": ["API_TOKEN", ".env"],
                "require": ["loadConfig"],
                "forbid_patterns": ["\\bgue\\b"],
                "first_paragraph_require": ["API_TOKEN"],
            },
        }
        good = "API_TOKEN missing from .env.\n\nCheck loadConfig next."
        self.assertEqual(evaluate_output.evaluate_output(case, good), [])

    def test_reports_each_failure_class(self) -> None:
        case = {
            "id": "demo",
            "checks": {
                "preserve": ["API_TOKEN"],
                "require": ["readConfig"],
                "forbid_patterns": ["\\bgue\\b"],
                "first_paragraph_require": ["API_TOKEN"],
            },
        }
        bad = "gue said the token is gone."
        failures = evaluate_output.evaluate_output(case, bad)
        self.assertEqual(len(failures), 4)

    def test_cli_pass_and_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "out.txt"
            output.write_text(
                "API_TOKEN is missing from .env so loadConfig at src/config.ts:42 "
                "returns undefined.\n\n"
                "TypeError: Cannot read properties of undefined (reading 'trim')\n"
                "Run npm test -- config.",
                encoding="utf-8",
            )
            self.assertEqual(
                evaluate_output.main(["netral-bug-explanation", str(output)]),
                0,
            )
            output.write_text("wrong", encoding="utf-8")
            self.assertEqual(
                evaluate_output.main(["netral-bug-explanation", str(output)]),
                1,
            )
            self.assertEqual(evaluate_output.main([]), 2)


class FindLanguageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.languages = find_language.load_languages()

    def test_english_and_indonesia_are_validated(self) -> None:
        english = find_language.find_languages(self.languages, "English")[0]
        indonesia = find_language.find_languages(self.languages, "bahasa")[0]
        self.assertEqual(english["support"]["status"], "validated")
        self.assertEqual(indonesia["id"], "indonesia")

    def test_abui_alias_and_dayak_umbrella(self) -> None:
        abui = find_language.find_languages(self.languages, "Aboa")[0]
        dayak = find_language.find_languages(self.languages, "Dayak")[0]
        self.assertEqual(abui["id"], "abui")
        self.assertTrue(dayak["umbrella"])

    def test_japanese_malay_mandarin_resolve(self) -> None:
        japanese = find_language.find_languages(self.languages, "Japanese")[0]
        malay = find_language.find_languages(self.languages, "Malay")[0]
        mandarin = find_language.find_languages(self.languages, "Mandarin")[0]
        self.assertEqual(japanese["id"], "japanese")
        self.assertEqual(malay["id"], "malay")
        self.assertEqual(mandarin["id"], "mandarin")
        for row in (japanese, malay, mandarin):
            self.assertEqual(row["support"]["status"], "validated")

    def test_makassar_is_validated_language(self) -> None:
        makassar = find_language.find_languages(self.languages, "Makassar")[0]
        self.assertEqual(makassar["id"], "makassar")
        self.assertEqual(makassar["support"]["status"], "validated")

    def test_wave2_languages_are_validated(self) -> None:
        for lang_id in (
            "japanese",
            "korean",
            "vietnamese",
            "spanish",
            "portuguese",
            "french",
            "hindi",
            "tagalog",
            "mandarin",
        ):
            row = next(item for item in self.languages if item["id"] == lang_id)
            self.assertEqual(row["support"]["status"], "validated")

    def test_all_registry_languages_validated(self) -> None:
        for row in self.languages:
            self.assertEqual(row["support"]["status"], "validated")

    def test_marketing_usecase_validated(self) -> None:
        registry = json.loads((SKILL_ROOT / "references/registry.json").read_text())
        marketing = next(uc for uc in registry["usecases"] if uc["id"] == "marketing")
        self.assertEqual(marketing["status"], "validated")

    def test_cli_prints_rows(self) -> None:
        self.assertEqual(find_language.main(["Abui"]), 0)
        self.assertEqual(find_language.main([]), 2)


class ValidateSkillTests(unittest.TestCase):
    def test_current_skill_passes(self) -> None:
        self.assertEqual(validate_skill.main([str(SKILL_ROOT)]), 0)


if __name__ == "__main__":
    unittest.main()
