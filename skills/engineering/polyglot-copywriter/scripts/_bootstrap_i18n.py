#!/usr/bin/env python3
"""One-time bootstrap helper for i18n pack scaffolding. Not part of runtime validation."""

from __future__ import annotations

import json
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
LANG_ROOT = SKILL_ROOT / "references" / "languages"

CATALOGUED_STUBS = [
    ("mandarin", "Mandarin Chinese", ["zh", "中文", "Chinese", "Mandarin"], False, []),
    ("hindi", "Hindi", ["hi", "हिन्दी"], False, []),
    ("spanish", "Spanish", ["es", "español", "Spanyol"], False, []),
    ("arabic", "Arabic", ["ar", "العربية", "Arab"], True, []),
    ("french", "French", ["fr", "français", "Perancis"], False, []),
    ("bengali", "Bengali", ["bn", "বাংলা"], False, []),
    ("portuguese", "Portuguese", ["pt", "português"], False, []),
    ("urdu", "Urdu", ["ur", "اردو"], False, []),
    ("russian", "Russian", ["ru", "русский"], False, []),
    ("german", "German", ["de", "Deutsch"], False, []),
    ("japanese", "Japanese", ["jp", "ja", "日本語", "Jepang"], False, []),
    ("pcm", "Nigerian Pidgin", ["pidgin", "Naija"], False, []),
    ("arz", "Egyptian Arabic", ["Egyptian Arabic", "Masri"], False, []),
    ("marathi", "Marathi", ["mr", "मराठी"], False, []),
    ("vietnamese", "Vietnamese", ["vi", "Tiếng Việt"], False, []),
    ("telugu", "Telugu", ["te", "తెలుగు"], False, []),
    ("swahili", "Swahili", ["sw", "Kiswahili"], False, []),
    ("hausa", "Hausa", ["ha"], False, []),
    ("korean", "Korean", ["ko", "kr", "한국어", "Korea"], False, []),
    ("tagalog", "Tagalog", ["tl", "Filipino"], False, []),
    ("turkish", "Turkish", ["tr", "Türkçe"], False, []),
    ("abui", "Abui", ["Aboa", "bahasa Abui"], False, []),
    ("dayak", "Dayak", ["bahasa Dayak", "Dayak languages"], True, []),
    ("dayak-ngaju", "Dayak Ngaju", ["Ngaju", "bahasa Ngaju"], False, []),
    ("makassar", "Makassar", ["Makassarese", "bahasa Makassar"], False, []),
    ("minangkabau", "Minangkabau", ["Minang", "bahasa Minang"], False, []),
]

STUB_PACK = """# {name} — catalogued

**Status:** `catalogued`. This skill recognises the name only. Do **not** invent vocabulary, grammar, pronouns, particles, or slang.

## Honesty

- Offer `indonesia` or `english` for full the author fingerprint output, or ask the user for examples.
- If the user supplies examples, follow visible patterns in a limited way. Do not fill gaps with invented forms.
- Planned overlays may be listed in [registry.json](../../registry.json) but are not loaded until status is `beta` or `validated`.

## Default register

`profesional` for work explanations; `santai` only when the user asks for casual tone in a language this skill does not yet write.
"""


def write_stub(lang_id: str, name: str) -> None:
    folder = LANG_ROOT / lang_id
    folder.mkdir(parents=True, exist_ok=True)
    pack = folder / "pack.md"
    if not pack.exists():
        pack.write_text(STUB_PACK.format(name=name), encoding="utf-8")


def main() -> None:
    for lang_id, name, _aliases, _umbrella, _overlays in CATALOGUED_STUBS:
        write_stub(lang_id, name)
    print(f"Stub packs ensured under {LANG_ROOT}")


if __name__ == "__main__":
    main()
