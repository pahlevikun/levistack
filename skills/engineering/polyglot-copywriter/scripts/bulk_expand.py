#!/usr/bin/env python3
"""One-shot bulk generator: locale techniques, profiles, index updates."""

from __future__ import annotations

import json
from pathlib import Path

from catalog import fictional_fixture_ids

SKILL_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = SKILL_ROOT / "references" / "registry.json"
TECH_INDEX_PATH = SKILL_ROOT / "references" / "techniques" / "index.json"
PROFILE_INDEX_PATH = SKILL_ROOT / "references" / "profiles" / "index.json"
LOCALES_DIR = SKILL_ROOT / "references" / "techniques" / "locales"
PROFILES_DIR = SKILL_ROOT / "references" / "profiles"

# Languages that had locale files before the registry-driven expansion
LEGACY_LOCALE_IDS = {
    "japanese",
    "indonesia",
    "mandarin",
    "korean",
    "vietnamese",
    "spanish",
    "french",
    "portuguese",
    "hindi",
    "tagalog",
}

LOCALE_USECASES = {
    "default": ["marketing", "ads", "social", "email", "chat", "incident", "docs", "academic"],
    "light": ["marketing", "ads", "social", "email", "chat"],
    "umbrella": ["marketing", "email", "chat"],
    "limited": ["email", "chat", "docs"],
}

LOCALE_PROFILE = {
    "arabic": {
        "usecases": "umbrella",
        "note": "Umbrella — route to dialect overlay or `arz` for Egyptian. Marketing/email/incident sections are light.",
        "marketing_bad": "Leverage our innovative solution",
        "marketing_good": "Reduce weekly reporting from 4 hours to 15 minutes",
        "email_bad": "We wish to inform you that…",
        "email_good": "Attached is the revised quote — please confirm by Friday",
        "incident_bad": "We apologize for any inconvenience",
        "incident_good": "Checkout failed for ~3% of sessions for 20 min; rollback at 14:32 UTC, errors normal",
    },
    "dayak-ngaju": {
        "usecases": "limited",
        "note": "Limited coverage — follow pack honesty; no invented Ngaju forms.",
    },
    "abui": {
        "usecases": "limited",
        "note": "Limited coverage — follow pack honesty; no invented Abui dialects.",
    },
    "minangkabau": {
        "usecases": "limited",
        "note": "Limited pack — stay within documented overlays.",
    },
    "makassar": {
        "usecases": "limited",
        "note": "Language pack — not `indonesia/makassar` city overlay.",
    },
    "kurdish": {
        "usecases": "umbrella",
        "note": "Umbrella — ask Kurmanji vs Sorani before thick prose; no invented dialect forms.",
    },
    "kashmiri": {
        "usecases": "limited",
        "note": "Limited coverage — conservative standard; ask script/dialect if unclear.",
    },
    "quechua": {
        "usecases": "limited",
        "note": "Limited coverage — ask regional variety; no invented dialect forms.",
    },
    "guarani": {
        "usecases": "limited",
        "note": "Limited coverage — ask regional variety; no invented dialect forms.",
    },
    "latin": {
        "usecases": "limited",
        "note": "Classical Latin — default baku; light marketing.",
    },
    "hokkien": {
        "usecases": "limited",
        "note": "Separate from mandarin — Minnan/Taiwanese; conservative forms.",
    },
    "cantonese": {
        "usecases": "default",
        "note": "Separate from mandarin — Yue/Cantonese grammar and lexicon.",
    },
    "english": {
        "usecases": "default",
        "note": "Register notes for in-en, au, uk overlays — the author fingerprint applies by default.",
        "extra": """
## Register notes (English varieties)

| Overlay | Spelling / tone |
|---|---|
| `us` / netral | American spelling; casual coworker default |
| `uk` | British spelling (colour, organise) |
| `au` | Australian light markers — avoid caricature |
| `in-en` | Indian English — formal complete sentences; Hinglish only if explicit |

the author fingerprint: [voice-fingerprint.md](../../voice-fingerprint.md). Locale file supplements overlay packs, not core.md.
""",
    },
}

