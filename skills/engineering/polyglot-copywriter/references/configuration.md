# Configuration and aliases

Users may pick language and style in plain words or a config block, in **English or Bahasa Indonesia**. Do not require a special config file.

This file covers both languages. `language` chooses the output language. The other options still apply; some overlays are Indonesian-only (see notes).

## Resolution order

Resolve each option on its own:

1. Explicit choice on the current request
2. Project or agent instructions
3. An explicit choice still in force in this conversation
4. The user's own language, only to match formality and pronouns
5. Defaults

An explicit ban wins over a preset at the same priority. English: “don't use kindly”, “no gue/lo”, “don't sound British”. Indonesian: “jangan pakai gue/lo”, “jangan formal”. If one value is unknown, drop **only that option** and use the next valid value. Do not throw away the whole config.

Current-request choices always beat older presets.

## Defaults

```yaml
farhan_voice:
  language: auto
  variety: auto
  regional_voice: netral
  register: santai
  intensity: tipis
  speech_level: auto
  prose_style: lugas
  poetic_intensity: tipis
  technical_terms: repo-natural
  self_reference: auto
  addressee_reference: auto
  orthography: auto
```

`language: auto`:

- User wrote or asked in Bahasa Indonesia → `indonesia`
- User wrote or asked in English → `english`
- Mixed, or unclear → match the language of the latest user sentence that is not a quote; if still mixed, ask one question

the author's default is casual and simple in **both** languages ([core.md](core.md)). Honorifics `mas`/`kak` still apply in Indonesian work chat, and may appear in mixed internal English chat. External English uses the person's name only. Load [plain-comms.md](usecases/plain-comms.md) only for email, letter, or announcement.

### Profiles vs overlay packs

When `regional_voice` is set, load the **overlay pack** from `references/languages/<lang>/overlays/<id>.md` (authoritative rules). Optionally load a matching **profile** from [profiles/](profiles/) for a short snapshot — see [profiles/README.md](profiles/README.md) and [profiles/index.json](profiles/index.json). Profiles never replace overlay files.

### Locale technique triggers (by language)

Plain-language aliases that should also load `references/techniques/locales/<language_id>.md` when the use case matches — after generic technique from [core.md](core.md):

| User says (examples) | `language` | Also load locale technique |
|---|---|---|
| 文案, 着陆页, 中文营销, LP Mandarin | `mandarin` | [locales/mandarin.md](techniques/locales/mandarin.md) |
| iklan, landing page Indonesia, copy marketplace | `indonesia` | [locales/indonesia.md](techniques/locales/indonesia.md) |
| キャッチコピー, LP 日本語, 日本語マーケ | `japanese` | [locales/japanese.md](techniques/locales/japanese.md) |
| việt marketing, quảng cáo, email tiếng Việt | `vietnamese` | [locales/vietnamese.md](techniques/locales/vietnamese.md) |
| copy en español, email en español, Bolivia, Perú, Chile | `spanish` | [locales/spanish.md](techniques/locales/spanish.md) |
| italiano, email in italiano | `italian` | [locales/italian.md](techniques/locales/italian.md) |
| Tamil, தமிழ் email | `tamil` | [locales/tamil.md](techniques/locales/tamil.md) |
| Punjabi, ਪੰਜਾਬੀ | `punjabi` | [locales/punjabi.md](techniques/locales/punjabi.md) |
| Deutsch, German marketing/email | `german` | [locales/german.md](techniques/locales/german.md) |
| العربية, Arabic email (umbrella) | `arabic` | [locales/arabic.md](techniques/locales/arabic.md) — route to overlay or `arz` |
| marketing coréen, email coréen | `korean` | [locales/korean.md](techniques/locales/korean.md) |
| marketing français, email français | `french` | [locales/french.md](techniques/locales/french.md) |
| marketing português, email português | `portuguese` | [locales/portuguese.md](techniques/locales/portuguese.md) |
| Hindi marketing, Hinglish (see in-en profile) | `hindi` / `english` | [locales/hindi.md](techniques/locales/hindi.md) or [profiles/in-en.md](profiles/in-en.md) |
| Taglish, Filipino marketing | `tagalog` / `english` | [locales/tagalog.md](techniques/locales/tagalog.md) or `ph-en` |
| ไทย, Thai email/marketing | `thai` | [locales/thai.md](techniques/locales/thai.md) |
| Nederlands, Dutch | `dutch` | [locales/dutch.md](techniques/locales/dutch.md) |
| فارسی, Farsi, Persian | `persian` | [locales/persian.md](techniques/locales/persian.md) |
| ελληνικά, Greek | `greek` | [locales/greek.md](techniques/locales/greek.md) |
| polski, Polish | `polish` | [locales/polish.md](techniques/locales/polish.md) |
| עברית, Hebrew | `hebrew` | [locales/hebrew.md](techniques/locales/hebrew.md) |
| 粵語, Cantonese, 廣東話 | `cantonese` | [locales/cantonese.md](techniques/locales/cantonese.md) — not `mandarin` |
| Hokkien, Taiwanese, Minnan | `hokkien` | [locales/hokkien.md](techniques/locales/hokkien.md) |
| Kiswahili, Swahili | `swahili` | [locales/swahili.md](techniques/locales/swahili.md) |

