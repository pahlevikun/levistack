# Regional voice router

Read when `regional_voice` is not `netral`, `speech_level` is not `auto`, or the user asks for a city style, English variety, or speech level.

**Index:** [registry.json](registry.json) → `languages[].overlays` and `speech_levels` (real languages only). Fictional fixtures in [fictional-catalog.json](fictional-catalog.json) have no overlays. Load **one** overlay file from the active language's `references/languages/<id>/overlays/` or `speech-levels.md`.

Always read [core.md](core.md) first. Language selection is [language-selection.md](languages/language-selection.md), not this file.

## Shared rules

- Apply markers only to prose in the active `language`.
- Load **one** profile or overlay. No mix soup unless user asked (`jaksel`, `singlish`, `manglish`).
- Intensity: `tipis` | `sedang` | `kental` — pattern depth, not slang quota.
- Unknown places (Atlantis, invented dialects): fall back to `netral`. Do not invent vocabulary.
- Pragmatic function before iconic vocabulary. No phonetic parody.
- All registry overlays are **validated**. Do not claim native authenticity or force marker quotas.

## English (`language: english`)

Resolve `regional_voice` against `english` overlays in registry. Key profiles also summarized in [profiles/english-netral.md](profiles/english-netral.md).

| `regional_voice` | Overlay file |
|---|---|
| `netral`, `us` | `languages/english/overlays/us.md` (netral ≈ us for routing) |
| `uk` | `languages/english/overlays/uk.md` |
| `us-slang` | `languages/english/overlays/us-slang.md` |
| `singlish` | `languages/english/overlays/singlish.md` |
| `jaksel` | `languages/english/overlays/jaksel.md` |

English has no `loma`/`ngoko`. Use `register` for social distance.

Full dialect audit: [dialect-coverage.md](dialect-coverage.md).

## Indonesian (`language: indonesia`)

| `regional_voice` | Overlay file |
|---|---|
| `jakarta` | `languages/indonesia/overlays/jakarta.md` |
| `jaksel` | `languages/indonesia/overlays/jaksel.md` |
| `bandung` | `languages/indonesia/overlays/bandung.md` |
| `surabaya` | `languages/indonesia/overlays/surabaya.md` |
| `yogyakarta` | `languages/indonesia/overlays/yogyakarta.md` |
| `medan` | `languages/indonesia/overlays/medan.md` |
| `makassar` | `languages/indonesia/overlays/makassar.md` |

City overlay is not ethnic language: `makassar` overlay ≠ `language: makassar`.

## Speech levels (separate language packs)

| Language | File |
|---|---|
| `jawa` | `languages/jawa/speech-levels.md` |
| `sunda` | `languages/sunda/speech-levels.md` |
| `bali` | `languages/bali/speech-levels.md` |

`Sunda kasar` without loma/cohag → ask first (see sunda speech-levels).

## Malay

| `regional_voice` | Overlay file |
|---|---|
| `ms-my` | `languages/malay/overlays/ms-my.md` |
| `ms-bn` | `languages/malay/overlays/ms-bn.md` |
| `ms-sg` | `languages/malay/overlays/ms-sg.md` |
| `manglish` | `languages/malay/overlays/manglish.md` (mix — explicit ask) |

## Japanese (`language: japanese`)

Keigo / です・ます stay in `languages/japanese/speech-levels.md`. Regional dialect is **one** overlay:

| `regional_voice` | Overlay file |
|---|---|
| `netral`, `tokyo` | `languages/japanese/overlays/tokyo.md` (standard default) |
| `kansai`, `osaka` | `languages/japanese/overlays/kansai.md` |
| `tohoku` | `languages/japanese/overlays/tohoku.md` |
| `kyushu` | `languages/japanese/overlays/kyushu.md` |

Do not mix です／ます with heavy 関西弁 (やねん／へん) in one sentence unless user asked.

## Korean (`language: korean`)

| `regional_voice` | Overlay file |
|---|---|
| `netral`, `seoul` | `languages/korean/overlays/seoul.md` |
| `busan`, `gyeongsang` | `languages/korean/overlays/busan.md` |
| `jeolla` | `languages/korean/overlays/jeolla.md` |

## Mandarin (`language: mandarin`)

| `regional_voice` | Overlay file |
|---|---|
| `zh-cn` | `languages/mandarin/overlays/zh-cn.md` |
| `zh-tw` | `languages/mandarin/overlays/zh-tw.md` |
| `zh-sg` | `languages/mandarin/overlays/zh-sg.md` |
| `zh-hk` | `languages/mandarin/overlays/zh-hk.md` (Mandarin for HK — not Cantonese) |