PROFILE_EXCEPTIONS = fictional_fixture_ids()  # fictional fixtures have no overlays

PROFILE_BULLETS = {
    "regional": [
        "Load when `regional_voice` matches this overlay id.",
        "Default register: `profesional` for work email; `santai` for chat unless user says otherwise.",
        "One overlay at a time — no dialect soup.",
        "Lead with impact; protected code/paths stay literal.",
        "Follow overlay caps — light regional colour, not caricature.",
    ],
    "mix": [
        "Mix overlay — load only when user explicitly asked.",
        "Cap loanwords; keep grammar of the primary language.",
        "No marker quota — pragmatic function over iconic vocabulary.",
        "Protected artifacts unchanged.",
    ],
    "slang": [
        "Slang overlay — casual contexts only.",
        "Not for customer email or incident comms unless user asked.",
        "Keep sentences complete; no telegram fragments.",
    ],
}


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def locale_content(lang_id: str, lang_name: str) -> str:
    profile = LOCALE_PROFILE.get(lang_id, {})
    usecases_key = profile.get("usecases", "default")
    usecases = LOCALE_USECASES[usecases_key]
    note = profile.get("note", "Transcreation — adapt for region and register, not translate-then-polish.")
    extra = profile.get("extra", "")

    m_bad = profile.get("marketing_bad", "Leverage our innovative solution")
    m_good = profile.get("marketing_good", "Concrete benefit + proof when available")
    e_bad = profile.get("email_bad", "We wish to inform you that…")
    e_good = profile.get("email_good", "Line 1 = answer or request")
    i_bad = profile.get("incident_bad", "We apologize for any inconvenience")
    i_good = profile.get("incident_good", "Impact + current status in sentence 1")

    sections = []
    if "marketing" in usecases:
        sections.append(f"""## Marketing

- Headline: concrete benefit + proof if available
- One primary CTA; no fabricated stats
- {note}

| Bad (calque) | Good |
|---|---|
| {m_bad} | {m_good} |""")
    if "email" in usecases:
        sections.append(f"""## Email / chat

- Line 1: answer or request — no warmup opener
- Match register to channel (chat may be shorter, still complete)

| Bad | Good |
|---|---|
| {e_bad} | {e_good} |""")
    if "incident" in usecases:
        sections.append(f"""## Incident

- Sentence 1: impact + current status
- Next update time when known
- No marketing tone

| Bad | Good |
|---|---|
| {i_bad} | {i_good} |""")
    if "docs" in usecases:
        sections.append("""## Docs

- Procedure steps as numbered list when helpful
- Keep technical terms repo-natural
- Complete sentences in `profesional` register""")
    if "academic" in usecases:
        sections.append("""## Academic

- `baku` register; hedging where evidence requires
- No marketing adjectives in critique sections""")

    body = "\n\n".join(sections)
    umbrella_block = ""
    if lang_id == "arabic":
        umbrella_block = """
## Honesty (umbrella)

- `arabic` is umbrella — prefer `arz` for sustained Egyptian, or a named dialect overlay (Levantine, Gulf).
- Do not write textbook MSA-only unless user asked; do not invent dialect forms.
- Marketing/email/incident guidance here is **light** — defer to active overlay pack.

"""

    return f"""# {lang_name} locale techniques

Load when **`language` is `{lang_id}`**. Base: [languages/{lang_id}/pack.md](../../languages/{lang_id}/pack.md), [culture.md](../../languages/{lang_id}/culture.md). Overlays under [languages/{lang_id}/overlays/](../../languages/{lang_id}/overlays/).

**Transcreation** — {note}
{umbrella_block}
## Register defaults by use case

| Use case | Default register | Notes |
|---|---|---|
| marketing | `profesional` | Benefit-first; match overlay lexicon |
| email | `profesional` | Complete sentences |
| chat | `santai` | Shorter OK; still grammatical |
| incident | `profesional` | Impact first |

Set `regional_voice` from user region name. One overlay at a time.

{body}
{extra}
## Related

- [marketing-copy.md](../marketing-copy.md)
- [email-comms.md](../email-comms.md)
- [incident-comms.md](../incident-comms.md)
"""


