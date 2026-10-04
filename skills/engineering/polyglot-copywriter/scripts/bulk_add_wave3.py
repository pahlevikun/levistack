#!/usr/bin/env python3
"""Bulk-add wave-3 languages (62 packs) with overlays, locales, and profiles."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = SKILL_ROOT / "references" / "registry.json"
LANG_ROOT = SKILL_ROOT / "references" / "languages"
TEMPLATE_ROOT = SKILL_ROOT / "references" / "_template" / "language"

# id, name, iso, overlay_id, aliases, family, umbrella, limited, default_register
WAVE3 = [
    # Europe (28)
    ("greek", "Greek", "el", "el-standard", ["ελληνικά", "ellinika"], "ie_eu", False, False, "profesional"),
    ("dutch", "Dutch", "nl", "nl-standard", ["Nederlands", "Hollands"], "germanic", False, False, "profesional"),
    ("polish", "Polish", "pl", "pl-standard", ["polski", "Polski"], "slavic", False, False, "profesional"),
    ("ukrainian", "Ukrainian", "uk", "uk-ua", ["українська", "ukrainska"], "slavic", False, False, "profesional"),
    ("czech", "Czech", "cs", "cs-standard", ["čeština", "cestina"], "slavic", False, False, "profesional"),
    ("romanian", "Romanian", "ro", "ro-standard", ["română", "romana"], "romance", False, False, "profesional"),
    ("hungarian", "Hungarian", "hu", "hu-standard", ["magyar", "Magyar"], "uralic", False, False, "profesional"),
    ("swedish", "Swedish", "sv", "sv-standard", ["svenska", "Svenska"], "germanic", False, False, "profesional"),
    ("norwegian", "Norwegian", "no", "no-standard", ["norsk", "Norsk"], "germanic", False, False, "profesional"),
    ("danish", "Danish", "da", "da-standard", ["dansk", "Dansk"], "germanic", False, False, "profesional"),
    ("finnish", "Finnish", "fi", "fi-standard", ["suomi", "Suomi"], "uralic", False, False, "profesional"),
    ("serbian", "Serbian", "sr", "sr-standard", ["српски", "srpski"], "slavic", False, False, "profesional"),
    ("croatian", "Croatian", "hr", "hr-standard", ["hrvatski", "Hrvatski"], "slavic", False, False, "profesional"),
    ("bosnian", "Bosnian", "bs", "bs-standard", ["bosanski", "Bosanski"], "slavic", False, False, "profesional"),
    ("bulgarian", "Bulgarian", "bg", "bg-standard", ["български", "bulgarski"], "slavic", False, False, "profesional"),
    ("slovak", "Slovak", "sk", "sk-standard", ["slovenčina", "slovencina"], "slavic", False, False, "profesional"),
    ("slovenian", "Slovenian", "sl", "sl-si", ["slovenščina", "slovenscina"], "slavic", False, False, "profesional"),
    ("lithuanian", "Lithuanian", "lt", "lt-standard", ["lietuvių", "lietuviu"], "baltic", False, False, "profesional"),
    ("latvian", "Latvian", "lv", "lv-standard", ["latviešu", "latviesu"], "baltic", False, False, "profesional"),
    ("estonian", "Estonian", "et", "et-standard", ["eesti", "Eesti"], "uralic", False, False, "profesional"),
    ("icelandic", "Icelandic", "is", "is-standard", ["íslenska", "islenska"], "germanic", False, False, "profesional"),
    ("albanian", "Albanian", "sq", "sq-standard", ["shqip", "Shqip"], "ie_eu", False, False, "profesional"),
    ("catalan", "Catalan", "ca", "cat-standard", ["català", "catala"], "romance", False, False, "profesional"),
    ("galician", "Galician", "gl", "gl-standard", ["galego", "Galego"], "romance", False, False, "profesional"),
    ("basque", "Basque", "eu", "eu-standard", ["euskara", "Euskara"], "isolate", False, False, "profesional"),
    ("irish", "Irish", "ga", "ga-standard", ["Gaeilge", "gaeilge"], "celtic", False, False, "profesional"),
    ("welsh", "Welsh", "cy", "cy-standard", ["Cymraeg", "cymraeg"], "celtic", False, False, "profesional"),
    ("esperanto", "Esperanto", "eo", "eo-standard", ["Esperanto"], "constructed", False, False, "profesional"),
    # Middle East / Central Asia (10)
    ("persian", "Persian", "fa", "fa-standard", ["فارسی", "farsi", "Farsi"], "iranian", False, False, "profesional"),
    ("hebrew", "Hebrew", "he", "he-standard", ["עברית", "ivrit"], "semitic", False, False, "profesional"),
    ("pashto", "Pashto", "ps", "ps-standard", ["پښتو", "pashto"], "iranian", False, False, "profesional"),
    ("kurdish", "Kurdish", "ku", "ku-standard", ["Kurdî", "kurdi", "Kurmanji"], "iranian", True, False, "profesional"),
    ("azerbaijani", "Azerbaijani", "az", "az-standard", ["Azərbaycan", "azeri"], "turkic", False, False, "profesional"),
    ("kazakh", "Kazakh", "kk", "kk-standard", ["қазақ", "qazaq"], "turkic", False, False, "profesional"),
    ("uzbek", "Uzbek", "uz", "uz-standard", ["o'zbek", "ozbek"], "turkic", False, False, "profesional"),
    ("mongolian", "Mongolian", "mn", "mn-standard", ["монгол", "mongol"], "mongolic", False, False, "profesional"),
    ("georgian", "Georgian", "ka", "ka-standard", ["ქართული", "kartuli"], "kartvelian", False, False, "profesional"),
    ("armenian", "Armenian", "hy", "hy-standard", ["հայերեն", "hayeren"], "armenian", False, False, "profesional"),
    # South & SE Asia (14)
    ("thai", "Thai", "th", "th-standard", ["ไทย", "ภาษาไทย"], "se_asian", False, False, "profesional"),
    ("lao", "Lao", "lo", "lo-standard", ["ລາວ", "lao"], "se_asian", False, False, "profesional"),
    ("khmer", "Khmer", "km", "km-standard", ["ខ្មែរ", "khmer"], "se_asian", False, False, "profesional"),
    ("burmese", "Burmese", "my", "my-mm", ["မြန်မာ", "myanmar"], "se_asian", False, False, "profesional"),
    ("nepali", "Nepali", "ne", "ne-standard", ["नेपाली", "nepali"], "south_asian", False, False, "profesional"),
    ("sinhala", "Sinhala", "si", "si-standard", ["සිංහල", "sinhala"], "south_asian", False, False, "profesional"),
    ("gujarati", "Gujarati", "gu", "gu-standard", ["ગુજરાતી", "gujarati"], "south_asian", False, False, "profesional"),
    ("kannada", "Kannada", "kn", "kn-standard", ["ಕನ್ನಡ", "kannada"], "south_asian", False, False, "profesional"),
    ("malayalam", "Malayalam", "ml", "ml-standard", ["മലയാളം", "malayalam"], "south_asian", False, False, "profesional"),
    ("odia", "Odia", "or", "or-standard", ["ଓଡ଼ିଆ", "oriya"], "south_asian", False, False, "profesional"),
    ("assamese", "Assamese", "as", "as-standard", ["অসমীয়া", "asamiya"], "south_asian", False, False, "profesional"),
    ("kashmiri", "Kashmiri", "ks", "ks-standard", ["کٲشُر", "koshur"], "south_asian", False, True, "profesional"),
    ("sindhi", "Sindhi", "sd", "sd-standard", ["سنڌي", "sindhi"], "south_asian", False, False, "profesional"),
    ("cantonese", "Cantonese", "yue", "yue-hk", ["粵語", "廣東話", "Cantonese"], "sinitic", False, False, "profesional"),
    # Africa (6)
    ("amharic", "Amharic", "am", "am-standard", ["አማርኛ", "amharic"], "semitic", False, False, "profesional"),
    ("somali", "Somali", "so", "so-standard", ["Soomaali", "soomaali"], "cushitic", False, False, "profesional"),
    ("yoruba", "Yoruba", "yo", "yo-standard", ["Yorùbá", "yoruba"], "niger_congo", False, False, "profesional"),
    ("igbo", "Igbo", "ig", "ig-standard", ["Igbo", "ibo"], "niger_congo", False, False, "profesional"),
    ("zulu", "Zulu", "zu", "zu-standard", ["isiZulu", "zulu"], "niger_congo", False, False, "profesional"),
    ("afrikaans", "Afrikaans", "af", "af-standard", ["Afrikaans"], "germanic", False, False, "profesional"),
    # Americas indigenous (2)
    ("quechua", "Quechua", "qu", "qu-standard", ["Runasimi", "Quechua"], "indigenous", False, True, "profesional"),
    ("guarani", "Guarani", "gn", "gn-standard", ["Avañe'ẽ", "guarani"], "indigenous", False, True, "profesional"),
    # Classical (1)
    ("latin", "Latin", "la", "la-standard", ["Latina", "classical Latin"], "classical", False, True, "baku"),
    # Hokkien — separate from mandarin (documented in pack)
    ("hokkien", "Hokkien", "nan", "nan-tw", ["Minnan", "Taiwanese", "福建話"], "sinitic", False, True, "profesional"),
]

# Per-language register example overrides (baku_good, prof_good, santai_good, baku_bad, prof_bad, santai_bad)
EXAMPLES: dict[str, dict[str, str]] = {
    "greek": {
        "baku_good": "Ενημερώνουμε ότι η υπηρεσία θα διακοπεί την Τρίτη για συντήρηση.",
        "prof_good": "Το `API_TOKEN` λείπει από το `.env`, οπότε το `loadConfig` επιστρέφει `undefined`.",
        "santai_good": "Δεν έχει `API_TOKEN` στο `.env` — τρέξε `npm test -- config`.",
    },
    "dutch": {
        "baku_good": "Hierbij informeren wij u dat de dienst dinsdag onderhoud krijgt.",
        "prof_good": "`API_TOKEN` staat niet in `.env`, dus `loadConfig` geeft `undefined` terug.",
        "santai_good": "Geen `API_TOKEN` in `.env` — run `npm test -- config`.",
    },
    "polish": {
        "baku_good": "Informujemy, że usługa będzie niedostępna we wtorek z powodu konserwacji.",
        "prof_good": "Brakuje `API_TOKEN` w `.env`, więc `loadConfig` zwraca `undefined`.",
        "santai_good": "Nie ma `API_TOKEN` w `.env` — odpal `npm test -- config`.",
    },
    "thai": {
        "baku_good": "แจ้งให้ทราบว่าบริการจะหยุดให้บริการวันอังคารเพื่อบำรุงรักษา",
        "prof_good": "ไม่มี `API_TOKEN` ใน `.env` เลย `loadConfig` คืนค่า `undefined`",
        "santai_good": "`.env` ไม่มี `API_TOKEN` — รัน `npm test -- config` นะ",
    },
    "persian": {
        "baku_good": "به اطلاع می‌رساند سرویس روز سه‌شنبه برای نگهداری قطع می‌شود.",
        "prof_good": "`API_TOKEN` در `.env` نیست؛ `loadConfig` مقدار `undefined` برمی‌گرداند.",
        "santai_good": "`API_TOKEN` توی `.env` نیست — `npm test -- config` بزن.",
    },
    "hebrew": {
        "baku_good": "הודעה: השירות יושבת ביום שלישי לצורך תחזוקה.",
        "prof_good": "חסר `API_TOKEN` ב־`.env`, ולכן `loadConfig` מחזיר `undefined`.",
        "santai_good": "אין `API_TOKEN` ב־`.env` — תריץ `npm test -- config`.",
    },
    "cantonese": {
        "baku_good": "特此通知：服務將於星期二維護期間暫停。",
        "prof_good": "`.env` 冇 `API_TOKEN`，所以 `loadConfig` 返回 `undefined`。",
        "santai_good": "`.env` 冇 `API_TOKEN` — 跑 `npm test -- config`。",
    },
    "hokkien": {
        "baku_good": "通知：服務禮拜二會停機維修。",
        "prof_good": "`.env` 無 `API_TOKEN`，所以 `loadConfig` 回傳 `undefined`。",
        "santai_good": "`.env` 無 `API_TOKEN` — 跑 `npm test -- config`。",
    },
    "latin": {
        "baku_good": "Notificamus operam die Martis propter conservationem intermissam iri.",
        "prof_good": "`API_TOKEN` in `.env` non est; `loadConfig` `undefined` reddit.",
        "santai_good": "`API_TOKEN` in `.env` non est — `npm test -- config` exsequere.",
    },
    "afrikaans": {
        "baku_good": "Hiermee word kennis gegee dat die diens Dinsdag onderhoud ondergaan.",
        "prof_good": "`API_TOKEN` is nie in `.env` nie, so `loadConfig` gee `undefined` terug.",
        "santai_good": "Geen `API_TOKEN` in `.env` — hardloop `npm test -- config`.",
    },
}

GRAMMAR: dict[str, str] = {
    "germanic": (
        "1. **V2 in main clauses** — finite verb second in statements.\n"
        "2. **Compound verbs** — separable prefixes in correct position.\n"
        "3. **Formal pronouns** — Sie/u in work external unless user says informal.\n"
        "4. **No English -ing calques** — use native gerund/participle patterns.\n"
        "5. **Preposition government** — match case where applicable.\n"
        "6. **Technical literals** — keep code tokens exact.\n"
        "7. **Natural word order** — avoid English front-loading every sentence."
    ),
    "romance": (
        "1. **Flexible SVO** — natural clitics and pronoun placement.\n"
        "2. **Por/para or de/a** — purpose vs possession, not English preposition calques.\n"
        "3. **Register agreement** — formal vs informal pronouns locked per message.\n"
        "4. **Subjunctive** — sparingly for soft requests.\n"
        "5. **Articles** — natural gender/number agreement.\n"
        "6. **Overlay lexicon** — stay within active regional overlay.\n"
        "7. **Code literals** unchanged."
    ),
    "slavic": (
        "1. **Case agreement** — noun/adjective/preposition cases must align.\n"
        "2. **Aspect** — perfective vs imperfective for completed vs ongoing.\n"
        "3. **No article calques** — Slavic definiteness via context.\n"
        "4. **Formal vy** — work external default where language uses it.\n"
        "5. **Word order** — flexible but natural; not English SVO pasted.\n"
        "6. **Technical terms** — repo literals exact.\n"
        "7. **Cyrillic/Latin script** — one script per message unless user asked."
    ),
    "uralic": (
        "1. **Agglutination** — suffix chains in natural order; do not split artificially.\n"
        "2. **Vowel harmony** — respect front/back harmony in suffixes.\n"
        "3. **No gender** — do not import Romance gender from English.\n"
        "4. **Cases/postpositions** — location and role via suffixes.\n"
        "5. **Formal te/On** patterns in work email.\n"
        "6. **Technical literals** exact.\n"
        "7. **Avoid English continuous tense calques**."
    ),
    "baltic": (
        "1. **Case system** — noun/adjective case matches role.\n"
        "2. **No articles** — definiteness from context.\n"
        "3. **Verb aspects** — completed vs ongoing where language marks it.\n"
        "4. **Formal address** in external work.\n"
        "5. **Natural SOV/SVO** per language norm.\n"
        "6. **Technical literals** exact.\n"
        "7. **Avoid Russian calques** unless overlay says otherwise."
    ),
    "celtic": (
        "1. **VSO tendency** — verb often early; do not force English order.\n"
        "2. **Mutation/lenition** — follow standard orthography; do not invent forms.\n"
        "3. **Formal sibh** — work external where applicable.\n"
        "4. **No English filler** — direct request in sentence 1.\n"
        "5. **Technical literals** exact.\n"
        "6. **Limited pack honesty** — stay conservative; ask if dialect unclear.\n"
        "7. **English loanwords** only when repo-normal."
    ),
    "ie_eu": (
        "1. **Case/preposition** — align with language norms.\n"
        "2. **Formal register** — external work uses respectful forms.\n"
        "3. **Natural word order** — not English pasted.\n"
        "4. **Technical literals** exact.\n"
        "5. **Avoid ancient/formal overload** in chat unless `baku`.\n"
        "6. **One overlay** at a time.\n"
        "7. **Ask** if Katharevousa vs Demotic (Greek) or similar split matters."
    ),
    "semitic": (
        "1. **Root patterns** — verbs from roots; do not invent broken forms.\n"
        "2. **Gender agreement** — verbs/adjectives agree with subject/object.\n"
        "3. **Definite article** — attach where language requires.\n"
        "4. **RTL script** — keep code LTR inside sentences.\n"
        "5. **Formal address** — external work respectful.\n"
        "6. **Technical literals** exact.\n"
        "7. **No dialect mix** without active overlay."
    ),
    "iranian": (
        "1. **SOV default** — verb final in main clauses.\n"
        "2. **Ezafe** — possession chains where required.\n"
        "3. **Formal شما** — work external.\n"
        "4. **Script** — Arabic/Persian script default; Roman only if user asked.\n"
        "5. **Technical literals** exact.\n"
        "6. **Umbrella honesty** — Kurdish: ask Kurmanji vs Sorani before thick prose.\n"
        "7. **No Arabic calque pile-up** in Persian unless user asked."
    ),
    "turkic": (
        "1. **Agglutination** — suffix order natural.\n"
        "2. **Vowel harmony** — front/back in suffixes.\n"
        "3. **SOV** — verb final.\n"
        "4. **Formal siz** — work external.\n"
        "5. **Technical literals** exact.\n"
        "6. **Latin/Cyrillic** — one script per message.\n"
        "7. **Avoid Russian calques** in Central Asian varieties."
    ),
    "mongolic": (
        "1. **SOV** — verb final.\n"
        "2. **Agglutinative suffixes** — natural order.\n"
        "3. **Formal ta** — work external.\n"
        "4. **Cyrillic/Mongolian script** — ask if unclear.\n"
        "5. **Technical literals** exact.\n"
        "6. **Limited overlay** — stay standard.\n"
        "7. **No invented dialect forms**."
    ),
    "kartvelian": (
        "1. **Ergativity awareness** — in past tense where applicable.\n"
        "2. **Postpositions** — not English preposition order.\n"
        "3. **Formal address** in external work.\n"
        "4. **Mkhedruli script** default.\n"
        "5. **Technical literals** exact.\n"
        "6. **Conservative forms** — no invented dialect.\n"
        "7. **Impact-first** sentence 1."
    ),
    "armenian": (
        "1. **Case suffixes** — align roles.\n"
        "2. **Formal դուք** — work external.\n"
        "3. **Armenian script** default.\n"
        "4. **Technical literals** exact.\n"
        "5. **Eastern/Western** — ask if user names region.\n"
        "6. **No Turkish/Russian calque soup**.\n"
        "7. **One overlay** at a time."
    ),
    "se_asian": (
        "1. **Classifier/noun** — use natural classifiers where required.\n"
        "2. **No tense calque** — aspect/time particles, not English past/future pasted.\n"
        "3. **Politeness particles** — sparingly in work (`ครับ/ค่ะ`, etc.).\n"
        "4. **Topic-comment** — topic first when natural.\n"
        "5. **Technical literals** exact.\n"
        "6. **Script** — native script default.\n"
        "7. **No Thai/Lao/Khmer mix** without user ask."
    ),
    "south_asian": (
        "1. **SOV** — verb final.\n"
        "2. **Postpositions** — location/role suffixes.\n"
        "3. **Honorific agreement** — formal verb forms in work.\n"
        "4. **Script** — native script default.\n"
        "5. **Technical literals** exact.\n"
        "6. **Limited packs** — Kashmiri: conservative; ask script/dialect.\n"
        "7. **No Hindi particle import** unless overlay allows."
    ),
    "sinitic": (
        "1. **Topic-comment** — topic before comment.\n"
        "2. **Aspect markers** — 了/过/咗 etc. per variety; not English tense pasted.\n"
        "3. **Cantonese ≠ Mandarin** — load `cantonese` pack, not `mandarin/zh-hk`.\n"
        "4. **Hokkien ≠ Mandarin** — separate pack; Minnan/Taiwanese overlay only.\n"
        "5. **Technical literals** exact.\n"
        "6. **Traditional/simplified** — match overlay/user.\n"
        "7. **No fake Canto particles** beyond overlay."
    ),
    "niger_congo": (
        "1. **Tone/mark orthography** — follow standard spelling; do not invent tone marks.\n"
        "2. **Noun class agreement** — where language requires.\n"
        "3. **Formal address** in external work.\n"
        "4. **Technical literals** exact.\n"
        "5. **Conservative register** — limited dialect invention.\n"
        "6. **Impact-first** sentence 1.\n"
        "7. **Ask** if country-specific variety matters."
    ),
    "cushitic": (
        "1. **SOV** — verb final.\n"
        "2. **Gender agreement** — where marked.\n"
        "3. **Latin script** default for Somali.\n"
        "4. **Technical literals** exact.\n"
        "5. **Formal tone** in external work.\n"
        "6. **No Arabic calque overload** unless user asked.\n"
        "7. **Conservative forms**."
    ),
    "indigenous": (
        "1. **Limited coverage honesty** — standard variety only; no invented dialect.\n"
        "2. **Ask region** — Quechua/Guarani have many varieties.\n"
        "3. **Technical literals** exact.\n"
        "4. **Impact-first** — clear status in sentence 1.\n"
        "5. **No folkloric caricature**.\n"
        "6. **Email/chat** focus; light marketing.\n"
        "7. **Defer to user** for community-preferred terms."
    ),
    "classical": (
        "1. **Classical grammar** — case endings and agreement.\n"
        "2. **Limited modern use** — email/chat/docs OK; marketing light.\n"
        "3. **No macaronic Latin-English** unless user asked.\n"
        "4. **Technical literals** may stay Latin/code.\n"
        "5. **Default `baku`** register.\n"
        "6. **No invented neo-Latin idioms**.\n"
        "7. **Honesty** — state classical register in modern context."
    ),
    "constructed": (
        "1. **Standard Esperanto grammar** — accusative -n, regular word-building.\n"
        "2. **Formal vi** — work external.\n"
        "3. **No English calques**.\n"
        "4. **Technical literals** exact.\n"
        "5. **Impact-first**.\n"
        "6. **No faux dialects**.\n"
        "7. **Community-neutral** tone."
    ),
    "isolate": (
        "1. **Ergativity** — Basque case/markers as standard.\n"
        "2. **No Spanish/French calque pile-up**.\n"
        "3. **Technical literals** exact.\n"
        "4. **Formal zu/berori** in external work.\n"
        "5. **Conservative forms**.\n"
        "6. **Ask** Euskara batua vs regional if unclear.\n"
        "7. **One overlay** at a time."
    ),
}

PACK_HEADER = """# {name} — language pack