## Spanish, French, Portuguese, German, Hindi, Bengali, Urdu, Russian

Resolve `regional_voice` against registry `overlays` for the active language. Common ids:

| Language | Overlay ids |
|---|---|
| spanish | `es-es`, `es-mx`, `es-ar`, `es-co`, `es-bo`, `es-pe`, `es-cl` |
| italian | `it-it`, `it-ch` |
| tamil | `ta-in`, `ta-lk` |
| punjabi | `pa-in`, `pa-pk` |
| french | `fr-fr`, `fr-ca`, `fr-be`, `fr-af` |
| portuguese | `pt-br`, `pt-pt` |
| german | `de-de`, `de-at`, `de-ch` |
| hindi | `hi-standard`, `haryanvi`, `mumbai-hindi`, `hinglish` (mix) |
| bengali | `bn-in`, `bn-bd` |
| urdu | `ur-pk`, `ur-in` |
| russian | `ru-standard`, `ru-southern` |

## Arabic (`language: arabic` — umbrella)

| `regional_voice` | Overlay file |
|---|---|
| `arabic-egyptian` | `languages/arabic/overlays/arabic-egyptian.md` (prefer `language: arz` for sustained Egyptian) |
| `arabic-levantine` | `languages/arabic/overlays/arabic-levantine.md` |
| `arabic-gulf` | `languages/arabic/overlays/arabic-gulf.md` |

## Vietnamese, Telugu, Marathi, Swahili, Hausa, Turkish, PCM, Tagalog

| Language | Overlay ids |
|---|---|
| vietnamese | `vi-north`, `vi-south`, `vi-central` |
| telugu | `te-hyderabad`, `te-coastal` |
| marathi | `mr-standard`, `mr-mumbai` |
| swahili | `sw-tanzania`, `sw-kenya` |
| hausa | `ha-nigeria`, `ha-niger` |
| turkish | `tr-istanbul`, `tr-anatolian` |
| pcm | `pcm-lagos`, `pcm-port-harcourt` |
| tagalog | `tl-manila`, `tl-provincial`, `taglish` (mix) |

## Sinitic varieties (separate language packs)

| Language | Overlay ids | Notes |
|---|---|---|
| mandarin | `zh-cn`, `zh-tw`, `zh-sg`, `zh-hk` | `zh-hk` = Mandarin for HK, **not** Cantonese |
| cantonese | `yue-hk` | Yue/Cantonese — do not route to `mandarin` |
| hokkien | `nan-tw` | Minnan/Taiwanese — separate from `mandarin` |

## Europe, Middle East, Africa, South Asia (wave 3)

Resolve `regional_voice` against registry `overlays` for the active language. Each language has a standard overlay (e.g. `th-standard`, `nl-standard`, `fa-standard`, `el-standard`). Umbrella: `kurdish` (`ku-standard` — ask Kurmanji vs Sorani). Limited: `kashmiri`, `quechua`, `guarani`, `latin`, `hokkien` — see pack honesty.

Lookup: `python3 scripts/find_language.py <name>`.

## Ethnic / limited packs (Jawa, Sunda, Bali, Minangkabau, Makassar, Dayak, Abui)

| Language | Overlay ids | Notes |
|---|---|---|
| jawa | `jv-solo`, `jv-timur` | + `speech-levels.md` |
| sunda | `su-bandung`, `su-cirebon` | + `speech-levels.md`; not `indonesia/bandung` |
| bali | `bali-urban`, `bali-highland` | + `speech-levels.md` |
| minangkabau | `minang-padang`, `minang-coastal` | Limited pack honesty |
| makassar | `mks-urban` | Language — not `indonesia/makassar` city overlay |
| arz | `arz-cairo`, `arz-upper` | Egyptian Arabic language |
| dayak-ngaju | `ngaju-standard` | Limited honesty |
| dayak | `dayak-umbrella` | Ask sub-language |
| abui | `abui-standard` | Limited honesty |
| atlantis | — | Fictional — fall back to `netral` |
| klingon | — | Fictional — fall back to `netral` |
| elvish | — | Fictional — fall back to `netral` |
| navi | — | Fictional — Na'vi (Avatar); fall back to `netral` |

## Quick profile summaries

Thin routing hints — full rules live in overlay files:

- [profiles/jakarta.md](profiles/jakarta.md)
- [profiles/jaksel.md](profiles/jaksel.md)
- [profiles/singlish.md](profiles/singlish.md)
- [profiles/us-slang.md](profiles/us-slang.md)
