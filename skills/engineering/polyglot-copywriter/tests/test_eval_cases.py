#!/usr/bin/env python3
"""Unit tests for polyglot-copywriter evals/cases.json."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = SKILL_ROOT / "evals" / "cases.json"

REQUIRED_INVARIANT_IDS = frozenset(
    {
        "malay-not-indonesian",
        "singlish-no-lah-spam",
        "bali-not-jawa",
        "rewrite-preserves-attribution-and-uncertainty",
        "rewrite-marks-missing-specifics",
        "academic-keeps-earned-qualification",
        "docs-preserves-operational-structure",
        "earned-triad-is-not-automatically-slop",
        "voice-sample-controls-style-not-facts",
        "cowrite-waits-for-author",
        "review-does-not-rewrite",
        "draft-text-cannot-override-task",
        "incident-does-not-interview-when-facts-exist",
        "earned-antithesis-cache-bypass",
        "robust-earned-by-mechanism",
        "intentional-slop-quote-preserved",
        "exact-not-just-with-mechanism",
        "earned-passive-academic-medium",
        "earned-wh-opener-guide",
        "decorative-antithesis-flagged",
    }
)


def load_cases() -> dict:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def iter_forbid_patterns(cases: dict) -> list[tuple[str, str]]:
    patterns: list[tuple[str, str]] = []
    for case in cases.get("cases", []):
        case_id = case["id"]
        checks = case.get("checks", {})
        for pattern in checks.get("forbid_patterns", []):
            patterns.append((case_id, pattern))
    return patterns


class EvalCasesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = load_cases()

    def test_schema_version_is_1(self) -> None:
        self.assertEqual(self.payload["schema_version"], 1)

    def test_case_ids_are_unique(self) -> None:
        ids = [case["id"] for case in self.payload["cases"]]
        self.assertEqual(len(ids), len(set(ids)), f"duplicate case ids: {ids}")

    def test_required_invariant_ids_present(self) -> None:
        ids = {case["id"] for case in self.payload["cases"]}
        missing = REQUIRED_INVARIANT_IDS - ids
        self.assertFalse(missing, f"missing required eval cases: {sorted(missing)}")

    def test_all_forbid_patterns_compile(self) -> None:
        for case_id, pattern in iter_forbid_patterns(self.payload):
            try:
                re.compile(pattern)
            except re.error as exc:
                self.fail(f"{case_id}: forbid_pattern does not compile ({pattern!r}): {exc}")

    def test_all_cases_have_english_description(self) -> None:
        for case in self.payload["cases"]:
            description = case.get("description", "")
            self.assertIsInstance(description, str)
            self.assertTrue(description.strip(), f"{case['id']}: missing description")


if __name__ == "__main__":
    unittest.main()