**Status:** `validated`. Write as a careful coworker in {name}; **not** the author fingerprint unless user asked English/Indonesian.

## Load map

| User signal | Load |
|---|---|
| Everyday writing | `pack.md` + `registers.md` |
| Culture, transcreation, pronouns | also `culture.md` |
| Region / variety | also **one** overlay from `overlays/` |

## Honesty

{honesty}

## Default register

`{default_register}` unless the user or use case requests another.

## When to ask

{when_to_ask}
"""

REGISTERS_TMPL = """# {lang_id} registers

Three registers. Default is `{default_register}`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, academic — on request |
| Work | `profesional` | Email, docs, status updates — **default** for work |
| Casual | `santai` | Chat, explanations, everyday writing |

## Pronouns and address

{pronouns}

## Examples

### `baku` (formal)

- **Good:** {baku_good}
- **Bad:** {baku_bad}

### `profesional` (work)

- **Good:** {prof_good}
- **Bad:** {prof_bad}

### `santai` (casual)

- **Good:** {santai_good}
- **Bad:** {santai_bad}

## What casual is not

{casual_not}
"""

CULTURE_TMPL = """# {lang_id} culture and transcreation

Transcreation, not translation. Load when the user asks for cultural fit, ads, or regional colour.

## Address and pronouns