All 97 locale files are indexed in [techniques/index.json](techniques/index.json). Lookup any language: `python3 scripts/find_language.py <name>`.

`tulis email`, `write email`, `outage update`, `status page` → match use case in registry, then generic [email-comms.md](techniques/email-comms.md) or [incident-comms.md](techniques/incident-comms.md) plus locale row when applicable.

---

## English

### Phrases to understand

- “Write this in English.” / “Switch back to English.”
- “Keep it casual.” / “Too fancy. Simpler words.”
- “More formal English.” / “Careful, complete sentences.”
- “US English.” / “American spelling.”
- “British English.” / “UK spelling.”
- “Don't use kindly / please revert / circle back.”
- “Jakarta style, but in English, and don't use gue or lo.”
- “Jaksel / Indoglish, light mix.”
- “Singlish / Singapore English.” / “lah / can or not”
- “Australian / Aussie English.” / “Kiwi / New Zealand English.”
- “Canadian English.”
- “American slang / street US.”
- “Indian English.” / “Hinglish” (mix only if explicit)
- “Filipino English.” / “Taglish” (mix only if explicit)
- “Irish English.” / “South African English.”
- “Poetic English, thin.” / “Back to plain.”
- “No em dash / no arrows / less AI-sounding.” → tighten per [noslop-prose.md](noslop-prose.md)
- “Write this in Japanese / Korean / Arabic / French / Italian / Tamil / Punjabi / German.” (load registry pack)
- “Italiano / Switzerland Italian.” / “Tamil India / Sri Lanka.” / “Punjabi India / Pakistan.”
- “Bolivia Spanish / Perú / Chile.” / “es-bo / es-pe / es-cl”
- “Deutsch / Germany / Austria / Switzerland German.” / “العربية” (umbrella — ask dialect or use `arz` for Egyptian)
- “Tokyo Japanese / standard Japanese.” / “Kansai / Osaka dialect.” / “関西弁”
- “Seoul Korean.” / “Busan dialect.” / “Gyeongsang.”
- “Putonghua / Taiwan Mandarin / Singapore Chinese.”
- “Brazilian Portuguese / European Portuguese.”
- “Egyptian Arabic” → prefer `language: arz`; umbrella `arabic` for Levant/Gulf

A “try this style for this example” request is not a permanent preference.

### Config block example

```yaml
farhan_voice:
  language: english
  variety: auto
  regional_voice: netral
  register: santai
  intensity: tipis
  speech_level: auto
  prose_style: lugas
  poetic_intensity: tipis
  technical_terms: repo-natural
  self_reference: I
  addressee_reference: you
  orthography: auto
```

### English aliases

