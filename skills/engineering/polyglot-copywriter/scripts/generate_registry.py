#!/usr/bin/env python3
"""Generate references/registry.json — run once during i18n migration."""

from __future__ import annotations

import json
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
OUT = SKILL_ROOT / "references" / "registry.json"


def lang(
    id: str,
    name: str,
    iso: str,
    aliases: list[str],
    status: str,
    umbrella: bool = False,
    speech_levels: list[str] | None = None,
    overlays: list[dict] | None = None,
) -> dict:
    return {
        "id": id,
        "iso": iso,
        "name": name,
        "aliases": aliases,
        "umbrella": umbrella,
        "support": {"status": status, "pack": f"references/languages/{id}/pack.md"},
        "registers": ["baku", "profesional", "santai"],
        "speech_levels": speech_levels or [],
        "overlays": overlays or [],
    }


def ov(oid: str, otype: str, status: str, lang_id: str) -> dict:
    return {
        "id": oid,
        "type": otype,
        "status": status,
        "file": f"references/languages/{lang_id}/overlays/{oid}.md",
    }


def uc(uid: str, aliases: list[str], status: str, default_register: str = "santai") -> dict:
    return {
        "id": uid,
        "aliases": aliases,
        "status": status,
        "pack": f"references/usecases/{uid}/pack.md",
        "default_register": default_register,
    }


