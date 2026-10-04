#!/usr/bin/env python3
"""Generate regional dialect overlay files and registry entries for polyglot-copywriter."""

from __future__ import annotations

import json
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = SKILL_ROOT / "references" / "registry.json"

# overlay_id -> markdown body (without front header line; script adds standard header)
OVERLAYS: dict[str, list[dict]] = {
    "japanese": [
        {
            "id": "tokyo",
            "type": "regional",
            "title": "Tokyo / Standard Japanese",
            "when": "`language: japanese` + `regional_voice: tokyo` (or `netral` default for regional). Hyōjungo baseline for national media and most workplaces.",
            "jobs": [
                ("です／ます", "Polite work default; statement + soft close", "tipis+"),
                ("だ／である", "Plain explanatory prose in technical docs when register is santai", "sedang+"),
                ("〜んです", "Explains cause gently in spoken-style explanation", "sedang+"),
                ("〜と思います", "Modest technical claim; caps overconfidence", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` が `.env` にないので、`loadConfig` が `undefined` を返しています。`npm test -- config` を試してください。",
                "設定ファイルにトークンが入っていないのが原因だと思います。",
            ],
            "caps": [
                "Default regional overlay — do not mix 関西弁 markers in the same sentence unless user asked.",
                "Keigo depth stays in `speech-levels.md`, not this overlay.",
                "No anime catchphrases or mascot slang.",
            ],
            "forbidden": "関西の やねん／へん／あかん in Tokyo-standard output.",
        },
        {
            "id": "kansai",
            "type": "regional",
            "title": "Kansai (Osaka-area) Japanese",
            "when": "`language: japanese` + `regional_voice: kansai`. Osaka–Kyoto conversational grammar — not comedy caricature.",
            "jobs": [
                ("〜や", "Predicate copula instead of だ (plain); states what something is", "tipis+"),
                ("〜やねん", "Explains cause/reason with Kansai assertive nuance", "sedang+"),
                ("〜へん", "Negative (しない → せえへん／しへん); denial of state", "sedang+"),
                ("あかん", "「だめ」— cannot proceed; blocks action", "sedang+"),
                ("〜ねん", "Sentence-final emphasis on explanation", "tipis+"),
                ("おおきに", "Thanks (casual Kansai); not in every sentence", "tipis"),
            ],
            "examples": [
                "`.env` に `API_TOKEN` が入ってへんから、`loadConfig` が `undefined` 返してるねん。`npm test -- config` 試してみて。",
                "設定ミスやねん。トークン足りてへん。",
            ],
            "caps": [
                "Pick one Kansai grammar lane per sentence — do not stack やねん + へん + あかん.",
                "Do not mix です／ます polite chain with heavy Kansai copula in one sentence without user ask.",
                "Cap at `sedang` without user examples; `kental` only with explicit request.",
            ],
            "forbidden": "Exaggerated comedy accent, random めっちゃ spam, Tokyo です／ます in same clause as やねん.",
        },
        {
            "id": "tohoku",
            "type": "regional",
            "title": "Tohoku Japanese (light)",
            "when": "`language: japanese` + `regional_voice: tohoku`. Light northeastern colour for casual explanation — thin overlay.",
            "jobs": [
                ("〜べ／〜べさ", "Soft assertion or shared reminder (dialectal sentence tail)", "tipis"),
                ("〜だべ", "Guess/soft conclusion about cause", "tipis"),
                ("〜けっぺ", "Casual 'so anyway / therefore' connector (very light)", "tipis"),
            ],
            "examples": [
                "`.env` に `API_TOKEN` ないけっぺ、`loadConfig` が `undefined` になるだべ。",
            ],
            "caps": [
                "Light touch only — one marker per paragraph at `tipis`.",
                "Do not invent heavy rural stereotype vocabulary.",
            ],
            "forbidden": "Phonetic parody spelling; stacking multiple Tohoku tails in one sentence.",
        },
        {
            "id": "kyushu",
            "type": "regional",
            "title": "Kyushu Japanese (light)",
            "when": "`language: japanese` + `regional_voice: kyushu`. Light southern colour — thin overlay.",
            "jobs": [
                ("〜と／〜っと", "Casual quotative / 'I mean' (Fukuoka-area spoken)", "tipis"),
                ("〜ばい／〜たい", "Light sentence tail for emphasis (use sparingly)", "tipis"),
                ("〜けん", "Because/so (Kyushu causal; not every sentence)", "tipis"),
            ],
            "examples": [
                "`.env` にトークンがないけん、`loadConfig` が `undefined` になっと。",
            ],
            "caps": [
                "Thin overlay — prefer standard grammar with at most one southern marker per paragraph.",
                "No TV stereotype accent writing.",
            ],
            "forbidden": "Heavy Tokyo keigo mixed with faux Kyushu every line.",
        },
    ],
    "korean": [
        {
            "id": "seoul",
            "type": "regional",
            "title": "Seoul / Standard Korean",
            "when": "`language: korean` + `regional_voice: seoul`. Gyeonggi-Seoul baseline for work and national media.",
            "jobs": [
                ("-요／-습니다", "Polite work default (pairs with jondaetmal speech level)", "tipis+"),
                ("-네요", "Notices state change; gentle diagnostic tone", "tipis+"),
                ("-거든요", "Background reason for the bug", "sedang+"),
            ],
            "examples": [
                "`.env`에 `API_TOKEN`이 없어서 `loadConfig`가 `undefined`를 반환합니다. `npm test -- config`를 실행해 보세요.",
            ],
            "caps": ["Default regional — do not mix Gyeongsang sentence tails without user ask."],
            "forbidden": "Busan -노/-나 every sentence in Seoul-standard output.",
        },
        {
            "id": "busan",
            "type": "regional",
            "title": "Busan / Gyeongsang Korean",
            "when": "`language: korean` + `regional_voice: busan`. Southeastern grammar — direct, not caricature.",
            "jobs": [
                ("-노／-나", "Sentence-final emphasis (assertion/check)", "sedang+"),
                ("-데이", "Soft explanation tail (spoken Gyeongsang)", "tipis+"),
                ("안 된다 → 안 되나", "Spoken negative with regional tail", "sedang+"),
                ("그라", "「그래」— agreement/acknowledgment", "tipis+"),
            ],
            "examples": [
                "`.env`에 `API_TOKEN` 없으니 `loadConfig`가 `undefined` 나오나. `npm test -- config` 해봐라.",
            ],
            "caps": [
                "One Gyeongsang tail per sentence at `sedang`.",
                "Do not mix Seoul-only formal chain with heavy -노 in same clause.",
            ],
            "forbidden": "Random 사투리 words without pragmatic job.",
        },
        {
            "id": "jeolla",
            "type": "regional",
            "title": "Jeolla Korean (light)",
            "when": "`language: korean` + `regional_voice: jeolla`. Southwestern colour — thin overlay.",
            "jobs": [
                ("-잉／-당", "Light sentence tail (Jeolla spoken)", "tipis"),
                ("-것네", "Soft observation about state", "tipis"),
            ],
            "examples": [
                "`.env`에 토큰 없당, `loadConfig`가 `undefined` 나오것네.",
            ],
            "caps": ["Thin — max one marker per paragraph at `tipis`."],
            "forbidden": "Heavy Gyeongsang -노 mixed with Jeolla tails in one sentence.",
        },
    ],
    "mandarin": [
        {
            "id": "zh-sg",
            "type": "regional",
            "title": "Singapore Mandarin",
            "when": "`language: mandarin` + `regional_voice: zh-sg`. Singapore Mandarin with local lexical choices.",
            "jobs": [
                ("Simplified + SG lexicon", "软件、视频、程序 — SG usage", "tipis+"),
                ("吗 → 吗/呢", "Question particle as in local spoken Mandarin", "tipis+"),
                ("先", "Do X first (spoken instruction ordering)", "tipis+"),
            ],
            "examples": [
                "`.env` 里没有 `API_TOKEN`，所以 `loadConfig` 返回 `undefined`。先跑 `npm test -- config` 试试。",
            ],
            "caps": ["Singlish particles (lah/leh) belong in `english/singlish` mix, not this overlay."],
            "forbidden": "lah/leh in Mandarin sentences unless user asked Singlish mix.",
        },
        {
            "id": "zh-hk",
            "type": "regional",
            "title": "Hong Kong Mandarin (written)",
            "when": "`language: mandarin` + `regional_voice: zh-hk`. Mandarin for HK readers — **Cantonese is a separate language**.",
            "jobs": [
                ("HK lexical choices in Mandarin", "程序、软件 — HK preference in Mandarin prose", "tipis+"),
                ("请／麻烦", "Polite request framing common in HK service tone", "tipis+"),
            ],
            "examples": [
                "`.env` 缺少 `API_TOKEN`，`loadConfig` 因此返回 `undefined`。麻烦先执行 `npm test -- config`。",
            ],
            "caps": [
                "This is Mandarin for HK context, not Cantonese.",
                "If user wants Cantonese, say it is not in registry as `mandarin`.",
            ],
            "forbidden": "Cantonese characters/grammar presented as Mandarin.",
        },
    ],
    "hindi": [
        {
            "id": "hi-standard",
            "type": "regional",
            "title": "Standard Hindi (Delhi / national)",
            "when": "`language: hindi` + `regional_voice: hi-standard` or `netral`. Khari Boli baseline for work.",
            "jobs": [
                ("है／हैं", "Present state copula", "tipis+"),
                ("नहीं", "Negation — clear diagnostic", "tipis+"),
                ("इसलिए", "Therefore — cause link", "tipis+"),
            ],
            "examples": [
                "`.env` में `API_TOKEN` नहीं है, इसलिए `loadConfig` `undefined` लौटा रहा है। `npm test -- config` चलाएँ।",
            ],
            "caps": ["Default Hindi regional — Hinglish is separate mix overlay."],
            "forbidden": "Random English insertions (Hinglish) without mix overlay.",
        },
        {
            "id": "haryanvi",
            "type": "regional",
            "title": "Haryanvi-influenced Hindi (light)",
            "when": "`language: hindi` + `regional_voice: haryanvi`. Light Haryana colour in Hindi prose.",
            "jobs": [
                ("सै／है", "Spoken copula flavour (light)", "tipis"),
                ("नै", "Negation variant (light, not every line)", "tipis"),
                ("के", "Casual connector 'because/so'", "tipis"),
            ],
            "examples": [
                "`.env` में `API_TOKEN` नै सै, इसलिए `loadConfig` `undefined` दे रहा सै।",
            ],
            "caps": ["Thin overlay — one regional form per sentence at `tipis`."],
            "forbidden": "Heavy stereotype comedy; full Haryanvi lexicon inventing.",
        },
        {
            "id": "mumbai-hindi",
            "type": "regional",
            "title": "Mumbai urban Hindi",
            "when": "`language: hindi` + `regional_voice: mumbai-hindi`. Urban Mumbai Hindi — conversational, not Bollywood pastiche.",
            "jobs": [
                ("यार", "Peer softener (only if casual register)", "sedang+"),
                ("ना", "Tag seeking agreement on diagnosis", "tipis+"),
                ("बस", "That's the issue / limit statement", "tipis+"),
                ("ठीक है", "Close with next step", "tipis+"),
            ],
            "examples": [
                "`.env` में `API_TOKEN` नहीं है ना, इसलिए `loadConfig` `undefined` दे रहा है। `npm test -- config` चला लो।",
            ],
            "caps": ["No forced yaaar every sentence."],
            "forbidden": "Bollywood catchphrases; Hinglish unless `hinglish` mix asked.",
        },
    ],
    "spanish": [
        {
            "id": "es-ar",
            "type": "regional",
            "title": "Argentina Spanish",
            "when": "`language: spanish` + `regional_voice: es-ar`. Rioplatense voseo for casual; usted for formal work.",
            "jobs": [
                ("vos + verb", "Casual address when register is santai", "sedang+"),
                ("usted", "External/formal work email", "tipis+"),
                ("che", "Peer attention (casual only, rare)", "sedang+"),
                ("acá／aquí", "Local deictic preference", "tipis+"),
            ],
            "examples": [
                "Falta `API_TOKEN` en `.env`, por eso `loadConfig` devuelve `undefined`. Probá `npm test -- config`.",
            ],
            "caps": ["Match tú/usted/vos to register and audience."],
            "forbidden": "Spain vosotros default; che in formal client email.",
        },
        {
            "id": "es-co",
            "type": "regional",
            "title": "Colombia Spanish",
            "when": "`language: spanish` + `regional_voice: es-co`. Colombian Spanish — polite default, clear work tone.",
            "jobs": [
                ("usted", "Default polite for work unless user asked casual tú", "tipis+"),
                ("por favor／si puede", "Softener on requests", "tipis+"),
                ("listo", "Acknowledgment / ready to proceed", "tipis+"),
                ("entonces", "Therefore in explanation", "tipis+"),
            ],
            "examples": [
                "No está `API_TOKEN` en `.env`, entonces `loadConfig` devuelve `undefined`. Ejecute `npm test -- config`, por favor.",
            ],
            "caps": ["Do not use Mexico-only slang as default."],
            "forbidden": "Random voseo unless user asked Argentine-style.",
        },
    ],
    "arabic": [
        {
            "id": "arabic-egyptian",
            "type": "regional",
            "title": "Egyptian Arabic (MSA umbrella note)",
            "when": "`language: arabic` + `regional_voice: arabic-egyptian`. **Umbrella honesty:** for full Egyptian, prefer `language: arz`.",
            "jobs": [
                ("في", "Locative 'in' (Egyptian/Levant shared in dialect)", "tipis+"),
                ("مش", "Negation (dialect-informed explanation in Arabic script)", "sedang+"),
                ("يعني", "Clarifies cause in spoken explanation", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` مش موجود في `.env`، يعني `loadConfig` بيرجع `undefined`. جرّب `npm test -- config`.",
            ],
            "caps": [
                "Umbrella `arabic` pack — state limit; offer `arz` for sustained Egyptian.",
                "Do not claim full native coverage from thin list.",
            ],
            "forbidden": "Inventing dialect words without pragmatic job.",
        },
        {
            "id": "arabic-levantine",
            "type": "regional",
            "title": "Levantine Arabic (umbrella)",
            "when": "`language: arabic` + `regional_voice: arabic-levantine`. Levant-informed — umbrella honesty applies.",
            "jobs": [
                ("ما … مش", "Double negation pattern (light)", "tipis+"),
                ("هلق", "Now/then connector (Levant spoken)", "tipis"),
                ("يعني", "Explains implication", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` مش موجود بـ`.env`، يعني `loadConfig` عم يرجّع `undefined`.",
            ],
            "caps": ["Thin overlay under umbrella `arabic`; ask for user example for `kental`."],
            "forbidden": "Mixing Egyptian and Levant tails in one sentence.",
        },
        {
            "id": "arabic-gulf",
            "type": "regional",
            "title": "Gulf Arabic (umbrella)",
            "when": "`language: arabic` + `regional_voice: arabic-gulf`. Gulf-informed — umbrella honesty applies.",
            "jobs": [
                ("ما في", "There is not (Gulf spoken pattern)", "tipis+"),
                ("بعد", "Still/yet in diagnostic", "tipis+"),
                ("لازم", "Must/need to — next step", "tipis+"),
            ],
            "examples": [
                "ما في `API_TOKEN` بـ`.env`، لازم تشغّل `npm test -- config`.",
            ],
            "caps": ["Umbrella honesty — offer MSA-neutral or user example if forms thin."],
            "forbidden": "Levant/Egyptian markers in Gulf-labelled output.",
        },
    ],
    "french": [
        {
            "id": "fr-ca",
            "type": "regional",
            "title": "Canadian French",
            "when": "`language: french` + `regional_voice: fr-ca`. Québec/Canada lexicon and informatics terms.",
            "jobs": [
                ("tu (informal)", "Casual peer when register is santai", "sedang+"),
                ("courriel", "Email (Canada)", "tipis+"),
                ("fin de semaine", "Weekend (not week-end France)", "tipis+"),
                ("magasiner", "Browse/shop — avoid in tech unless relevant", "tipis"),
            ],
            "examples": [
                "Il manque `API_TOKEN` dans `.env`, donc `loadConfig` retourne `undefined`. Lance `npm test -- config`.",
            ],
            "caps": ["Do not use France-only terms as default (e.g. e-mail vs courriel)."],
            "forbidden": "France tu/vous assumptions for Canadian formal client without check.",
        },
        {
            "id": "fr-be",
            "type": "regional",
            "title": "Belgian French",
            "when": "`language: french` + `regional_voice: fr-be`. Belgium French — thin lexical overlay.",
            "jobs": [
                ("septante/nonante", "70/90 (Belgium) — only if numbers matter", "tipis"),
                ("à tantôt", "See you soon (Belgium)", "tipis"),
                ("standard vous", "Work default polite", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` manque dans `.env`, donc `loadConfig` renvoie `undefined`. Exécutez `npm test -- config`.",
            ],
            "caps": ["Thin overlay — Belgium lexicon only when relevant."],
            "forbidden": "Inventing Belgicism every sentence.",
        },
        {
            "id": "fr-af",
            "type": "regional",
            "title": "African French (broad)",
            "when": "`language: french` + `regional_voice: fr-af`. Broad Sub-Saharan African French — **honesty: not one monolith**.",
            "jobs": [
                ("on", "We/one — inclusive team voice", "tipis+"),
                ("merci de", "Polite request frame", "tipis+"),
                ("du coup", "Therefore/so (spoken link)", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` n'est pas dans `.env`, du coup `loadConfig` retourne `undefined`. Merci de lancer `npm test -- config`.",
            ],
            "caps": [
                "Broad overlay — do not claim one country.",
                "Ask country if user needs local colour at `kental`.",
            ],
            "forbidden": "Stereotype inventing; mixing Canadian/France defaults.",
        },
    ],
    "bengali": [
        {
            "id": "bn-in",
            "type": "regional",
            "title": "West Bengal Bengali",
            "when": "`language: bengali` + `regional_voice: bn-in`. Kolkata/West Bengal standard prose.",
            "jobs": [
                ("নেই", "Absent/not there", "tipis+"),
                ("তাই", "Therefore", "tipis+"),
                ("হচ্ছে", "Ongoing state (returns undefined)", "tipis+"),
            ],
            "examples": [
                "`.env`-এ `API_TOKEN` নেই, তাই `loadConfig` `undefined` ফেরত দিচ্ছে। `npm test -- config` চালান।",
            ],
            "caps": ["India Bengali script and vocabulary default."],
            "forbidden": "Bangladesh-specific spelling in bn-in output.",
        },
        {
            "id": "bn-bd",
            "type": "regional",
            "title": "Bangladesh Bengali",
            "when": "`language: bengali` + `regional_voice: bn-bd`. Bangladesh standard prose.",
            "jobs": [
                ("নেই", "Absent", "tipis+"),
                ("তাই", "Therefore", "tipis+"),
                ("হচ্ছে", "Ongoing/result state", "tipis+"),
            ],
            "examples": [
                "`.env`-এ `API_TOKEN` নেই, তাই `loadConfig` `undefined` রিটার্ন করছে। `npm test -- config` চালান।",
            ],
            "caps": ["Bangladesh usage — do not force Kolkata idioms."],
            "forbidden": "West Bengal-only lexical choices presented as BD default.",
        },
    ],
    "portuguese": [
        {
            "id": "pt-pt",
            "type": "regional",
            "title": "European Portuguese",
            "when": "`language: portuguese` + `regional_voice: pt-pt`. Portugal Portuguese — not Brazilian default.",
            "jobs": [
                ("tu/você", "Match formality; PT-PT often avoids Brazilian você default in formal", "tipis+"),
                ("ecrã", "Screen (PT)", "tipis+"),
                ("ficheiro", "File (PT)", "tipis+"),
                ("está a", "Progressive (PT-PT)", "tipis+"),
            ],
            "examples": [
                "Falta `API_TOKEN` no `.env`, por isso `loadConfig` devolve `undefined`. Execute `npm test -- config`.",
            ],
            "caps": ["Do not use Brazilian a gente/tá as default."],
            "forbidden": "pt-br overlay markers in pt-pt output.",
        },
    ],
    "urdu": [
        {
            "id": "ur-pk",
            "type": "regional",
            "title": "Pakistan Urdu",
            "when": "`language: urdu` + `regional_voice: ur-pk`. Pakistan standard Urdu prose.",
            "jobs": [
                ("نہیں ہے", "Negation copula", "tipis+"),
                ("اس لیے", "Therefore", "tipis+"),
                ("واپس", "Return (function result)", "tipis+"),
            ],
            "examples": [
                "`.env` میں `API_TOKEN` نہیں ہے، اس لیے `loadConfig` `undefined` واپس کر رہا ہے۔ `npm test -- config` چلائیں۔",
            ],
            "caps": ["Pakistan Urdu vocabulary and spelling."],
            "forbidden": "Hindi devanagari in Urdu output.",
        },
        {
            "id": "ur-in",
            "type": "regional",
            "title": "Indian Urdu",
            "when": "`language: urdu` + `regional_voice: ur-in`. Indian Urdu — thin overlay.",
            "jobs": [
                ("نہیں ہے", "Negation", "tipis+"),
                ("اس لئے", "Therefore (Indian spelling preference)", "tipis+"),
                ("لو", "Casual imperative 'run' (spoken, santai only)", "sedang+"),
            ],
            "examples": [
                "`.env` میں `API_TOKEN` نہیں ہے، اس لئے `loadConfig` `undefined` لوٹ رہا ہے۔",
            ],
            "caps": ["Thin — distinguish PK/IN spelling only when relevant."],
            "forbidden": "Mixing Persian-heavy PK terms with forced Indian slang.",
        },
    ],
    "russian": [
        {
            "id": "ru-standard",
            "type": "regional",
            "title": "Moscow / Standard Russian",
            "when": "`language: russian` + `regional_voice: ru-standard` or `netral`. National standard for work.",
            "jobs": [
                ("нет", "Absent/not configured", "tipis+"),
                ("поэтому", "Therefore", "tipis+"),
                ("возвращает", "Returns (technical)", "tipis+"),
            ],
            "examples": [
                "В `.env` нет `API_TOKEN`, поэтому `loadConfig` возвращает `undefined`. Запустите `npm test -- config`.",
            ],
            "caps": ["Default Russian regional overlay."],
            "forbidden": "Southern dialect tails in standard output.",
        },
        {
            "id": "ru-southern",
            "type": "regional",
            "title": "Southern Russian (light)",
            "when": "`language: russian` + `regional_voice: ru-southern`. Light southern colour — thin.",
            "jobs": [
                ("шо", "What (spoken, very light)", "tipis"),
                ("это", "Emphatic 'this' in diagnosis", "tipis+"),
                ("же", "Particle emphasis on obvious cause", "tipis+"),
            ],
            "examples": [
                "В `.env` `API_TOKEN` нету, поэтому `loadConfig` `undefined` возвращает же.",
            ],
            "caps": ["Thin — one colloquial form per paragraph at `tipis`."],
            "forbidden": "Heavy caricature; нету in formal baku register.",
        },
    ],
    "german": [
        {
            "id": "de-de",
            "type": "regional",
            "title": "Germany German",
            "when": "`language: german` + `regional_voice: de-de`. Standard Germany German.",
            "jobs": [
                ("Sie", "Formal work default", "tipis+"),
                ("nicht", "Negation", "tipis+"),
                ("deshalb", "Therefore", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` fehlt in `.env`, deshalb gibt `loadConfig` `undefined` zurück. Führen Sie `npm test -- config` aus.",
            ],
            "caps": ["Default German overlay."],
            "forbidden": "Swiss ß/ss or Austrian particles in de-de output.",
        },
        {
            "id": "de-at",
            "type": "regional",
            "title": "Austrian German",
            "when": "`language: german` + `regional_voice: de-at`. Austria German — lexical overlay.",
            "jobs": [
                ("Jänner", "January (AT)", "tipis"),
                ("heuer", "This year (AT)", "tipis"),
                ("Standard Sie", "Formal work", "tipis+"),
                ("eh", "Particle 'anyway/obviously' (casual)", "sedang+"),
            ],
            "examples": [
                "In `.env` fehlt `API_TOKEN`, deshalb liefert `loadConfig` `undefined`. Bitte `npm test -- config` ausführen.",
            ],
            "caps": ["Lexicon overlay — do not force Jänner into every sentence."],
            "forbidden": "Swiss forms in Austrian output.",
        },
        {
            "id": "de-ch",
            "type": "regional",
            "title": "Swiss German (written standard)",
            "when": "`language: german` + `regional_voice: de-ch`. Swiss High German written — not dialect Schwyzertütsch.",
            "jobs": [
                ("ss not ß", "Swiss spelling", "tipis+"),
                ("Velo", "Bike (CH) — only if relevant", "tipis"),
                ("Grüezi", "Greeting — not in bug explanation body", "tipis"),
            ],
            "examples": [
                "`API_TOKEN` fehlt in `.env`, deshalb gibt `loadConfig` `undefined` zurück. Bitte `npm test -- config` ausführen.",
            ],
            "caps": [
                "Written Swiss Standard German — not oral dialect transcription.",
                "Do not phonetic-write Schwyzertütsch.",
            ],
            "forbidden": "ß in Swiss overlay; dialect phonetic parody.",
        },
    ],
    "malay": [
        {
            "id": "ms-my",
            "type": "regional",
            "title": "Malaysia Malay",
            "when": "`language: malay` + `regional_voice: ms-my`. Malaysian Malay baseline.",
            "jobs": [
                ("tiada", "Absent (MY preference in formal)", "tipis+"),
                ("jadi", "Therefore/so", "tipis+"),
                ("sila", "Please (work polite)", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` tiada dalam `.env`, jadi `loadConfig` memulangkan `undefined`. Sila jalankan `npm test -- config`.",
            ],
            "caps": ["Manglish is separate mix overlay."],
            "forbidden": "Indonesian jakarta particles in ms-my output.",
        },
        {
            "id": "ms-bn",
            "type": "regional",
            "title": "Brunei Malay",
            "when": "`language: malay` + `regional_voice: ms-bn`. Brunei Malay — thin overlay.",
            "jobs": [
                ("ada", "Exist/have", "tipis+"),
                ("tidak", "Negation", "tipis+"),
                ("bah", "Sentence softener (very light)", "tipis"),
            ],
            "examples": [
                "`API_TOKEN` tidak ada dalam `.env`, jadi `loadConfig` memulangkan `undefined`.",
            ],
            "caps": ["Thin overlay."],
            "forbidden": "Heavy Brunei particle stacking.",
        },
        {
            "id": "ms-sg",
            "type": "regional",
            "title": "Singapore Malay (light)",
            "when": "`language: malay` + `regional_voice: ms-sg`. Singapore Malay — thin.",
            "jobs": [
                ("tak", "Negation (spoken)", "tipis+"),
                ("dah", "Already/state change", "tipis+"),
                ("saja", "Just/only", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` tak ada dalam `.env`, jadi `loadConfig` return `undefined`. Cuba `npm test -- config`.",
            ],
            "caps": [
                "English mix belongs in `english/singlish` or `malay/manglish` on ask.",
            ],
            "forbidden": "lah in Malay script unless manglish mix.",
        },
    ],
    "vietnamese": [
        {
            "id": "vi-north",
            "type": "regional",
            "title": "Northern Vietnamese (Hanoi)",
            "when": "`language: vietnamese` + `regional_voice: vi-north`. Northern baseline — national standard lean.",
            "jobs": [
                ("không", "Negation", "tipis+"),
                ("nên", "Should/therefore next step", "tipis+"),
                ("đang", "Progressive state", "tipis+"),
                ("ạ", "Polite sentence tail (formal)", "tipis+"),
            ],
            "examples": [
                "`.env` không có `API_TOKEN`, nên `loadConfig` trả về `undefined`. Chạy `npm test -- config` nhé.",
            ],
            "caps": ["Default northern/standard lean for work."],
            "forbidden": "Southern particles in northern output.",
        },
        {
            "id": "vi-south",
            "type": "regional",
            "title": "Southern Vietnamese (Saigon)",
            "when": "`language: vietnamese` + `regional_voice: vi-south`. Southern grammar and lexicon.",
            "jobs": [
                ("không có", "Does not have", "tipis+"),
                ("nên", "Should", "tipis+"),
                ("hen", "Softener (southern)", "tipis+"),
                ("nghen", "Casual attention (santai only)", "sedang+"),
            ],
            "examples": [
                "`.env` không có `API_TOKEN`, nên `loadConfig` trả về `undefined`. Chạy `npm test -- config` hen.",
            ],
            "caps": ["One southern marker per sentence at `sedang`."],
            "forbidden": "Northern ạ spam in southern voice.",
        },
        {
            "id": "vi-central",
            "type": "regional",
            "title": "Central Vietnamese (light)",
            "when": "`language: vietnamese` + `regional_voice: vi-central`. Huế/Da Nang — thin overlay.",
            "jobs": [
                ("rứa", "Thus/so (central spoken)", "tipis"),
                ("mô", "Interrogative flavour (light)", "tipis"),
            ],
            "examples": [
                "`.env` không có `API_TOKEN`, `loadConfig` trả `undefined` rứa.",
            ],
            "caps": ["Thin — honesty cap without user examples."],
            "forbidden": "Inventing heavy Huế forms from stereotype.",
        },
    ],
    "telugu": [
        {
            "id": "te-hyderabad",
            "type": "regional",
            "title": "Hyderabad / Telangana Telugu",
            "when": "`language: telugu` + `regional_voice: te-hyderabad`. Standard Telugu for work — Telangana baseline.",
            "jobs": [
                ("లేదు", "Absent/not there", "tipis+"),
                ("కాబట్టి", "Therefore", "tipis+"),
                ("తిరిగి ఇస్తోంది", "Returns (result)", "tipis+"),
            ],
            "examples": [
                "`.env` లో `API_TOKEN` లేదు, కాబట్టి `loadConfig` `undefined` తిరిగి ఇస్తోంది. `npm test -- config` రన్ చేయండి.",
            ],
            "caps": ["Default Telugu regional."],
            "forbidden": "Invented slang outside pack.",
        },
        {
            "id": "te-coastal",
            "type": "regional",
            "title": "Coastal Andhra Telugu (light)",
            "when": "`language: telugu` + `regional_voice: te-coastal`. Light coastal colour.",
            "jobs": [
                ("లేదు", "Negation", "tipis+"),
                ("అంటే", "Meaning/that is", "tipis+"),
            ],
            "examples": [
                "`.env` లో `API_TOKEN` లేదు అంటే, `loadConfig` `undefined` ఇస్తోంది.",
            ],
            "caps": ["Thin overlay."],
            "forbidden": "Forced dialect word invention.",
        },
    ],
    "marathi": [
        {
            "id": "mr-standard",
            "type": "regional",
            "title": "Standard Marathi",
            "when": "`language: marathi` + `regional_voice: mr-standard` or `netral`. Pune/Mumbai standard for work.",
            "jobs": [
                ("नाही", "Negation", "tipis+"),
                ("म्हणून", "Therefore", "tipis+"),
                ("परत", "Return", "tipis+"),
            ],
            "examples": [
                "`.env` मध्ये `API_TOKEN` नाही, म्हणून `loadConfig` `undefined` परत करतो. `npm test -- config` चालवा.",
            ],
            "caps": ["Default Marathi regional."],
            "forbidden": "Mumbai slang unless mumbai overlay.",
        },
        {
            "id": "mr-mumbai",
            "type": "regional",
            "title": "Mumbai Marathi",
            "when": "`language: marathi` + `regional_voice: mr-mumbai`. Urban Mumbai conversational Marathi.",
            "jobs": [
                ("नाही ना", "Negation + tag", "tipis+"),
                ("म्हणजे", "That is/meaning", "tipis+"),
                ("बघ", "Look/try (casual imperative)", "sedang+"),
            ],
            "examples": [
                "`.env` मध्ये `API_TOKEN` नाही ना, म्हणून `loadConfig` `undefined` देतो. `npm test -- config` बघ.",
            ],
            "caps": ["Casual urban — not formal client email default."],
            "forbidden": "Bollywood catchphrases.",
        },
    ],
    "swahili": [
        {
            "id": "sw-tanzania",
            "type": "regional",
            "title": "Tanzania Swahili",
            "when": "`language: swahili` + `regional_voice: sw-tanzania`. Tanzania standard (KI swahili baseline).",
            "jobs": [
                ("hapana", "No/not there", "tipis+"),
                ("kwa hiyo", "Therefore", "tipis+"),
                ("inarudisha", "Returns", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` haipo kwenye `.env`, kwa hiyo `loadConfig` inarudisha `undefined`. Tekeleza `npm test -- config`.",
            ],
            "caps": ["East Africa standard lean."],
            "forbidden": "Kenya-only slang in Tanzania overlay.",
        },
        {
            "id": "sw-kenya",
            "type": "regional",
            "title": "Kenya Swahili",
            "when": "`language: swahili` + `regional_voice: sw-kenya`. Kenyan Swahili — light overlay.",
            "jobs": [
                ("sio", "Is not (spoken)", "tipis+"),
                ("basi", "So/okay then", "tipis+"),
                ("sasa", "Now/next — move to action", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` sio kwenye `.env`, basi `loadConfig` inarudisha `undefined`. Sasa tekeleza `npm test -- config`.",
            ],
            "caps": ["Thin Kenya colour — not Sheng mix."],
            "forbidden": "English/Sheng mix without user ask.",
        },
    ],
    "hausa": [
        {
            "id": "ha-nigeria",
            "type": "regional",
            "title": "Nigeria Hausa",
            "when": "`language: hausa` + `regional_voice: ha-nigeria`. Nigeria Hausa baseline.",
            "jobs": [
                ("ba", "Negation marker", "tipis+"),
                ("don haka", "Therefore", "tipis+"),
                ("ya dawo", "It returned", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` ba ya cikin `.env`, don haka `loadConfig` ya dawo da `undefined`. Gudanar da `npm test -- config`.",
            ],
            "caps": ["Default Hausa regional."],
            "forbidden": "Niger-only forms in Nigeria overlay.",
        },
        {
            "id": "ha-niger",
            "type": "regional",
            "title": "Niger Hausa (light)",
            "when": "`language: hausa` + `regional_voice: ha-niger`. Niger Hausa — thin overlay.",
            "jobs": [
                ("ba", "Negation", "tipis+"),
                ("saboda haka", "Therefore", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` ba ya cikin `.env`, saboda haka `loadConfig` yana dawo da `undefined`.",
            ],
            "caps": ["Thin — honesty without deep Niger-specific list."],
            "forbidden": "Inventing dialect words.",
        },
    ],
    "tagalog": [
        {
            "id": "tl-manila",
            "type": "regional",
            "title": "Manila Tagalog",
            "when": "`language: tagalog` + `regional_voice: tl-manila`. Metro Manila Filipino baseline.",
            "jobs": [
                ("wala", "Absent", "tipis+"),
                ("kaya", "Therefore/so", "tipis+"),
                ("nagbabalik", "Returns", "tipis+"),
                ("po", "Polite tail (work)", "tipis+"),
            ],
            "examples": [
                "Walang `API_TOKEN` sa `.env`, kaya nagbabalik ng `undefined` ang `loadConfig`. Patakbuhin ang `npm test -- config` po.",
            ],
            "caps": ["Taglish is separate mix overlay."],
            "forbidden": "English code-switch in every clause unless taglish.",
        },
        {
            "id": "tl-provincial",
            "type": "regional",
            "title": "Provincial Tagalog (light)",
            "when": "`language: tagalog` + `regional_voice: tl-provincial`. Light non-Manila colour.",
            "jobs": [
                ("ngà", "Emphasis tail (light)", "tipis"),
                ("kasi", "Because (explanatory)", "tipis+"),
            ],
            "examples": [
                "Wala ang `API_TOKEN` sa `.env` kasi, kaya `undefined` ang ibinabalik ng `loadConfig`.",
            ],
            "caps": ["Thin overlay."],
            "forbidden": "Inventing province-specific words without job.",
        },
    ],
    "turkish": [
        {
            "id": "tr-istanbul",
            "type": "regional",
            "title": "Istanbul / Standard Turkish",
            "when": "`language: turkish` + `regional_voice: tr-istanbul` or `netral`. National standard.",
            "jobs": [
                ("yok", "Absent", "tipis+"),
                ("bu yüzden", "Therefore", "tipis+"),
                ("döndürüyor", "Returns", "tipis+"),
            ],
            "examples": [
                "`.env` dosyasında `API_TOKEN` yok, bu yüzden `loadConfig` `undefined` döndürüyor. `npm test -- config` çalıştırın.",
            ],
            "caps": ["Default Turkish regional."],
            "forbidden": "Heavy eastern markers in Istanbul standard.",
        },
        {
            "id": "tr-anatolian",
            "type": "regional",
            "title": "Anatolian Turkish (light)",
            "when": "`language: turkish` + `regional_voice: tr-anatolian`. Light central/eastern colour.",
            "jobs": [
                ("yok ki", "Emphatic absence", "tipis+"),
                ("işte", "Here's the point/cause", "tipis+"),
            ],
            "examples": [
                "`.env`'de `API_TOKEN` yok ki, `loadConfig` `undefined` döndürüyor işte.",
            ],
            "caps": ["Thin — one marker per sentence at `tipis`."],
            "forbidden": "Stereotype rural parody.",
        },
    ],
    "pcm": [
        {
            "id": "pcm-lagos",
            "type": "regional",
            "title": "Lagos Nigerian Pidgin",
            "when": "`language: pcm` + `regional_voice: pcm-lagos`. Lagos PCM baseline.",
            "jobs": [
                ("no dey", "Is not present", "tipis+"),
                ("na so", "That's how/therefore", "tipis+"),
                ("abeg", "Please (soft request)", "tipis+"),
                ("make you", "Imperative please do", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` no dey for `.env`, na so `loadConfig` dey return `undefined`. Abeg run `npm test -- config`.",
            ],
            "caps": ["PCM pack honesty still applies."],
            "forbidden": "Forced comedy spellings.",
        },
        {
            "id": "pcm-port-harcourt",
            "type": "regional",
            "title": "Port Harcourt Pidgin (light)",
            "when": "`language: pcm` + `regional_voice: pcm-port-harcourt`. Niger Delta PCM — thin.",
            "jobs": [
                ("no dey", "Not there", "tipis+"),
                ("na im", "That's why", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` no dey for `.env`, na im `loadConfig` dey return `undefined`.",
            ],
            "caps": ["Thin overlay."],
            "forbidden": "Inventing delta slang list.",
        },
    ],
    "arz": [
        {
            "id": "arz-cairo",
            "type": "regional",
            "title": "Cairo Egyptian Arabic",
            "when": "`language: arz` + `regional_voice: arz-cairo`. Cairo urban Egyptian — default for arz.",
            "jobs": [
                ("مش", "Negation", "tipis+"),
                ("يعني", "So/meaning", "tipis+"),
                ("لازم", "Need to", "tipis+"),
                ("جرّب", "Try (imperative)", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` مش موجود في `.env`، يعني `loadConfig` بيرجع `undefined`. لازم تجرب `npm test -- config`.",
            ],
            "caps": ["arz is Egyptian — do not mix MSA-only chains without reason."],
            "forbidden": "Fusha formal every sentence unless register is baku.",
        },
        {
            "id": "arz-upper",
            "type": "regional",
            "title": "Upper Egypt Arabic (light)",
            "when": "`language: arz` + `regional_voice: arz-upper`. Light Upper Egypt colour.",
            "jobs": [
                ("مش", "Negation", "tipis+"),
                ("كده", "Like this/so", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` مش في `.env` كده، `loadConfig` بيرجع `undefined`.",
            ],
            "caps": ["Thin — honesty cap."],
            "forbidden": "Caricature southern spellings.",
        },
    ],
    "jawa": [
        {
            "id": "jv-solo",
            "type": "regional",
            "title": "Solo / Central Javanese",
            "when": "`language: jawa` + `regional_voice: jv-solo`. Central Javanese variety — pairs with speech levels.",
            "jobs": [
                ("ora", "Negation (ngoko)", "tipis+"),
                ("mula", "Therefore/so", "tipis+"),
                ("ngembalike", "Returns", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` ora ana ing `.env`, mula `loadConfig` bali `undefined`. Jaluk `npm test -- config`.",
            ],
            "caps": ["Speech level from `speech-levels.md` — overlay is regional lexicon/grammar colour."],
            "forbidden": "Mixing krama forms with ngoko particles without level choice.",
        },
        {
            "id": "jv-timur",
            "type": "regional",
            "title": "Eastern Javanese (light)",
            "when": "`language: jawa` + `regional_voice: jv-timur`. Eastern variety — thin.",
            "jobs": [
                ("ora", "Negation", "tipis+"),
                ("dadi", "So/therefore", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` ora ana ing `.env`, dadi `loadConfig` bali `undefined`.",
            ],
            "caps": ["Thin overlay."],
            "forbidden": "Inventing Surabaya Indonesian as Javanese.",
        },
    ],
    "sunda": [
        {
            "id": "su-bandung",
            "type": "regional",
            "title": "Priangan / Bandung Sundanese",
            "when": "`language: sunda` + `regional_voice: su-bandung`. Priangan Sundanese baseline.",
            "jobs": [
                ("teu", "Negation", "tipis+"),
                ("jadi", "Therefore", "tipis+"),
                ("mulangkeun", "Returns", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` teu aya di `.env`, jadi `loadConfig` mulangkeun `undefined`. Jalankeun `npm test -- config`.",
            ],
            "caps": ["Pair with loma/cohag from speech-levels."],
            "forbidden": "Indonesian kota Bandung overlay confused with Sundanese language.",
        },
        {
            "id": "su-cirebon",
            "type": "regional",
            "title": "Cirebon Sundanese (light)",
            "when": "`language: sunda` + `regional_voice: su-cirebon`. Cirebon area — thin.",
            "jobs": [
                ("teu", "Negation", "tipis+"),
                ("nya", "Sentence tail (light)", "tipis"),
            ],
            "examples": [
                "`API_TOKEN` teu aya di `.env` nya, `loadConfig` mulangkeun `undefined`.",
            ],
            "caps": ["Thin overlay."],
            "forbidden": "Heavy Cirebon Javanese mix without user ask.",
        },
    ],
    "bali": [
        {
            "id": "bali-urban",
            "type": "regional",
            "title": "Urban Balinese (Denpasar)",
            "when": "`language: bali` + `regional_voice: bali-urban`. Urban Denpasar Balinese.",
            "jobs": [
                ("ten", "Negation", "tipis+"),
                ("krana", "Because", "tipis+"),
                ("ngembalang", "Returns", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` ten wénten ring `.env`, krana `loadConfig` ngembalang `undefined`. Auts `npm test -- config`.",
            ],
            "caps": ["Pair with alus/madia/kasar speech levels."],
            "forbidden": "Tourism phrase spam.",
        },
        {
            "id": "bali-highland",
            "type": "regional",
            "title": "Highland Balinese (light)",
            "when": "`language: bali` + `regional_voice: bali-highland`. Highland register colour — thin.",
            "jobs": [
                ("ten", "Negation", "tipis+"),
                ("maké", "Because/so", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` ten wénten ring `.env`, maké `loadConfig` ngembalang `undefined`.",
            ],
            "caps": ["Thin — prefer alus level for formal."],
            "forbidden": "Inventing village exotica.",
        },
    ],
    "minangkabau": [
        {
            "id": "minang-padang",
            "type": "regional",
            "title": "Padang Minangkabau",
            "when": "`language: minangkabau` + `regional_voice: minang-padang`. Padang baseline.",
            "jobs": [
                ("indak", "Negation", "tipis+"),
                ("jadi", "Therefore", "tipis+"),
                ("ambali", "Returns/fetch", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` indak ado di `.env`, jadi `loadConfig` ambali `undefined`. Jalankan `npm test -- config`.",
            ],
            "caps": ["Limited pack honesty still applies."],
            "forbidden": "Indonesian minang overlay invention.",
        },
        {
            "id": "minang-coastal",
            "type": "regional",
            "title": "Coastal Minangkabau (light)",
            "when": "`language: minangkabau` + `regional_voice: minang-coastal`. Thin coastal colour.",
            "jobs": [
                ("indak", "Negation", "tipis+"),
                ("kok", "Emphasis (light)", "tipis"),
            ],
            "examples": [
                "`API_TOKEN` indak ado di `.env` kok, `loadConfig` ambali `undefined`.",
            ],
            "caps": ["Thin overlay."],
            "forbidden": "Forced kok every sentence.",
        },
    ],
    "makassar": [
        {
            "id": "mks-urban",
            "type": "regional",
            "title": "Urban Makassarese",
            "when": "`language: makassar` + `regional_voice: mks-urban`. Makassar city variety — **not** `indonesia` makassar overlay.",
            "jobs": [
                ("te'-", "Negation prefix (light)", "tipis+"),
                ("jadi", "Therefore", "tipis+"),
            ],
            "examples": [
                "`API_TOKEN` te'ada' ri `.env`, jadi `loadConfig` ampao `undefined`. Pa'jari `npm test -- config`.",
            ],
            "caps": [
                "Language pack honesty — thin forms.",
                "City overlay `indonesia/makassar` ≠ this language.",
            ],
            "forbidden": "Inventing Makassar Indonesian as Makassarese.",
        },
    ],
    "dayak-ngaju": [
        {
            "id": "ngaju-standard",
            "type": "regional",
            "title": "Ngaju Dayak (standard)",
            "when": "`language: dayak-ngaju` + `regional_voice: ngaju-standard`. Limited pack — thin regional marker.",
            "jobs": [
                ("jé", "Negation/not (light)", "tipis"),
                ("hambar", "Only/just", "tipis"),
            ],
            "examples": [
                "`API_TOKEN` jé há `.env`, `loadConfig` mulang `undefined`.",
            ],
            "caps": ["Limited coverage — state honesty; offer Indonesian if forms thin."],
            "forbidden": "Inventing Ngaju from stereotype.",
        },
    ],
    "dayak": [
        {
            "id": "dayak-umbrella",
            "type": "regional",
            "title": "Dayak umbrella (honesty)",
            "when": "`language: dayak` + any regional ask. **Umbrella — not one dialect.**",
            "jobs": [
                ("(none)", "Do not invent — route to `dayak-ngaju` or ask sub-language", "tipis"),
            ],
            "examples": [],
            "caps": [
                "Umbrella language: ask which Dayak language or use `dayak-ngaju`.",
                "Do not pick random Borneo forms.",
            ],
            "forbidden": "Any invented tribal vocabulary.",
        },
    ],
    "abui": [
        {
            "id": "abui-standard",
            "type": "regional",
            "title": "Abui (limited)",
            "when": "`language: abui` + regional ask. Limited pack — honesty first.",
            "jobs": [
                ("(thin)", "Use only forms from pack/culture.md", "tipis"),
            ],
            "examples": [],
            "caps": [
                "Limited coverage — do not invent regional variants.",
                "Offer Indonesian or English if user needs full explanation.",
            ],
            "forbidden": "Inventing Abui dialects.",
        },
    ],
}


def render_overlay(lang_id: str, spec: dict) -> str:
    lines = [
        f"# {spec['id']} — {spec['title']}",
        "",
        f"**Type:** `{spec['type']}` | **Status:** `validated`",
        "",
        "## When to load",
        "",
        spec["when"],
        "",
        "## Particle and grammar jobs",
        "",
        "| Form | Pragmatic job | Intensity |",
        "|---|---|---|",
    ]
    for form, job, intensity in spec["jobs"]:
        lines.append(f"| `{form}` | {job} | `{intensity}` |")

    if spec.get("examples"):
        lines.extend(["", "## Examples (bug explanation)", ""])
        for ex in spec["examples"]:
            lines.append(f"- {ex}")

    lines.extend(["", "## Caps", ""])
    for cap in spec["caps"]:
        lines.append(f"- {cap}")

    lines.extend(["", "## What NOT to mix", "", f"- {spec['forbidden']}"])
    lines.extend(["", "## Forbidden caricature", "", f"- {spec['forbidden']}"])
    return "\n".join(lines) + "\n"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    lang_by_id = {lang["id"]: lang for lang in registry["languages"]}

    for lang_id, specs in OVERLAYS.items():
        if lang_id not in lang_by_id:
            raise SystemExit(f"Unknown language id: {lang_id}")
        overlay_dir = SKILL_ROOT / "references" / "languages" / lang_id / "overlays"
        overlay_dir.mkdir(parents=True, exist_ok=True)
        existing_ids = {o["id"] for o in lang_by_id[lang_id].get("overlays", [])}

        for spec in specs:
            rel = f"references/languages/{lang_id}/overlays/{spec['id']}.md"
            path = SKILL_ROOT / rel
            path.write_text(render_overlay(lang_id, spec), encoding="utf-8")
            if spec["id"] not in existing_ids:
                lang_by_id[lang_id].setdefault("overlays", []).append(
                    {
                        "id": spec["id"],
                        "type": spec["type"],
                        "status": "validated",
                        "file": rel,
                    }
                )
                existing_ids.add(spec["id"])

    REGISTRY_PATH.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    total = sum(len(v) for v in OVERLAYS.values())
    print(f"Wrote {total} overlay files and updated registry.json")


if __name__ == "__main__":
    main()