def all_language_ids(registry: dict) -> set[str]:
    return {lang["id"] for lang in registry.get("languages", [])}


def profile_content(lang_id: str, overlay_id: str, overlay_type: str, lang_name: str) -> str:
    bullets = PROFILE_BULLETS.get(overlay_type, PROFILE_BULLETS["regional"])
    bullet_text = "\n".join(f"- {b}" for b in bullets[:5])
    locale_link = f"\n**Locale techniques:** [locales/{lang_id}.md](../techniques/locales/{lang_id}.md) when use case matches.\n"
    return f"""# {overlay_id} profile (summary)

**Language:** `{lang_id}` · **Overlay id:** `{overlay_id}`

Full rules: [languages/{lang_id}/overlays/{overlay_id}.md](../languages/{lang_id}/overlays/{overlay_id}.md).

{lang_name} overlay — load when `regional_voice: {overlay_id}` or user names this region/variety.

**When to load:** `language: {lang_id}` + `regional_voice: {overlay_id}`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
{bullet_text}
{locale_link}
**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
"""


def main() -> None:
    registry = load_registry()
    languages = {lang["id"]: lang for lang in registry["languages"]}
    registry_lang_ids = all_language_ids(registry)

    # Locale files — one per registry language (fictional fixtures live in fictional-catalog.json)
    skip_locales = fictional_fixture_ids()
    for lang_id in sorted(registry_lang_ids - skip_locales):
        lang_name = languages.get(lang_id, {}).get("name", lang_id.title())
        path = LOCALES_DIR / f"{lang_id}.md"
        path.write_text(locale_content(lang_id, lang_name), encoding="utf-8")
        print(f"locale: {path.name}")

    # Technique index
    tech_index = json.loads(TECH_INDEX_PATH.read_text(encoding="utf-8"))
    all_locale_ids = sorted(registry_lang_ids - skip_locales)
    new_locales = []
    for lang_id in all_locale_ids:
        if lang_id not in languages:
            continue
        usecases_key = LOCALE_PROFILE.get(lang_id, {}).get("usecases", "default")
        entry = {
            "id": lang_id,
            "languages": [lang_id],
            "usecases": LOCALE_USECASES[usecases_key],
            "file": f"references/techniques/locales/{lang_id}.md",
        }
        new_locales.append(entry)
    tech_index["locales"] = new_locales
    TECH_INDEX_PATH.write_text(json.dumps(tech_index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"technique index: {len(new_locales)} locales")

    # Profiles
    profile_index = json.loads(PROFILE_INDEX_PATH.read_text(encoding="utf-8"))
    existing_profiles = {(p["language_id"], p["overlay_id"]) for p in profile_index.get("profiles", [])}
    profiles = list(profile_index.get("profiles", []))

    for lang in registry["languages"]:
        lang_id = lang["id"]
        if lang_id in PROFILE_EXCEPTIONS:
            continue
        lang_name = lang.get("name", lang_id)
        for overlay in lang.get("overlays") or []:
            oid = overlay["id"]
            key = (lang_id, oid)
            if key in existing_profiles:
                continue
            otype = overlay.get("type", "regional")
            profile_file = f"references/profiles/{oid}.md"
            profile_path = PROFILES_DIR / f"{oid}.md"
            profile_path.write_text(profile_content(lang_id, oid, otype, lang_name), encoding="utf-8")
            profiles.append(
                {
                    "overlay_id": oid,
                    "language_id": lang_id,
                    "file": profile_file,
                }
            )
            print(f"profile: {oid}.md ({lang_id})")

    profile_index["profiles"] = profiles
    PROFILE_INDEX_PATH.write_text(json.dumps(profile_index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"profile index: {len(profiles)} profiles")


if __name__ == "__main__":
    main()
