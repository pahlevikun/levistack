#!/usr/bin/env python3
"""Promote all registry rows to validated and fill language pack files."""

from __future__ import annotations

import json
import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
LANG_ROOT = SKILL_ROOT / "references" / "languages"
REGISTRY = SKILL_ROOT / "references" / "registry.json"

PACK_HEADER = """# {name} — language pack

**Status:** `validated`. Write as a careful coworker in {name}; **not** the author fingerprint unless user asked English/Indonesian.

## Load map

| User signal | Load |
|---|---|
| Everyday writing | `pack.md` + `registers.md` |
| Culture, transcreation, pronouns | also `culture.md` |
| City, slang, mix, speech level | also **one** overlay from `overlays/` or `speech-levels.md` |

## Honesty

{honesty}

## Default register

`{default_register}` unless the user or use case requests another.

## When to ask

{when_to_ask}
"""

REGISTERS = """# {lang_id} registers

Three registers. Default is `santai`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, investor — on request |
| Work | `profesional` | Email, docs, LinkedIn — on request |
| Casual | `santai` | **Default**: chat, explanations, everyday writing |

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

CULTURE = """# {lang_id} culture and transcreation

Transcreation, not translation. Load when the user asks for cultural fit, ads, or regional colour.

## Address and pronouns

| Situation | Form | Notes |
|---|---|---|
| Work chat | {work_addr} | Do not guess closeness from a name |
| External / formal | {formal_addr} | |

## Directness

- First sentence job in this culture: {directness}
- Softening patterns: {softening}

## Humor and taboo

- Safe: {humor_safe}
- Avoid: {humor_avoid}

## Do not copy from English corporate

{no_copy}

## Natural grammar

{natural_grammar}

## Dates, names, honorifics