def main() -> None:
    english_overlays = [
        ov("us", "regional", "validated", "english"),
        ov("uk", "regional", "validated", "english"),
        ov("au", "regional", "catalogued", "english"),
        ov("nz", "regional", "catalogued", "english"),
        ov("ca", "regional", "catalogued", "english"),
        ov("ie", "regional", "catalogued", "english"),
        ov("za", "regional", "catalogued", "english"),
        ov("in-en", "regional", "catalogued", "english"),
        ov("ph-en", "regional", "catalogued", "english"),
        ov("us-slang", "slang", "validated", "english"),
        ov("singlish", "mix", "validated", "english"),
        ov("jaksel", "mix", "validated", "english"),
    ]
    indonesia_overlays = [
        ov("jakarta", "regional", "validated", "indonesia"),
        ov("bandung", "regional", "validated", "indonesia"),
        ov("surabaya", "regional", "validated", "indonesia"),
        ov("yogyakarta", "regional", "validated", "indonesia"),
        ov("medan", "regional", "validated", "indonesia"),
        ov("makassar", "regional", "validated", "indonesia"),
        ov("jaksel", "mix", "validated", "indonesia"),
    ]

    languages = [
        lang(
            "english",
            "English",
            "en",
            ["en", "US English", "Indo-US", "American English"],
            "validated",
            overlays=english_overlays,
        ),
        lang(
            "indonesia",
            "Bahasa Indonesia",
            "id",
            ["Indonesian", "id", "bahasa", "ID"],
            "validated",
            overlays=indonesia_overlays,
        ),
        lang(
            "malay",
            "Malay",
            "ms",
            ["Malaysian Malay", "bahasa Melayu", "Melayu"],
            "beta",
            overlays=[ov("manglish", "mix", "beta", "malay")],
        ),
        lang(
            "jawa",
            "Jawa",
            "jv",
            ["Javanese", "bahasa Jawa"],
            "beta",
            speech_levels=["ngoko", "madya", "krama"],
        ),
        lang(
            "sunda",
            "Sunda",
            "su",
            ["Sundanese", "bahasa Sunda"],
            "beta",
            speech_levels=["loma", "cohag"],
        ),
        lang(
            "bali",
            "Balinese",
            "ban",
            ["bahasa Bali", "Bali"],
            "beta",
            speech_levels=["alus", "madia", "kasar"],
        ),
        lang("mandarin", "Mandarin Chinese", "zh", ["zh", "中文", "Chinese", "Mandarin"], "catalogued"),
        lang("hindi", "Hindi", "hi", ["hi", "हिन्दी"], "catalogued"),
        lang("spanish", "Spanish", "es", ["es", "español", "Spanyol"], "catalogued"),
        lang("arabic", "Arabic", "ar", ["ar", "العربية", "Arab"], "catalogued", umbrella=True),
        lang("french", "French", "fr", ["fr", "français", "Perancis"], "catalogued"),
        lang("bengali", "Bengali", "bn", ["bn", "বাংলা"], "catalogued"),
        lang("portuguese", "Portuguese", "pt", ["pt", "português"], "catalogued"),
        lang("urdu", "Urdu", "ur", ["ur", "اردو"], "catalogued"),
        lang("russian", "Russian", "ru", ["ru", "русский"], "catalogued"),
        lang("german", "German", "de", ["de", "Deutsch"], "catalogued"),
        lang("japanese", "Japanese", "ja", ["jp", "ja", "日本語", "Jepang"], "catalogued"),
        lang("pcm", "Nigerian Pidgin", "pcm", ["pidgin", "Naija"], "catalogued"),
        lang("arz", "Egyptian Arabic", "arz", ["Egyptian Arabic", "Masri"], "catalogued"),
        lang("marathi", "Marathi", "mr", ["mr", "मराठी"], "catalogued"),
        lang("vietnamese", "Vietnamese", "vi", ["vi", "Tiếng Việt"], "catalogued"),
        lang("telugu", "Telugu", "te", ["te", "తెలుగు"], "catalogued"),
        lang("swahili", "Swahili", "sw", ["sw", "Kiswahili"], "catalogued"),
        lang("hausa", "Hausa", "ha", ["ha"], "catalogued"),
        lang("korean", "Korean", "ko", ["ko", "kr", "한국어", "Korea"], "catalogued"),
        lang("tagalog", "Tagalog", "tl", ["tl", "Filipino"], "catalogued"),
        lang("turkish", "Turkish", "tr", ["tr", "Türkçe"], "catalogued"),
        lang("abui", "Abui", "", ["Aboa", "bahasa Abui"], "catalogued"),
        lang("dayak", "Dayak", "", ["bahasa Dayak", "Dayak languages"], "catalogued", umbrella=True),
        lang("dayak-ngaju", "Dayak Ngaju", "", ["Ngaju", "bahasa Ngaju"], "catalogued"),
        lang("makassar", "Makassar", "", ["Makassarese", "bahasa Makassar"], "catalogued"),
        lang("minangkabau", "Minangkabau", "", ["Minang", "bahasa Minang"], "catalogued"),
    ]

    usecases = [
        uc("casual", ["default", "everyday"], "validated", "santai"),
        uc("email", ["inbox", "reply to this mail", "subject line"], "validated", "profesional"),
        uc("letter", ["surat", "cover letter", "recommendation letter"], "validated", "profesional"),
        uc("announcement", ["announce", "FYI team", "channel post", "blast"], "validated", "profesional"),
        uc("chat", ["Lark", "message", "standup", "DM", "thread", "conversation"], "validated", "santai"),
        uc("technical-doc", ["RFC", "ADR", "PRD", "design doc", "architecture", "RCA", "incident doc"], "validated", "profesional"),
        uc("glab-code-review", ["glab-mr-review", "MR", "merge request", "code review", "mr-review", "glab mr review", "nit", "lgtm", "diff"], "validated", "santai"),
        uc("peer-review", ["360", "peer feedback", "performance review", "self-assessment"], "validated", "profesional"),
        uc("poetic", ["puitis", "poetic", "lebih liris"], "validated", "santai"),
        uc("humanize", ["humanize", "too AI", "de-AI"], "validated", "santai"),
        uc("vocab", ["vocabulary", "vocab", "word of the day"], "validated", "santai"),
        uc("marketing", ["landing page", "homepage", "pricing page"], "catalogued", "profesional"),
        uc("ads", ["ad copy", "advertisement"], "catalogued", "profesional"),
        uc("social", ["LinkedIn post", "tweet", "Instagram"], "catalogued", "santai"),
        uc("docs", ["runbook", "internal guide", "meeting notes"], "catalogued", "profesional"),
        uc("slides", ["deck", "presentation"], "catalogued", "profesional"),
        uc("incident", ["incident comms", "outage update"], "catalogued", "profesional"),
        uc("academic", ["journal review", "paper critique"], "catalogued", "baku"),
    ]

    registry = {
        "schema_version": 2,
        "source": {
            "name": "Polyglot Voice pluggable registry",
            "note": "Languages and use cases are plug-in rows. Markdown packs are content. SKILL.md routes via this file.",
        },
        "languages": languages,
        "usecases": usecases,
    }
    OUT.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(languages)} languages, {len(usecases)} use cases)")


if __name__ == "__main__":
    main()