| Situation | Form | Notes |
|---|---|---|
| Work email | {work_addr} | Default respectful |
| Peer chat | {peer_addr} | Only when user already casual |

## Directness

- First sentence: impact or request; details next.
- Softening: one polite marker per request — not every line.

## Humor and taboo

- Safe: light understatement after facts are clear.
- Avoid: ethnicity/religion mockery, accent caricature in spelling.

## Do not copy from English corporate

- `leverage` / `kindly revert` / `hope this finds you well` calques
- Passive chains when active voice is natural
- Marketing hype without concrete proof

## Natural grammar

{natural_grammar}

## Dates, names, honorifics

- Date format: ISO or local norm with timezone for global teams
- Names: follow user/repo spelling; do not guess familiarity
- Honorifics: use when external formal context requires
"""

OVERLAY_TMPL = """# {overlay_id} — {name} standard

**Type:** `regional` | **Status:** `validated`

## When to load

`language: {lang_id}` + `regional_voice: {overlay_id}`. Default overlay for {name}.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| formal pronoun | Respectful work default | `tipis+` |
| polite softener | One request soften | `tipis` |

## Examples (bug explanation)

- {prof_example}

## Caps

- Standard {name} orthography; no dialect caricature.
- Technical literals (`API_TOKEN`, paths) unchanged.
- One overlay at a time.