| User says | Set |
|---|---|
| casual, simple, everyday, chatty | `register: santai` |
| work English, professional, clear | `register: profesional` |
| formal English, careful, complete | `register: baku` |
| US English, American | `language: english` + `regional_voice: us` (or `netral`) |
| British, UK English | `language: english` + `regional_voice: uk` |
| Jaksel, Indoglish, South Jakarta English | `regional_voice: jaksel` |
| Singlish, Singapore English, SG English | `regional_voice: singlish` |
| Australian, Aussie | `regional_voice: au` |
| Kiwi, New Zealand | `regional_voice: nz` |
| Canadian | `regional_voice: ca` |
| American slang, street US | `regional_voice: us-slang` |
| Indian English | `regional_voice: in-en` |
| Hinglish (explicit mix) | `regional_voice: in-en` + user examples; cap intensity |
| Filipino English | `regional_voice: ph-en` |
| Taglish (explicit mix) | `regional_voice: ph-en` + user examples |
| Irish English | `regional_voice: ie` |
| South African English | `regional_voice: za` |
| too fancy, simpler words, too AI, de-AI | keep `language`, tighten vocab ([core.md](core.md), [noslop-prose.md](noslop-prose.md)) |
| poetic, more lyrical | `prose_style: puitis` |
| back to plain, don't be poetic | `prose_style: lugas` |
| go neutral, no accent | `regional_voice: netral` |
| Tokyo Japanese, standard Japanese, hyōjungo | `language: japanese` + `regional_voice: tokyo` |
| Kansai, Osaka Japanese, 関西弁 | `language: japanese` + `regional_voice: kansai` |
| Tohoku Japanese | `language: japanese` + `regional_voice: tohoku` |
| Kyushu Japanese | `language: japanese` + `regional_voice: kyushu` |
| Seoul Korean, standard Korean | `language: korean` + `regional_voice: seoul` |
| Busan, Gyeongsang Korean | `language: korean` + `regional_voice: busan` |
| Jeolla Korean | `language: korean` + `regional_voice: jeolla` |
| Mainland Mandarin, Putonghua | `language: mandarin` + `regional_voice: zh-cn` |
| Taiwan Mandarin | `language: mandarin` + `regional_voice: zh-tw` |
| Singapore Mandarin | `language: mandarin` + `regional_voice: zh-sg` |
| Hong Kong Mandarin | `language: mandarin` + `regional_voice: zh-hk` |
| Argentina Spanish | `language: spanish` + `regional_voice: es-ar` |
| Colombia Spanish | `language: spanish` + `regional_voice: es-co` |
| Canadian French | `language: french` + `regional_voice: fr-ca` |
| European Portuguese | `language: portuguese` + `regional_voice: pt-pt` |
| Germany / Austria / Swiss German | `language: german` + `de-de` / `de-at` / `de-ch` |
| Northern / Southern Vietnamese | `language: vietnamese` + `vi-north` / `vi-south` |
| Malaysian / Brunei / Singapore Malay | `language: malay` + `ms-my` / `ms-bn` / `ms-sg` |

`register: baku` in English means complete, careful sentences. It is not legal English and not British formality.

`orthography: auto` in English: US spelling and contractions on `santai`; US spelling, fewer contractions on `profesional` / `baku`. British spelling only when `regional_voice: uk` (or the user asked). Never rewrite program literals.

`speech_level` has no English `loma`/`ngoko`. For English social distance, use `register`. If the user says “street” or “posh”, map to `santai` or `baku` and keep `speech_level: auto`.

`regional_voice` on English output uses the **English** table in [regional.md](regional.md). Do not pour `ya` / `sih` / `dong` into English unless the user asked for mixed chat (`jaksel`).

---

## Bahasa Indonesia

### Phrases to understand

- “Tulis dalam bahasa Indonesia.”
- “Pakai gaya Jakarta, santai, tapi jangan gue/lo.”
- “Jawab ala Jaksel.”
- “Pakai Sunda loma.” / “Pakai Sunda cohag, tapi jangan memaki.”
- “Sunda kasar.” (ambiguous — ask loma vs cohag)
- “Jelaskan dalam bahasa Abui. Kalau belum ada panduan, jangan mengarang.”
- “Jelaskan dalam bahasa Dayak.”
- “language: makassar” (the language, not city-Indonesian)
- “Pakai bahasa puitis, tipis saja.”
- “Balik netral.”

### Config block example

```yaml
farhan_voice:
  language: indonesia
  variety: auto
  regional_voice: jakarta
  register: santai
  intensity: tipis
  speech_level: auto
  prose_style: lugas
  poetic_intensity: tipis
  technical_terms: repo-natural
  self_reference: auto
  addressee_reference: auto
  orthography: auto
```

### Indonesian aliases

- `Jawa halus` / `krama` / `kromo` → `speech_level: krama`
- `Sunda loma` / `Sunda akrab` → `speech_level: loma`
- `Sunda cohag` / `Sunda kasar pisan` → `speech_level: cohag`
- `Sunda kasar` with no extra words → ask: “Do you mean loma/akrab or cohag/kasar pisan?”
- `bahasa puitis`, `lebih liris` → `prose_style: puitis`
- `kasual` / `santai` / `gaul` → `register: santai`
- `formal` / `baku` / `korporat` → `register: baku` or `profesional` from channel

Do not equate `Betawi` with `jakarta`, full Sundanese with `bandung`, or every Javanese variety with `yogyakarta`.

---

## Option meanings (both languages)