- Date format: {dates}
- Name order: {names}
- Honorifics: {honorifics}
"""

LANGUAGE_DATA: dict[str, dict[str, str]] = {
    "arabic": {
        "honesty": (
            "Umbrella label — ask MSA vs dialect (e.g. Egyptian `arz`) before drafting thick prose. "
            "Do not costume MSA with dialect particles."
        ),
        "when_to_ask": (
            "- User said only \"Arabic\" → ask Modern Standard vs which dialect.\n"
            "- Egyptian content → use `arz`, not `arabic`.\n"
            "- Script (Arabic vs Latin chat) unclear → ask once."
        ),
        "default_register": "profesional",
        "pronouns": "MSA: أنا / نحن for ownership; أنتَ/أنتِ or حضرتك in formal work. Dialect packs override pronouns.",
        "baku_good": "نود إبلاغكم بأن الخدمة ستتوقف للصيانة يوم الثلاثاء.",
        "baku_bad": "Hey team, the service will be down Tuesday — translated word order.",
        "prof_good": "السبب أن `API_TOKEN` غير موجود في `.env`. شغّل `npm test -- config`.",
        "prof_bad": "Kindly revert regarding the token issue.",
        "santai_good": "الـ token مش موجود في `.env` — جرّب `npm test -- config`.",
        "santai_bad": "Slang soup mixing dialect markers from three countries.",
        "casual_not": "- Not random dialect spelling without an active overlay\n- Not insulting forms in incident or review text",
        "work_addr": "First name + title on external; internal team may use given name",
        "formal_addr": "حضرتك / سيادة / titles per country",
        "directness": "State the point early; soften with formulaic respect, not vague warmup.",
        "softening": "لو سمحت، يُرجى — sparingly in work chat.",
        "humor_safe": "Light understatement in chat after the fact is delivered.",
        "humor_avoid": "Religion, politics, gendered insults, dialect mockery.",
        "no_copy": "- `hope this email finds you well` calques\n- English exclamation marketing\n- Fake \"Gulf corporate\" filler",
        "natural_grammar": (
            "1. **VSO in news/formal** — lead with verb in headlines; don't force English SVO.\n"
            "2. **Definite with ال** — attach ال to known entities; don't double-mark with \"the\".\n"
            "3. **Idafa for possession** — `مفتاح API` not `مفتاح ال API` unless naturalized.\n"
            "4. **Numbers with nouns** — agree gender where MSA requires; don't leave English ordinals.\n"
            "5. **لا negation** — `لا يوجد` for absence; avoid `مش` unless dialect overlay active.\n"
            "6. **Preposition calques** — `في .env` not `على .env` for location.\n"
            "7. **Passive for formal reports** — `تم إيقاف الخدمة` beats blaming \"the system\" vaguely."
        ),
        "dates": "Tuesday 16 Sep 2026 or locale day-month; include timezone for global teams.",
        "names": "Given + family; patronymic where relevant.",
        "honorifics": "Engineer / Dr / titles on first external contact.",
    },
    "bengali": {
        "honesty": "Write standard colloquial Bengali for work; ask West Bengal vs Bangladesh if lexicon matters.",
        "when_to_ask": "- Formal literary (সাধু) vs colloquial (চলিত) → ask for legal/official.\n- Script Latin vs Bengali → default Bengali script.",
        "default_register": "santai",
        "pronouns": "আমি / আমরা; তুমি (close) vs আপনি (work/respect).",
        "baku_good": "অনুগ্রহ করে জানানো যাচ্ছে যে পরিষেবাটি মঙ্গলবার রক্ষণাবেক্ষণের জন্য বন্ধ থাকবে।",
        "baku_bad": "Service will be down Tuesday — English pasted into Bengali script.",
        "prof_good": "`API_TOKEN` `.env`-এ নেই, তাই `loadConfig` `undefined` ফেরত দিচ্ছে।",
        "prof_bad": "Kindly revert your configuration.",
        "santai_good": "`API_TOKEN` `.env`-এ নেই — `npm test -- config` চালাও।",
        "santai_bad": "Random Kolkata/Dhaka slang mix without user ask.",
        "casual_not": "- Not Hindi particles in Bengali\n- Not English filler every sentence",
        "work_addr": "Name + আপনি on external; first name internal if user set tone",
        "formal_addr": "আপনি / শ্রী / শ্রীমতী",
        "directness": "Lead with cause or action; respect markers after the fact.",
        "softening": "যদি সম্ভব হয় — once, not every line.",
        "humor_safe": "Gentle self-deprecation after clear status.",
        "humor_avoid": "Caste, religion, regional slurs.",
        "no_copy": "- `game-changer` calques\n- English email warmup\n- Over-formal Sanskrit pile-up in chat",
        "natural_grammar": (
            "1. **SOV default** — object before verb: `আমি ফাইলটি পড়েছি`.\n"
            "2. **Postpositions** — `ফাইলে`, `টেবিলের উপর`; no English preposition order.\n"
            "3. **এ-খানে/ও-খানে** — location, not \"এই জায়গায় the file\".\n"
            "4. **Compound verbs** — `চালু করে দাও` for \"run it\"; not `রান করো` unless tech loan is repo norm.\n"
            "5. **Honorific agreement** — আপনি → verb honorific forms in formal.\n"
            "6. **না placement** — before the verb phrase being negated.\n"
            "7. **Classifiers** — use natural measure words, not English \"a\" inserted."
        ),
        "dates": "16 Sep 2026 or ১৬ সেপ্টেম্বর ২০২৬",
        "names": "Given + family; titles on formal.",
        "honorifics": "শ্রী/শ্রীমতী/ডাঃ as context requires.",
    },
    "urdu": {
        "honesty": "Default Nastaliq-ready prose; ask Pakistan vs India vocabulary if unclear.",
        "when_to_ask": "- Script: Urdu vs Roman Urdu chat.\n- Religious/formal register for official letters.",
        "default_register": "profesional",
        "pronouns": "میں / ہم; تم (close) vs آپ (respect).",
        "baku_good": "آگاہ کیا جاتا ہے کہ سروس منگل کو دیکھ بھال کے لیے بند رہے گی۔",
        "baku_bad": "The service will be down — English order in Urdu script.",
        "prof_good": "`API_TOKEN` `.env` میں نہیں ہے؛ `npm test -- config` چلائیں۔",
        "prof_bad": "Please revert the token kindly.",
        "santai_good": "`API_TOKEN` `.env` میں نہیں — `npm test -- config` چلا لو۔",
        "santai_bad": "Bollywood caricature or random Punjabi mix.",
        "casual_not": "- Not Hindi devanagari in Urdu task\n- Not Persian flourishes without context",
        "work_addr": "آپ + name on external",
        "formal_addr": "جناب / محترم",
        "directness": "Problem first; respectful close second.",
        "softening": "براہِ کرم — once in requests.",
        "humor_safe": "Dry observation after facts.",
        "humor_avoid": "Religion, ethnicity, gendered insults.",
        "no_copy": "- English corporate openers\n- Fake poetic Arabic filler in tech chat",
        "natural_grammar": (
            "1. **SOV** — `میں فائل پڑھتا ہوں`.\n"
            "2. **Postpositions** — `فائل میں`, `ٹیبل پر`.\n"
            "3. **ہے/ہیں agreement** — plural subjects need ہیں.\n"
            "4. **کر دینا compound** — `چلا دو` for \"run it\".\n"
            "5. **آپ verb forms** — honorific plural verb with آپ.\n"
            "6. **نہیں placement** — before main verb.\n"
            "7. **Ezāfa** — `API کا token` natural genitive."
        ),
        "dates": "16 Sep 2026",
        "names": "Given + family",
        "honorifics": "جناب / صاحب / صاحبہ",
    },
    "russian": {
        "honesty": "Use natural modern Russian; ты/вы is a real boundary — default вы in work.",
        "when_to_ask": "- ты vs вы if relationship unclear.\n- Belarus/Ukraine vocabulary — stay neutral Russian unless asked.",
        "default_register": "profesional",
        "pronouns": "я / мы; вы (work default); ты only when user signals close peer chat.",
        "baku_good": "Сообщаем, что во вторник сервис будет недоступен из‑за обслуживания.",
        "baku_bad": "Service will be down Tuesday — English calque.",
        "prof_good": "`API_TOKEN` нет в `.env`, поэтому `loadConfig` возвращает `undefined`.",
        "prof_bad": "Kindly revert the configuration.",
        "santai_good": "`API_TOKEN` в `.env` нет — запусти `npm test -- config`.",
        "santai_bad": "Fake mat or 90s slang in incident text.",
        "casual_not": "- Not ты to executives without signal\n- Not transliterated English every noun",
        "work_addr": "Имя + вы",
        "formal_addr": "Вы + surname or title",
        "directness": "First sentence = fact or ask.",
        "softening": "Пожалуйста, не могли бы вы — sparingly.",
        "humor_safe": "Understatement after clear diagnosis.",
        "humor_avoid": "Politics, war jokes, ethnic slurs.",
        "no_copy": "- `hope this finds you well`\n- `leverage` → используйте",
        "natural_grammar": (
            "1. **Flexible SVO** — keep natural case marking, don't drop cases.\n"
            "2. **Aspect** — perfective for completed fixes: `я исправил`.\n"
            "3. **Negation genitive** — `нет токена`, not `не есть`.\n"
            "4. **Preposition + case** — `в .env`, `на сервере`.\n"
            "5. **Impersonal** — `нужно запустить` for instructions.\n"
            "6. **Diminutives** — not in incident warnings.\n"
            "7. **Formal passive** — `было обнаружено` for reports."
        ),
        "dates": "16 сентября 2026 г.",
        "names": "Given + family; patronymic in very formal",
        "honorifics": "Уважаемый / title",
    },
    "german": {
        "honesty": "Default Hochdeutsch; du/Sie boundary — Sie in external work unless user says du.",
        "when_to_ask": "- du vs Sie\n- Swiss/Austrian vocabulary if user names region.",
        "default_register": "profesional",
        "pronouns": "ich / wir; Sie (work default); du when peer chat is explicit.",
        "baku_good": "Hiermit teilen wir mit, dass der Dienst am Dienstag wegen Wartung ausfällt.",
        "baku_bad": "The service will be down Tuesday — English pasted.",
        "prof_good": "`API_TOKEN` fehlt in `.env`, deshalb gibt `loadConfig` `undefined` zurück.",
        "prof_bad": "Please kindly revert.",
        "santai_good": "`API_TOKEN` fehlt in `.env` — starte `npm test -- config`.",
        "santai_bad": "Fake Bayerisch spelling without overlay.",
        "casual_not": "- Not du in customer email\n- Not English verbs unintegrated",
        "work_addr": "Sie + surname or first name per company culture",
        "formal_addr": "Sie + Herr/Frau + surname",
        "directness": "Lead with Nutzen or problem; details follow.",
        "softening": "Könnten Sie bitte — once.",
        "humor_safe": "Dry after facts.",
        "humor_avoid": "Nazi references, dialect mockery.",
        "no_copy": "- `circle back` → `wir melden uns`\n- `leverage` calques",
        "natural_grammar": (
            "1. **V2 in main clauses** — verb second after fronted object.\n"
            "2. **Subordinate verb-final** — `..., weil das Token fehlt`.\n"
            "3. **Capitalize nouns** — Token stays code; common nouns capitalized.\n"
            "4. **Compound nouns** — `API-Token` not `Token von API` if naturalized.\n"
            "5. **Sie agreement** — verb and possessives formal.\n"
            "6. **nicht placement** — before what it negates.\n"
            "7. **Imperative Sie** — `Bitte starten Sie` in work email."
        ),
        "dates": "16.09.2026 or Dienstag, 16. September 2026",
        "names": "Given + family",
        "honorifics": "Herr/Frau + surname",
    },
    "pcm": {
        "honesty": "Nigerian Pidgin is a language — not broken English. Write natural PCM; don't add error stigma.",
        "when_to_ask": "- Lagos vs Port Harcourt flavour if user cares.\n- Formal letter may need English instead — ask.",
        "default_register": "santai",
        "pronouns": "I / we; you; dem for they.",
        "baku_good": "We wan inform una say service go stop for maintenance on Tuesday.",
        "baku_bad": "Kindly revert regarding the maintenance window.",
        "prof_good": "`API_TOKEN` no dey for `.env`, so `loadConfig` dey return `undefined`.",
        "prof_bad": "The API_TOKEN is not present in the environment file — stiff translation.",
        "santai_good": "`API_TOKEN` no dey `.env` — run `npm test -- config`.",
        "santai_bad": "Mocking tone or fake Jamaican mix.",
        "casual_not": "- Not \"comedy African accent\" spelling\n- Not English corporate in PCM announcement",
        "work_addr": "First name; dey/you fine internally",
        "formal_addr": "Sir/Madam + clear PCM or offer English",
        "directness": "Say wetin happen first.",
        "softening": "abeg — light, not every line.",
        "humor_safe": "Light after serious news delivered.",
        "humor_avoid": "Tribal slurs, poverty jokes.",
        "no_copy": "- `hope this finds you well`\n- Forcing `-ing` on every verb",
        "natural_grammar": (
            "1. **No be for negation** — `e no dey work`.\n"
            "2. **dey for progressive** — `e dey run`.\n"
            "3. **wen/then sequence** — natural time order, not calque.\n"
            "4. **una/unu** — pick one audience form per message.\n"
            "5. **fit for ability** — `you fit run am`.\n"
            "6. **make for causative** — `make we check`.\n"
            "7. **No past tense overload** — context markers over English past forms."
        ),
        "dates": "Tuesday 16 Sep",
        "names": "Given names common",
        "honorifics": "Oga/Madam sparingly",
    },
    "arz": {
        "honesty": "Egyptian Arabic is not MSA with costume. Write natural Masri; don't mix Levant/Gulf without ask.",
        "when_to_ask": "- User said Arabic only → clarify MSA vs Egyptian.\n- Formal letter may need MSA — ask.",
        "default_register": "santai",
        "pronouns": "أنا / إحنا; انتَ/انتِ; حضرتك in polite work.",
        "baku_good": "بنحب نبلغكم إن الخدمة هتتوقف يوم التلات للصيانة.",
        "baku_bad": "MSA fossil with random Egyptian emoji tone.",
        "prof_good": "`API_TOKEN` مش موجود في `.env` — شغّل `npm test -- config`.",
        "prof_bad": "Kindly revert the token issue.",
        "santai_good": "الـ token مش في `.env` — جرّب `npm test -- config`.",
        "santai_bad": "Gulf/Khaleeji words in Cairo team chat without reason.",
        "casual_not": "- Not MSA في every casual line\n- Not insulting forms to user",
        "work_addr": "First name + light respect",
        "formal_addr": "حضرتك / أستاذ",
        "directness": "Point first; warmth in particles, not filler paragraphs.",
        "softening": "لو سمحت — light.",
        "humor_safe": "After status is clear.",
        "humor_avoid": "Politics, religion mockery.",
        "no_copy": "- English email openers\n- Fake \"Hollywood Arab\"",
        "natural_grammar": (
            "1. **مش negation** — not لا only in casual.\n"
            "2. **هو/هي pronoun copula** — `الخدمة واقفة`.\n"
            "3. **في for location** — `في .env`.\n"
            "4. **عايز/محتاج** — need/want distinction in requests.\n"
            "5. **Present continuous with بـ** — `بيشتغل`.\n"
            "6. **Question with إيه/ليه** — natural wh-words.\n"
            "7. **Don't paste MSA case endings** into casual chat."
        ),
        "dates": "التلات 16 سبتمبر",
        "names": "Given + family",
        "honorifics": "أستاذ / دكتور",
    },
    "marathi": {
        "honesty": "Colloquial Mumbai/Pune work Marathi default; literary संस्कृतनिष्ठ on ask.",
        "when_to_ask": "- Formal legal vs everyday.\n- Devanagari vs Roman — default Devanagari.",
        "default_register": "santai",
        "pronouns": "मी / आम्ही; तू (close) vs तुम्ही (work).",
        "baku_good": "कळविण्यात येते की मंगळवारी देखभालीसाठी सेवा बंद राहील.",
        "baku_bad": "Service down Tuesday — English order.",
        "prof_good": "`API_TOKEN` `.env` मध्ये नाही, म्हणून `loadConfig` `undefined` देतो.",
        "prof_bad": "Kindly revert configuration.",
        "santai_good": "`API_TOKEN` `.env` मध्ये नाही — `npm test -- config` चालव.",
        "santai_bad": "Hindi particles in Marathi.",
        "casual_not": "- Not Hindi mix without ask\n- Not overly Sanskrit in chat",
        "work_addr": "तुम्ही + name",
        "formal_addr": "श्री / तुम्ही",
        "directness": "Fact first.",
        "softening": "कृपया — once.",
        "humor_safe": "Gentle after facts.",
        "humor_avoid": "Caste, regional slurs.",
        "no_copy": "- English marketing calques",
        "natural_grammar": (
            "1. **SOV** — object before verb.\n"
            "2. **मध्ये/वर postpositions**.\n"
            "3. **नाही negation** — before verb phrase.\n"
            "4. **Honorific तुम्ही** verb forms.\n"
            "5. **करून द्या** causative for \"please run\".\n"
            "6. **ने ergative** in past transitive where natural.\n"
            "7. **Loan tech terms** — keep repo literals exact."
        ),
        "dates": "16 Sep 2026",
        "names": "Given + family",
        "honorifics": "श्री/श्रीमती",
    },
    "telugu": {
        "honesty": "Standard Telugu; ask region (AP vs Telangana) if vocabulary differs.",
        "when_to_ask": "- Formal ప్రామాణిక vs spoken.\n- Script vs Roman.",
        "default_register": "santai",
        "pronouns": "నేను / మేము; నువ్వు (close) vs మీరు (respect).",
        "baku_good": "మంగళవారం నిర్వహణ కారణంగా సేవ అందుబాటులో ఉండదని తెలియజేస్తున్నాం.",
        "baku_bad": "Service will be down — English pasted.",
        "prof_good": "`API_TOKEN` `.env` లో లేదు, కాబట్టి `loadConfig` `undefined` ఇస్తోంది.",
        "prof_bad": "Kindly revert.",
        "santai_good": "`API_TOKEN` `.env` లో లేదు — `npm test -- config` రన్ చేయి.",
        "santai_bad": "Random slang mix.",
        "casual_not": "- Not English every other word\n- Not Hindi in Telugu",
        "work_addr": "మీరు + name",
        "formal_addr": "మీరు / గారు",
        "directness": "Lead with issue.",
        "softening": "దయచేసి — sparingly.",
        "humor_safe": "Light after clear message.",
        "humor_avoid": "Caste, religion insults.",
        "no_copy": "- English corporate warmup",
        "natural_grammar": (
            "1. **SOV** word order.\n"
            "2. **లో/పై postpositions**.\n"
            "3. **లేదు negation**.\n"
            "4. **మీరు honorific verbs**.\n"
            "5. **చేయించు causative** for requests.\n"
            "6. **Agglutinative endings** — don't split naturally fused forms.\n"
            "7. **Keep code literals** unchanged."
        ),
        "dates": "16 Sep 2026",
        "names": "Given + family",
        "honorifics": "గారు suffix",
    },
    "swahili": {
        "honesty": "Standard Swahili (KI) for work; ask Kenya vs Tanzania lexicon if needed.",
        "when_to_ask": "- Regional slang (Sheng) only on explicit ask.\n- Very formal government letter → confirm register.",
        "default_register": "profesional",
        "pronouns": "mimi / sisi; wewe; wao.",
        "baku_good": "Tunafahamisha kwamba huduma itasimamishwa siku ya Jumanne kwa ajili ya matengenezo.",
        "baku_bad": "Service will be down Tuesday — English order.",
        "prof_good": "`API_TOKEN` haipo kwenye `.env`, kwa hiyo `loadConfig` inarudisha `undefined`.",
        "prof_bad": "Kindly revert.",
        "santai_good": "`API_TOKEN` haipo `.env` — endesha `npm test -- config`.",
        "santai_bad": "English nouns every word.",
        "casual_not": "- Not Sheng without ask\n- Not rude imperatives to seniors",
        "work_addr": "First name + polite verb",
        "formal_addr": "Bwana / Bi / title",
        "directness": "State habari (news) first.",
        "softening": "Tafadhali — once.",
        "humor_safe": "After facts.",
        "humor_avoid": "Tribal/ethnic jokes.",
        "no_copy": "- English email filler",
        "natural_grammar": (
            "1. **SVO default** — keep natural.\n"
            "2. **ni copula** — `ni undefined`.\n"
            "3. **ha- negation** on verbs.\n"
            "4. **kwenye for location** — `kwenye .env`.\n"
            "5. **Plenary subject prefixes** — a-, wa-, i- agreement.\n"
            "6. **Shauri for suggestions** — `tuendeshe test`.\n"
            "7. **Avoid English prepositions** calqued."
        ),
        "dates": "Jumanne 16 Sep 2026",
        "names": "Given + family",
        "honorifics": "Bwana/Bi",
    },
    "hausa": {
        "honesty": "Standard Hausa; Latin script default unless user asks Ajami.",
        "when_to_ask": "- Nigeria vs Niger vocabulary.\n- Highly formal religious register.",
        "default_register": "profesional",
        "pronouns": "ni / mu; kai (m) / ke (f); su.",
        "baku_good": "Muna sanar da cewa sabis zai tsaya ranar Talata don gyara.",
        "baku_bad": "Service will be down — English pasted.",
        "prof_good": "`API_TOKEN` ba ya cikin `.env`, don haka `loadConfig` yana dawo da `undefined`.",
        "prof_bad": "Kindly revert.",
        "santai_good": "`API_TOKEN` ba ya cikin `.env` — gudanar `npm test -- config`.",
        "santai_bad": "Fake accent spelling.",
        "casual_not": "- Not English every noun\n- Not religious insults",
        "work_addr": "Name + polite plural",
        "formal_addr": "Gwanin / title",
        "directness": "Lead with news.",
        "softening": "Don Allah — sparingly.",
        "humor_safe": "After clear status.",
        "humor_avoid": "Ethnic/religious slurs.",
        "no_copy": "- English corporate openers",
        "natural_grammar": (
            "1. **SVO basic** — subject focus early.\n"
            "2. **ba negation** — `ba ya aiki`.\n"
            "3. **a cikin for in** — `a cikin .env`.\n"
            "4. **Gender agreement** on kai/ke.\n"
            "5. **Imperative plural polite** — `mu yi` for let's.\n"
            "6. **Aspect markers** — `yana`, `ya` past.\n"
            "7. **Don't drop tone meaning** in minimal pairs when typing."
        ),
        "dates": "Talata 16 Sep 2026",
        "names": "Given + family",
        "honorifics": "Malam / title",
    },
    "turkish": {
        "honesty": "Modern Istanbul Turkish default; sen/siz boundary — siz in external work.",
        "when_to_ask": "- sen vs siz\n- Very formal legal wording.",
        "default_register": "profesional",
        "pronouns": "ben / biz; siz (work); sen when peer chat explicit.",
        "baku_good": "Salı günü bakım nedeniyle hizmetin duracağını bildiririz.",
        "baku_bad": "Service will be down Tuesday — English calque.",
        "prof_good": "`API_TOKEN` `.env` dosyasında yok; bu yüzden `loadConfig` `undefined` döndürüyor.",
        "prof_bad": "Kindly revert.",
        "santai_good": "`API_TOKEN` `.env`'de yok — `npm test -- config` çalıştır.",
        "santai_bad": "Aggressive slang to user.",
        "casual_not": "- Not sen in customer email\n- Not Ottoman flourishes in chat",
        "work_addr": "Siz + name",
        "formal_addr": "Siz + Bey/Hanım + surname",
        "directness": "First sentence = point.",
        "softening": "Lütfen — once.",
        "humor_safe": "Dry after facts.",
        "humor_avoid": "Ethnic slurs, politics.",
        "no_copy": "- `leverage` calques\n- English email warmup",
        "natural_grammar": (
            "1. **SOV** — verb final.\n"
            "2. **Agglutinative cases** — `.env`'de, not `.env in`.\n"
            "3. **Vowel harmony** — suffixes match stem.\n"
            "4. **yok for absence** — `token yok`.\n"
            "5. **Question mi particle** — `çalıştı mı?`.\n"
            "6. **Formal siz verbs**.\n"
            "7. **Keep code literals** Latin as-is."
        ),
        "dates": "16 Eylül 2026 Salı",
        "names": "Given + family",
        "honorifics": "Bey/Hanım",
    },
    "abui": {
        "honesty": (
            "Limited pack — Alor Island Abui. Use documented patterns; ask user for examples before kental variety. "
            "Offer Indonesian or English if forms are uncertain."
        ),
        "when_to_ask": "- Dialect within Abui → ask.\n- Any kental request without examples → ask or stay tipis.",
        "default_register": "profesional",
        "pronouns": "Documented 1sg/2sg forms from user examples; do not invent pronominal paradigms.",
        "baku_good": "Clear Indonesian bridge sentence if Abui form uncertain, plus ask for user's preferred phrasing.",
        "baku_bad": "Invented Abui words presented as fluent.",
        "prof_good": "State technical fact in simple Indonesian/English, note Abui limit, invite user's phrasing.",
        "prof_bad": "Fake dictionary entries.",
        "santai_good": "Thin Abui only from user examples; diagnosis stays clear.",
        "santai_bad": "Caricature or random Papuan mixing.",
        "casual_not": "- Not inventing morphology\n- Not mocking tone",
        "work_addr": "Follow user examples",
        "formal_addr": "Follow user examples",
        "directness": "Technical clarity first.",
        "softening": "From user examples only.",
        "humor_safe": "Only if user models it.",
        "humor_avoid": "Ethnic mockery.",
        "no_copy": "- Invented ritual speech\n- Indonesian dengan kata Abui random",
        "natural_grammar": (
            "1. **Do not invent** verb affixes or pronouns.\n"
            "2. **Follow user SVO** if they provide samples.\n"
            "3. **Keep technical terms** in repo language.\n"
            "4. **One clause per fact** when uncertain.\n"
            "5. **Ask for variety** before kental.\n"
            "6. **No particle soup** from other Papuan langs.\n"
            "7. **Honest bridge** to Indonesian/English beats fake fluency."
        ),
        "dates": "User locale",
        "names": "User preference",
        "honorifics": "Ask",
    },
    "dayak": {
        "honesty": (
            "Umbrella — Dayak languages are many. Ask Ngaju, Iban, Kenyah, etc. before drafting. "
            "Use `dayak-ngaju` when user confirms Ngaju."
        ),
        "when_to_ask": "- Always ask which Dayak language.\n- Do not pick from stereotype.",
        "default_register": "profesional",
        "pronouns": "Resolved per specific language pack after clarification.",
        "baku_good": "Satu kalimat klarifikasi: Dayak mana — Ngaju, Iban, atau lainnya?",
        "baku_bad": "Picking Ngaju without asking.",
        "prof_good": "Tanyakan bahasa Dayak spesifik sebelum menulis paragraf.",
        "prof_bad": "Campur aduk bahasa Kalimantan.",
        "santai_good": "Boleh sebut varietas Dayak yang kamu mau?",
        "santai_bad": "Invented \"Dayak\" words.",
        "casual_not": "- Not stereotype jungle talk\n- Not mixing unrelated languages",
        "work_addr": "After variety chosen",
        "formal_addr": "After variety chosen",
        "directness": "Clarify variety first.",
        "softening": "Indonesian polite ask OK while clarifying.",
        "humor_safe": "Not before variety is clear.",
        "humor_avoid": "Stereotypes about Kalimantan.",
        "no_copy": "- Fake \"tribal\" English\n- Random Indonesian dengan -lah",
        "natural_grammar": (
            "1. **Umbrella rule** — clarify before grammar.\n"
            "2. **No invented** Dayak lexicon.\n"
            "3. **Route to** `dayak-ngaju` or other packs when named.\n"
            "4. **Indonesian bridge** OK for clarification.\n"
            "5. **One question** not a lecture.\n"
            "6. **Respect** language names user gives.\n"
            "7. **Technical facts** stay accurate in any bridge language."
        ),
        "dates": "Per chosen variety",
        "names": "Per chosen variety",
        "honorifics": "Per chosen variety",
    },
    "dayak-ngaju": {
        "honesty": "Ngaju Dayak — thin pack; ask for examples before kental; don't invent sacred/register forms.",
        "when_to_ask": "- Subdialect; formal ritual register.",
        "default_register": "santai",
        "pronouns": "From user examples; default neutral if unknown.",
        "baku_good": "Kalimat jelas + minta contoh jika bentuk Ngaju belum pasti.",
        "baku_bad": "Ngaju palsu dari kamus imajiner.",
        "prof_good": "Fakta teknis jelas; bentuk Ngaju tipis atau dari contoh user.",
        "prof_bad": "Campur Banjar/Bugis random.",
        "santai_good": "Ngaju ringan hanya dari contoh user.",
        "santai_bad": "Stereotip \"suku Dayak\".",
        "casual_not": "- Not inventing\n- Not mock accent",
        "work_addr": "Nama + hormat ringan",
        "formal_addr": "Sesuai contoh user",
        "directness": "Fakta dulu.",
        "softening": "Dari contoh user.",
        "humor_safe": "Setelah fakta jelas.",
        "humor_avoid": "Stereotip.",
        "no_copy": "- Bahasa Indonesia dengan sufiks ngaju palsu",
        "natural_grammar": (
            "1. **Jangan mengarang** kata Ngaju.\n"
            "2. **Ikuti contoh user** untuk urutan kata.\n"
            "3. **Satu fakta per kalimat** jika ragu.\n"
            "4. **Tanya subdialek** sebelum kental.\n"
            "5. **Istilah teknis** tetap literal repo.\n"
            "6. **Jangan campur** bahasa Borneo lain.\n"
            "7. **Kejujuran** lebih baik dari pura-pura fasih."
        ),
        "dates": "Lokal user",
        "names": "Preferensi user",
        "honorifics": "Tanya jika perlu",
    },
    "atlantis": {
        "honesty": (
            "Honesty fixture — Atlantis is not a real language. Do not invent Atlantis vocabulary. "
            "Fall back to Indonesian or English and state the limit briefly."
        ),
        "when_to_ask": "- N/A — clarify that Atlantis is unsupported as a real variety.",
        "default_register": "profesional",
        "pronouns": "Use Indonesian/English fallback pronouns.",
        "baku_good": "Jelaskan batas: logat Atlantis tidak didukung; lanjut dalam Indonesia netral.",
        "baku_bad": "Invented Atlantis words.",
        "prof_good": "Same — honest fallback with clear technical content.",
        "prof_bad": "Fantasy language roleplay.",
        "santai_good": "Bahasa Indonesia netral setelah satu kalimat batas.",
        "santai_bad": "Fake Atlantis -sedang particles.",
        "casual_not": "- Not inventing\n- Not extended fantasy",
        "work_addr": "Indonesian/English",
        "formal_addr": "Indonesian/English",
        "directness": "State unsupported variety first sentence.",
        "softening": "Brief only.",
        "humor_safe": "Light ack that Atlantis was a joke request.",
        "humor_avoid": "Mocking user.",
        "no_copy": "- Invented Atlantis lexicon",
        "natural_grammar": (
            "1. **No invented** grammar.\n"
            "2. **Fallback** to Indonesian or English.\n"
            "3. **One sentence** limit statement.\n"
            "4. **Technical content** unchanged.\n"
            "5. **No particle** -sedang/-kental for Atlantis.\n"
            "6. **Do not extend** fantasy.\n"
            "7. **Offer** real language alternative."
        ),
        "dates": "N/A",
        "names": "N/A",
        "honorifics": "N/A",
    },
    "makassar": {
        "honesty": (
            "Makassarese language — not the same as Indonesian `regional_voice: makassar`. "
            "Use natural Makassar forms; ask variety before kental."
        ),
        "when_to_ask": "- Urban vs rural variety.\n- Mix with Indonesian only on ask.",
        "default_register": "santai",
        "pronouns": "ku / ta; ko for close 2sg — confirm in work external.",
        "baku_good": "Formal announcement in clear Makassar or Indonesian bridge if uncertain.",
        "baku_bad": "Sprinkling -mi -ki -ji without function.",
        "prof_good": "`API_TOKEN` ta' ada di `.env` — jalankan `npm test -- config`.",
        "prof_bad": "Indonesian dengan -mi di setiap kata.",
        "santai_good": "Satu partikel dengan fungsi jelas, bukan hiasan.",
        "santai_bad": "Ornamen Makassar palsu.",
        "casual_not": "- Not Indonesian overlay only\n- Not particle quota",
        "work_addr": "Name; polite 2p in external",
        "formal_addr": "Title + respectful form",
        "directness": "Fakta dulu.",
        "softening": "Partikel ringan, bukan banyak.",
        "humor_safe": "Setelah status jelas.",
        "humor_avoid": "Etnis.",
        "no_copy": "- -mi -ki -ji soup\n- Indonesian gaul as Makassar",
        "natural_grammar": (
            "1. **SOV tendencies** — follow natural Makassar order.\n"
            "2. **Particles -mi/-ki/-ji** — one job each, not every word.\n"
            "3. **ta' negation** — natural placement.\n"
            "4. **Don't confuse** with Bugis or Malay.\n"
            "5. **Technical terms** literal.\n"
            "6. **Ask variety** before kental.\n"
            "7. **Language ≠ regional_voice** on Indonesian."
        ),
        "dates": "Lokal",
        "names": "Given + family",
        "honorifics": "Daeng / title when formal",
    },
    "minangkabau": {
        "honesty": "Minangkabau — ask Agam/Pariaman/etc. before kental; don't invent dialect forms.",
        "when_to_ask": "- Dialect; formal adat register.",
        "default_register": "santai",
        "pronouns": "ambo / awak / sanak — register-dependent; default polite work forms.",
        "baku_good": "Pengumuman resmi dengan bentuk hormat Minang yang jelas.",
        "baku_bad": "Campur Jakarta gaul.",
        "prof_good": "`API_TOKEN` indak ado di `.env` — jalankan `npm test -- config`.",
        "prof_bad": "Indonesian dengan -lah random.",
        "santai_good": "Minang ringan; partikel dengan fungsi.",
        "santai_bad": "Kental tanpa varietas.",
        "casual_not": "- Not gue/lo\n- Not kental without variety",
        "work_addr": "Nama + hormat",
        "formal_addr": "Bapak/Ibu",
        "directness": "Intention kalimat pertama.",
        "softening": "Mintak — sparingly.",
        "humor_safe": "Setelah fakta.",
        "humor_avoid": "Stereotip Padang.",
        "no_copy": "- Indonesian particles default\n- Fake dialect soup",
        "natural_grammar": (
            "1. **indak negation** — not tidak default.\n"
            "2. **ambo/awak** — pick register-appropriate.\n"
            "3. **SOV flexible** — natural Minang order.\n"
            "4. **Ask dialect** before kental.\n"
            "5. **Partikel** pun/job clear.\n"
            "6. **Don't mix** Malay or Indonesian gaul.\n"
            "7. **Repo literals** exact."
        ),
        "dates": "Lokal",
        "names": "Given + clan where relevant",
        "honorifics": "Bapak/Ibu",
    },
    "jawa": {
        "honesty": "Speech levels are boundaries — ngoko is not swearing. Don't mix rek/ik/je subvarieties.",
        "when_to_ask": "- ngoko vs krama vs madya.\n- Sub-region (Banyumas vs Solo) before kental.",
        "default_register": "santai",
        "pronouns": "aku/kowe (ngoko); kula/sampéyan (krama) — level first.",
        "baku_good": "Krama ingkang leres kangge pengumuman resmi.",
        "baku_bad": "Ngoko in investor letter.",
        "prof_good": "Kula nyuwun dipun paringi pitulung — `API_TOKEN` mboten wonten ing `.env`.",
        "prof_bad": "Campur rek + kula + je.",
        "santai_good": "Ngoko alus: tokené ora ana ing `.env`.",
        "santai_bad": "Ngoko dianggep makian.",
        "casual_not": "- Not mixing levels\n- Not Indonesian particles as Jawa",
        "work_addr": "Level determines pronoun",
        "formal_addr": "krama + panjenengan",
        "directness": "Fakta ing ngarep.",
        "softening": "Monggo — in krama.",
        "humor_safe": "After clear status.",
        "humor_avoid": "Mocking ngoko.",
        "no_copy": "- Indonesian gaul as Jawa\n- rek+ik+je soup",
        "natural_grammar": (
            "1. **Level locks pronoun** — don't swap mid-message.\n"
            "2. **ngoko ≠ rude** by default.\n"
            "3. **-né/-e possession** — natural placement.\n"
            "4. **ora negation** in ngoko.\n"
            "5. **mboten in krama**.\n"
            "6. **One subvariety** per message.\n"
            "7. **Technical terms** literal."
        ),
        "dates": "Lokal",
        "names": "Given + respect level",
        "honorifics": "Mas/Mbak in Indonesian bridge only if asked",
    },
    "sunda": {
        "honesty": "loma vs cohag/kasar pisan — ask when user says kasar. Not insulting user.",
        "when_to_ask": "- Sunda kasar → loma or cohag?\n- Formal halus register.",
        "default_register": "santai",
        "pronouns": "abdi/saéndén (polite); manéh/érang by level.",
        "baku_good": "Basa hormat keur surat resmi.",
        "baku_bad": "Cohag keur klien éksternal tanpa sinyal.",
        "prof_good": "`API_TOKEN` teu aya di `.env` — jalankan `npm test -- config`.",
        "prof_bad": "Campur Jawa rek.",
        "santai_good": "Loma: tokenna teu aya di `.env`.",
        "santai_bad": "Ngina ka pamaké.",
        "casual_not": "- Not cohag without ask\n- Not Jawa mix",
        "work_addr": "Level picks pronoun",
        "formal_addr": "Basa hormat",
        "directness": "Fakta heula.",
        "softening": "Punten — sparingly.",
        "humor_safe": "Sanggeus fakta.",
        "humor_avoid": "Hinaan.",
        "no_copy": "- Jawa particles\n- Indonesian gaul default",
        "natural_grammar": (
            "1. **teu negation**.\n"
            "2. **loma vs cohag** social meaning.\n"
            "3. **di/de locative** — natural.\n"
            "4. **Don't insult** in cohag to user.\n"
            "5. **One level** per message.\n"
            "6. **Ask kasar** ambiguity.\n"
            "7. **Technical literal**."
        ),
        "dates": "Lokal",
        "names": "Given",
        "honorifics": "Aang/teh in casual if natural",
    },
    "bali": {
        "honesty": "alus/madia/kasar ≠ Jawa krama/ngoko. Don't import Javanese forms.",
        "when_to_ask": "- speech_level: alus/madia/kasar.\n- Ceremony vs everyday.",
        "default_register": "santai",
        "pronouns": "tiang/ida (alus); titiang/cang (madia); by level.",
        "baku_good": "Alus sing patut keur pengumuman resmi.",
        "baku_bad": "Ngoko Jawa in Bali text.",
        "prof_good": "`API_TOKEN` nenten wénten ring `.env` — antosang `npm test -- config`.",
        "prof_bad": "Campur krama Jawa.",
        "santai_good": "Madia: tokené ten wénten ring `.env`.",
        "santai_bad": "Kasar without context.",
        "casual_not": "- Not Jawa levels\n- Not particle soup",
        "work_addr": "Level-based",
        "formal_addr": "alus pronouns",
        "directness": "Fakta dulu.",
        "softening": "Mangkin — light.",
        "humor_safe": "After facts.",
        "humor_avoid": "Sacred mockery.",
        "no_copy": "- Jawa krama\n- Indonesian gaul as Bali",
        "natural_grammar": (
            "1. **alus/madia/kasar** locks forms.\n"
            "2. **nenten/ten negation** by level.\n"
            "3. **ring locative** — not di default.\n"
            "4. **No Jawa rek/ik**.\n"
            "5. **Ceremony register** only when asked.\n"
            "6. **One level** per message.\n"
            "7. **Technical literal**."
        ),
        "dates": "Lokal",
        "names": "Given",
        "honorifics": "I Gusti etc. when formal",
    },
}


def promote_registry() -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for lang in data["languages"]:
        lang["support"]["status"] = "validated"
        for overlay in lang.get("overlays") or []:
            overlay["status"] = "validated"
    for uc in data["usecases"]:
        uc["status"] = "validated"
    REGISTRY.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data


def write_language_files(lang_id: str, name: str, data: dict[str, str]) -> None:
    lang_dir = LANG_ROOT / lang_id
    lang_dir.mkdir(parents=True, exist_ok=True)

    pack = PACK_HEADER.format(
        name=name,
        honesty=data["honesty"],
        when_to_ask=data["when_to_ask"],
        default_register=data["default_register"],
    )
    (lang_dir / "pack.md").write_text(pack, encoding="utf-8")

    registers = REGISTERS.format(lang_id=lang_id, **data)
    (lang_dir / "registers.md").write_text(registers, encoding="utf-8")

    culture = CULTURE.format(lang_id=lang_id, **data)
    (lang_dir / "culture.md").write_text(culture, encoding="utf-8")


def update_pack_status(path: Path) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\*\*Status:\*\* `(?:beta|catalogued)`", "**Status:** `validated`", text)
    text = re.sub(
        r"- `catalogued`:.*\n- `beta`:.*\n- `validated`:.*",
        "- `validated`: load full pack; still no caricature or slang quota.",
        text,
    )
    text = text.replace(
        "Thin writing unless user gives examples. Cap `intensity` at `sedang` without variety.",
        "Cap `intensity` at `sedang` without user examples or named variety.",
    )
    text = text.replace(
        "are not loaded until status is `beta` or `validated`.",
        "are loaded per registry when active.",
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    registry = promote_registry()
    id_to_name = {lang["id"]: lang["name"] for lang in registry["languages"]}

    for lang_id, data in LANGUAGE_DATA.items():
        write_language_files(lang_id, id_to_name.get(lang_id, lang_id), data)

    for lang in registry["languages"]:
        pack_path = SKILL_ROOT / lang["support"]["pack"]
        update_pack_status(pack_path)
        for overlay in lang.get("overlays") or []:
            overlay_path = SKILL_ROOT / overlay["file"]
            update_pack_status(overlay_path)

    print(f"Promoted registry; filled/updated {len(LANGUAGE_DATA)} language packs.")


if __name__ == "__main__":
    main()