## What NOT to mix

- Markers from another language pack without explicit user ask.

## Forbidden caricature

- Random English filler every sentence.
- Invented dialect spellings outside this overlay.
"""


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def save_registry(registry: dict) -> None:
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def honesty_text(lang_id: str, name: str, umbrella: bool, limited: bool) -> str:
    parts: list[str] = []
    if umbrella:
        parts.append(
            f"Umbrella label — ask which variety (Kurmanji vs Sorani, etc.) before drafting thick prose."
        )
    if limited:
        parts.append(
            f"Limited coverage — conservative standard {name}; do not invent regional dialect forms."
        )
    if lang_id == "hokkien":
        parts.append(
            "Separate from `mandarin` — use this pack for Minnan/Hokkien/Taiwanese. "
            "For Mandarin in Hong Kong, use `mandarin` + `zh-hk`."
        )
    if lang_id == "cantonese":
        parts.append(
            "Separate from `mandarin` — Cantonese/Yue grammar and lexicon. "
            "Do not route Cantonese requests to `mandarin`."
        )
    if lang_id == "latin":
        parts.append("Classical Latin for modern comms — default `baku`; state register honestly.")
    if not parts:
        parts.append(f"Standard {name}; load overlay `{lang_id}` default when region unspecified.")
    return " ".join(parts)


def when_to_ask(lang_id: str, umbrella: bool, limited: bool) -> str:
    lines = [
        "- Formal vs casual register unclear → default `profesional` for work email.",
        "- Script (native vs Roman) unclear → ask once.",
    ]
    if umbrella:
        lines.append("- User said only umbrella name → ask which variety before long draft.")
    if limited:
        lines.append("- Regional dialect named but not in overlay → ask or stay standard.")
    if lang_id in ("cantonese", "hokkien"):
        lines.append("- User asked Mandarin → switch to `mandarin` pack, not this one.")
    if lang_id == "latin":
        lines.append("- User wants Ecclesiastical vs Classical → ask once.")
    return "\n".join(lines)


def examples_for(lang_id: str, name: str) -> dict[str, str]:
    custom = EXAMPLES.get(lang_id, {})
    bad_en = "Service will be down Tuesday — English pasted without natural grammar."
    bad_corp = "Kindly revert regarding the token issue."
    bad_mix = f"Random dialect mix or English filler in every {name} sentence."
    return {
        "baku_good": custom.get("baku_good", f"[Formal {name} maintenance notice — use standard orthography.]"),
        "baku_bad": custom.get("baku_bad", bad_en),
        "prof_good": custom.get(
            "prof_good",
            f"`API_TOKEN` missing in `.env`; `loadConfig` returns `undefined`. Run `npm test -- config`.",
        ),
        "prof_bad": custom.get("prof_bad", bad_corp),
        "santai_good": custom.get(
            "santai_good",
            f"No `API_TOKEN` in `.env` — run `npm test -- config`.",
        ),
        "santai_bad": custom.get("santai_bad", bad_mix),
    }


def scaffold_language(lang_id: str, name: str, iso: str) -> None:
    dest = LANG_ROOT / lang_id
    if dest.exists():
        return
    shutil.copytree(TEMPLATE_ROOT, dest)
    replacements = {
        "{language_id}": lang_id,
        "{language_name}": name,
        "{status}": "validated",
        "{overlay_id}": "example",
        "{overlay_type}": "regional",
    }
    for path in dest.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for key, value in replacements.items():
            text = text.replace(key, value)
        path.write_text(text, encoding="utf-8")
    overlay_example = dest / "overlays" / "_overlay.md"
    if overlay_example.exists():
        overlay_example.unlink()


def fill_language(
    lang_id: str,
    name: str,
    iso: str,
    overlay_id: str,
    aliases: list[str],
    family: str,
    umbrella: bool,
    limited: bool,
    default_register: str,
) -> None:
    scaffold_language(lang_id, name, iso)
    ex = examples_for(lang_id, name)
    grammar = GRAMMAR.get(family, GRAMMAR["ie_eu"])

    pack = PACK_HEADER.format(
        name=name,
        honesty=honesty_text(lang_id, name, umbrella, limited),
        default_register=default_register,
        when_to_ask=when_to_ask(lang_id, umbrella, limited),
    )
    (LANG_ROOT / lang_id / "pack.md").write_text(pack, encoding="utf-8")

    registers = REGISTERS_TMPL.format(
        lang_id=lang_id,
        default_register=default_register,
        pronouns=f"Standard {name} pronouns — formal for external work; casual only when user set tone.",
        casual_not=f"- Not English sentence with one {name} word\n- Not slang quota in incident or customer email",
        **ex,
    )
    (LANG_ROOT / lang_id / "registers.md").write_text(registers, encoding="utf-8")

    culture = CULTURE_TMPL.format(
        lang_id=lang_id,
        work_addr="Formal/respectful second person",
        peer_addr="Informal second person when user already casual",
        natural_grammar=grammar,
    )
    (LANG_ROOT / lang_id / "culture.md").write_text(culture, encoding="utf-8")

    overlay_path = LANG_ROOT / lang_id / "overlays" / f"{overlay_id}.md"
    overlay_path.parent.mkdir(parents=True, exist_ok=True)
    overlay_path.write_text(
        OVERLAY_TMPL.format(
            overlay_id=overlay_id,
            lang_id=lang_id,
            name=name,
            prof_example=ex["prof_good"],
        ),
        encoding="utf-8",
    )

    registry = load_registry()
    languages = registry.setdefault("languages", [])
    entry = next((lang for lang in languages if lang.get("id") == lang_id), None)
    if entry is None:
        entry = {
            "id": lang_id,
            "iso": iso,
            "name": name,
            "aliases": aliases,
            "umbrella": umbrella,
            "support": {
                "status": "validated",
                "pack": f"references/languages/{lang_id}/pack.md",
            },
            "registers": ["baku", "profesional", "santai"],
            "speech_levels": [],
            "overlays": [],
        }
        languages.append(entry)
    else:
        entry["iso"] = iso
        entry["name"] = name
        entry["aliases"] = aliases
        entry["umbrella"] = umbrella
        entry["support"]["status"] = "validated"

    overlays = entry.setdefault("overlays", [])
    if not any(o.get("id") == overlay_id for o in overlays):
        overlays.append(
            {
                "id": overlay_id,
                "type": "regional",
                "status": "validated",
                "file": f"references/languages/{lang_id}/overlays/{overlay_id}.md",
            }
        )
    save_registry(registry)
    print(f"filled: {lang_id} (+ overlay {overlay_id})")


def main() -> int:
    for row in WAVE3:
        fill_language(*row)
    print(f"wave3 complete: {len(WAVE3)} languages")
    bulk_expand = SKILL_ROOT / "scripts" / "bulk_expand.py"
    result = subprocess.run([sys.executable, str(bulk_expand)], cwd=SKILL_ROOT)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