| Option | Values | Notes |
|---|---|---|
| `language` | `auto`, `english`, `indonesia`, or an id from [registry.json](registry.json) / [fictional-catalog.json](fictional-catalog.json) | Real languages load from the registry; fictional fixtures from the fictional catalog. Umbrella/limited packs have honesty rules in `pack.md`. Unknown names → do not invent. |
| `variety` | `auto` or an explicit variety | Never guess dialect from province or identity. |
| `regional_voice` | canonical id in [regional.md](regional.md) | `netral` adds no region markers. Indonesian ids overlay Indonesian prose. English ids overlay English prose. |
| `register` | `baku`, `profesional`, `santai` | Default `santai` in both languages. The others are on request. |
| `intensity` | `tipis`, `sedang`, `kental` | Depth of regional pattern, not a slang quota. |
| `speech_level` | `auto`, or a level from the language guide | Indonesian: Sunda `loma`/`cohag`, Jawa `ngoko`/`krama`. English: ignore; use `register`. Not a license to insult. |
| `prose_style` | `lugas`, `puitis` | Separate from regional voice. Works in both languages. |
| `poetic_intensity` | `tipis`, `sedang`, `kental` | Only when `prose_style: puitis`. |
| `technical_terms` | `repo-natural`, `indonesia-first`, `english-first` | Exact-match artifacts stay protected. |
| `self_reference` | `auto` or an explicit form | `saya`, `aku`, `I`, `omit`. Never print the word `omit`. |
| `addressee_reference` | `auto` or an explicit form | `kamu`, `Anda`, `you`, `omit`. |
| `orthography` | `auto`, `standar`, `percakapan` | Never rewrite technical artifacts. English `auto` = US spelling unless `regional_voice: uk`. |

`orthography: auto` becomes `standar` on `baku`/`profesional`, and `percakapan` on `santai`.

With `regional_voice: netral`, ignore `intensity` for regional features. With `prose_style: lugas`, ignore `poetic_intensity`.

## Conflicts

- If `language` is umbrella (`arabic`, `dayak`), limited (`abui`, `kashmiri`, `quechua`, …), or a fictional fixture from [fictional-catalog.json](fictional-catalog.json), follow `pack.md` before raising `intensity`. Offer `indonesia` or `english`, or ask for a user example when the pack says so. Fictional fixtures never get thick invented prose.
- `language: makassar` is not `regional_voice: makassar`.
- Indonesian `speech_level` (`loma`, `ngoko`) on `language: english` → keep English, set `speech_level: auto`, and use `register` for distance. If both were explicit and it matters, ask one short question.
- `regional_voice: jakarta` with `language: english` is mixed chat only if the user asked for Jakarta-in-English or Jaksel. Otherwise keep English `netral` (Indo-US) and do not sprinkle Indonesian particles.
- If `speech_level` does not belong to the Indonesian profile family (`bandung + ngoko`, `surabaya + loma`), do not mix.
- “kurangi” / “less” / “dial it down” lowers the axis last discussed. If regional and poetic are both on and the target is unclear, ask which intensity.
- Japanese, Korean, Arabic, French, and other registry languages load packs under `references/languages/`. Umbrella and limited packs still have honesty caps in `pack.md`.

## Incomplete choices

- “Jawa” as `language` is known, but variety and speech level may be too wide. Offer choices if the difference matters.
- Umbrella labels (`Dayak`, `Batak`, `Papua`, `Melayu`, `Indonesia Timur`) need a more specific language. Do not pick one from stereotype.
- `Kebumen` without a sub-region may use a broad profile up to `sedang`. For `kental`, ask for kecamatan or west/centre/east lean.
- “US accent” / “British accent” / “sound local” without a variety: use the English `netral` or `uk`/`us` row in [regional.md](regional.md). Do not invent Texas, Cockney, or valley-girl speech.
- “Singapore / Australia / Canada / India / Philippines / Ireland / South Africa” English: map to the matching row in [regional.md](regional.md) (`singlish`, `au`, `ca`, `in-en`, `ph-en`, `ie`, `za`). Ask one question if country and slang level are both unclear.
- “Puitis” / “poetic” with no form means thin poetic prose, not stanza verse.

## Switching

- “balik netral” / “go neutral” / “no accent” clears `regional_voice` markers. It does not change `language` unless also named.
- “jangan puitis” / “back to plain” sets `prose_style: lugas` and keeps the regional profile.
- “write in English” / “tulis dalam bahasa Indonesia” switches `language` for the current task.
