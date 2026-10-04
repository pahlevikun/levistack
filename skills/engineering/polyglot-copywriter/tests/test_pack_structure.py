#!/usr/bin/env python3
"""Unit tests for sample polyglot-copywriter language pack structure."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
LANG_ROOT = SKILL_ROOT / "references" / "languages"

SAMPLE_LANGUAGES = ("english", "indonesia", "malay", "japanese", "mandarin")
MIN_PACK_CHARS = 200

REGISTER_EXAMPLE_PATTERNS = (
    re.compile(r"✅|❌"),
    re.compile(r"\*\*Good:\*\*", re.IGNORECASE),
    re.compile(r"\*\*Bad:\*\*", re.IGNORECASE),
    re.compile(r"\bJangan\b"),
    re.compile(r"\bNatural\b"),
    re.compile(r"^##\s+What .+ is not", re.IGNORECASE | re.MULTILINE),
    re.compile(r"\*\*Not\b"),
)

GRAMMAR_GUIDANCE_PATTERNS = (
    re.compile(r"^##\s+Natural grammar", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^##\s+.*grammar", re.IGNORECASE | re.MULTILINE),
    # Calque and construction rules (e.g. indonesia wave-1 culture.md)
    re.compile(r"^##\s+Do not copy", re.IGNORECASE | re.MULTILINE),
)


def has_register_examples(text: str) -> bool:
    return any(pattern.search(text) for pattern in REGISTER_EXAMPLE_PATTERNS)


def has_grammar_guidance(text: str) -> bool:
    return any(pattern.search(text) for pattern in GRAMMAR_GUIDANCE_PATTERNS)


class PackStructureTests(unittest.TestCase):
    def test_registers_have_good_bad_examples(self) -> None:
        for lang_id in SAMPLE_LANGUAGES:
            path = LANG_ROOT / lang_id / "registers.md"
            self.assertTrue(path.is_file(), f"{lang_id}: missing registers.md")
            content = path.read_text(encoding="utf-8")
            self.assertTrue(
                has_register_examples(content),
                f"{lang_id}/registers.md: missing good/bad or equivalent examples",
            )

    def test_culture_has_grammar_guidance(self) -> None:
        for lang_id in SAMPLE_LANGUAGES:
            path = LANG_ROOT / lang_id / "culture.md"
            self.assertTrue(path.is_file(), f"{lang_id}: missing culture.md")
            content = path.read_text(encoding="utf-8")
            self.assertTrue(
                has_grammar_guidance(content),
                f"{lang_id}/culture.md: missing grammar guidance section",
            )

    def test_pack_md_is_non_trivial(self) -> None:
        for lang_id in SAMPLE_LANGUAGES:
            path = LANG_ROOT / lang_id / "pack.md"
            self.assertTrue(path.is_file(), f"{lang_id}: missing pack.md")
            content = path.read_text(encoding="utf-8")
            self.assertGreater(
                len(content.strip()),
                MIN_PACK_CHARS,
                f"{lang_id}/pack.md: expected >{MIN_PACK_CHARS} chars",
            )


if __name__ == "__main__":
    unittest.main()
