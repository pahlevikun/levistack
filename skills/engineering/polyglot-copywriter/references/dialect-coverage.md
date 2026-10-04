# Dialect and regional overlay coverage

Audit of `references/registry.json` regional varieties. **Keigo / speech levels** stay in `speech-levels.md` (Japanese, Korean, Jawa, Sunda, Bali) — not duplicated here. Fictional honesty fixtures (`atlantis`, `klingon`, `elvish`, `navi`) are in [fictional-catalog.json](fictional-catalog.json), not the registry.

Legend: **exists** = overlay file + registry row; **n/a** = umbrella/honesty-only; **fictional** = fixture in fictional catalog — no overlay by design.

## Summary by language

| Language | Regional overlays | Mix/slang | Gaps / notes |
|---|---|---|---|
| english | 9 (us, uk, au, nz, ca, ie, za, in-en, ph-en) | us-slang, singlish, jaksel | Complete for major varieties |
| indonesia | 6 cities + jaksel mix | jaksel | City overlays complete |
| malay | ms-my, ms-bn, ms-sg | manglish | Complete |
| jawa | jv-solo, jv-timur | — | Speech levels separate |
| sunda | su-bandung, su-cirebon | — | Speech levels separate |
| bali | bali-urban, bali-highland | — | Speech levels separate |
| mandarin | zh-cn, zh-tw, zh-sg, zh-hk | — | Cantonese is separate language |
| hindi | hi-standard, haryanvi, mumbai-hindi | hinglish | Complete |
| spanish | es-es, es-mx, es-ar, es-co, es-bo, es-pe, es-cl | — | LATAM + Spain complete for listed varieties |
| italian | it-it, it-ch | — | Switzerland light |
| tamil | ta-in, ta-lk | — | Sri Lanka light |
| punjabi | pa-in, pa-pk | — | Pakistan light (Gurmukhi baseline) |
| arabic | arabic-egyptian, levantine, gulf | — | Umbrella honesty; prefer `arz` for Egyptian |
| french | fr-fr, fr-ca, fr-be, fr-af | — | Complete |
| bengali | bn-in, bn-bd | — | Complete |
| portuguese | pt-br, pt-pt | — | Complete |
| urdu | ur-pk, ur-in | — | Complete |
| russian | ru-standard, ru-southern | — | Complete (light southern) |
| german | de-de, de-at, de-ch | — | Complete |
| japanese | tokyo, kansai, tohoku, kyushu | — | Keigo in speech-levels |
| korean | seoul, busan, jeolla | — | Jondaetmal/banmal in speech-levels |
| vietnamese | vi-north, vi-south, vi-central | — | Complete |
| telugu | te-hyderabad, te-coastal | — | Complete (light coastal) |
| marathi | mr-standard, mr-mumbai | — | Complete |
| swahili | sw-tanzania, sw-kenya | — | Complete |
| hausa | ha-nigeria, ha-niger | — | Complete (light Niger) |
| tagalog | tl-manila, tl-provincial | taglish | Complete |
| turkish | tr-istanbul, tr-anatolian | — | Complete |
| pcm | pcm-lagos, pcm-port-harcourt | — | Complete |
| arz | arz-cairo, arz-upper | — | Egyptian Arabic language pack |
| minangkabau | minang-padang, minang-coastal | — | Limited pack honesty |
| makassar | mks-urban | — | ≠ `indonesia/makassar` city overlay |
| dayak-ngaju | ngaju-standard | — | Limited pack honesty |
| dayak | dayak-umbrella | — | Umbrella — route to sub-language |
| abui | abui-standard | — | Limited — no invented dialects |
| kashmiri | ks-standard | — | Scaffolded — ask script; no invented dialect forms |
| quechua | qu-standard | — | Scaffolded — ask regional variety |
| guarani | gn-standard | — | Scaffolded — ask Jopará vs pure Guarani |
| latin | la-standard | — | Scaffolded — default `baku`; no neologisms |
| hokkien | nan-tw | — | Scaffolded — not `mandarin`; ask script |
| atlantis | — | — | Fictional — fall back to `netral` |
| klingon | — | — | Fictional — fall back to `netral` |
| elvish | — | — | Fictional — fall back to `netral` |
| navi | — | — | Fictional — Na'vi (Avatar); fall back to `netral` |

## Full overlay table

| Language | Overlay id | Type | Status | Notes |
|---|---|---|---|---|
| english | us | regional | exists | Default/neutral American |
| english | uk | regional | exists | British spelling/lexicon |
| english | au | regional | exists | Australian |
| english | nz | regional | exists | New Zealand |
| english | ca | regional | exists | Canadian |
| english | ie | regional | exists | Irish |
| english | za | regional | exists | South African |
| english | in-en | regional | exists | Indian English |
| english | ph-en | regional | exists | Filipino English |
| english | us-slang | slang | exists | Casual US |
| english | singlish | mix | exists | SG English mix |
| english | jaksel | mix | exists | Jakarta-in-English mix |
| indonesia | jakarta | regional | exists | Jakarta Indonesian |
| indonesia | bandung | regional | exists | Bandung |
| indonesia | surabaya | regional | exists | Surabaya |
| indonesia | yogyakarta | regional | exists | Yogyakarta |
| indonesia | medan | regional | exists | Medan |
| indonesia | makassar | regional | exists | City Indonesian (not language) |
| indonesia | jaksel | mix | exists | Jaksel mix |
| malay | ms-my | regional | exists | Malaysia Malay |
| malay | ms-bn | regional | exists | Brunei Malay |
| malay | ms-sg | regional | exists | Singapore Malay light |
| malay | manglish | mix | exists | Malay–English mix |
| jawa | jv-solo | regional | exists | Central/Solo variety |
| jawa | jv-timur | regional | exists | Eastern light |
| sunda | su-bandung | regional | exists | Priangan/Bandung |
| sunda | su-cirebon | regional | exists | Cirebon light |
| bali | bali-urban | regional | exists | Denpasar urban |
| bali | bali-highland | regional | exists | Highland light |
| mandarin | zh-cn | regional | exists | Mainland Putonghua |
| mandarin | zh-tw | regional | exists | Taiwan Mandarin |
| mandarin | zh-sg | regional | exists | Singapore Mandarin |
| mandarin | zh-hk | regional | exists | HK Mandarin (not Cantonese) |
| hindi | hi-standard | regional | exists | Standard Hindi |
| hindi | haryanvi | regional | exists | Haryanvi-influenced light |
| hindi | mumbai-hindi | regional | exists | Mumbai urban |
| hindi | hinglish | mix | exists | Hindi–English mix |
| spanish | es-es | regional | exists | Spain |
| spanish | es-mx | regional | exists | Mexico |
| spanish | es-ar | regional | exists | Argentina |
| spanish | es-co | regional | exists | Colombia |
| spanish | es-bo | regional | exists | Bolivia |
| spanish | es-pe | regional | exists | Peru |
| spanish | es-cl | regional | exists | Chile |
| italian | it-it | regional | exists | Italy standard |
| italian | it-ch | regional | exists | Swiss Italian light |
| tamil | ta-in | regional | exists | India Tamil |
| tamil | ta-lk | regional | exists | Sri Lanka light |
| punjabi | pa-in | regional | exists | India Gurmukhi |
| punjabi | pa-pk | regional | exists | Pakistan light |
| arabic | arabic-egyptian | regional | exists | Umbrella; prefer `arz` |
| arabic | arabic-levantine | regional | exists | Umbrella Levant |
| arabic | arabic-gulf | regional | exists | Umbrella Gulf |
| french | fr-fr | regional | exists | France |
| french | fr-ca | regional | exists | Canadian |
| french | fr-be | regional | exists | Belgian light |
| french | fr-af | regional | exists | African French broad |
| bengali | bn-in | regional | exists | West Bengal |
| bengali | bn-bd | regional | exists | Bangladesh |
| portuguese | pt-br | regional | exists | Brazil |
| portuguese | pt-pt | regional | exists | Portugal |
| urdu | ur-pk | regional | exists | Pakistan |
| urdu | ur-in | regional | exists | India light |
| russian | ru-standard | regional | exists | Moscow/standard |
| russian | ru-southern | regional | exists | Southern light |
| german | de-de | regional | exists | Germany |
| german | de-at | regional | exists | Austria |
| german | de-ch | regional | exists | Swiss High German |
| japanese | tokyo | regional | exists | Hyōjungo / standard default |
| japanese | kansai | regional | exists | Osaka–Kyoto grammar |
| japanese | tohoku | regional | exists | Northeastern light |
| japanese | kyushu | regional | exists | Kyushu light |
| korean | seoul | regional | exists | Standard |
| korean | busan | regional | exists | Gyeongsang |
| korean | jeolla | regional | exists | Jeolla light |
| vietnamese | vi-north | regional | exists | Hanoi/northern |
| vietnamese | vi-south | regional | exists | Saigon/southern |
| vietnamese | vi-central | regional | exists | Central light |
| telugu | te-hyderabad | regional | exists | Telangana baseline |
| telugu | te-coastal | regional | exists | Coastal light |
| marathi | mr-standard | regional | exists | Standard |
| marathi | mr-mumbai | regional | exists | Mumbai urban |
| swahili | sw-tanzania | regional | exists | Tanzania standard |
| swahili | sw-kenya | regional | exists | Kenya light |
| hausa | ha-nigeria | regional | exists | Nigeria |
| hausa | ha-niger | regional | exists | Niger light |
| tagalog | tl-manila | regional | exists | Metro Manila |
| tagalog | tl-provincial | regional | exists | Provincial light |
| tagalog | taglish | mix | exists | Tagalog–English mix |
| turkish | tr-istanbul | regional | exists | Standard |
| turkish | tr-anatolian | regional | exists | Anatolian light |
| pcm | pcm-lagos | regional | exists | Lagos PCM |
| pcm | pcm-port-harcourt | regional | exists | Port Harcourt light |
| arz | arz-cairo | regional | exists | Cairo Egyptian |
| arz | arz-upper | regional | exists | Upper Egypt light |
| minangkabau | minang-padang | regional | exists | Padang |
| minangkabau | minang-coastal | regional | exists | Coastal light |
| makassar | mks-urban | regional | exists | Makassarese language |
| dayak-ngaju | ngaju-standard | regional | exists | Limited honesty |
| dayak | dayak-umbrella | regional | exists | Routes to sub-language |
| abui | abui-standard | regional | exists | Limited honesty |
| kashmiri | ks-standard | regional | exists | Scaffolded — ask script |
| quechua | qu-standard | regional | exists | Scaffolded — ask variety |
| guarani | gn-standard | regional | exists | Scaffolded — ask Jopará vs pure |
| latin | la-standard | regional | exists | Scaffolded — default `baku` |
| hokkien | nan-tw | regional | exists | Scaffolded — not `mandarin` |
| atlantis | — | — | n/a | Fictional — use `netral` |
| klingon | — | — | n/a | Fictional — use `netral` |
| elvish | — | — | n/a | Fictional — use `netral` |
| navi | — | — | n/a | Fictional — Na'vi (Avatar); use `netral` |

## Wave 3 additions (62 languages)

Each new language has one standard regional overlay (`*-standard`, `*-ua`, `yue-hk`, `nan-tw`, `my-mm`, etc.) unless umbrella/limited honesty applies.

| Region | Languages | Overlay pattern | Notes |
|---|---|---|---|
| Europe | greek, dutch, polish, ukrainian, czech, romanian, hungarian, swedish, norwegian, danish, finnish, serbian, croatian, bosnian, bulgarian, slovak, slovenian, lithuanian, latvian, estonian, icelandic, albanian, catalan, galician, basque, irish, welsh, esperanto | `<id>-standard` or `cat-standard`, `sl-si`, `uk-ua` | Conservative standard variety |
| Middle East / Central Asia | persian, hebrew, pashto, kurdish, azerbaijani, kazakh, uzbek, mongolian, georgian, armenian | `*-standard` | `kurdish` umbrella — ask variety |
| South & SE Asia | thai, lao, khmer, burmese, nepali, sinhala, gujarati, kannada, malayalam, odia, assamese, kashmiri, sindhi, cantonese | `*-standard`, `my-mm`, `yue-hk` | `cantonese` ≠ `mandarin`; `kashmiri` limited |
| Africa | amharic, somali, yoruba, igbo, zulu, afrikaans | `*-standard` | Standard variety per language |
| Americas indigenous | quechua, guarani | `*-standard` | Limited — ask regional variety |
| Classical | latin | `la-standard` | Limited — default `baku` |
| Sinitic (Minnan) | hokkien | `nan-tw` | **Separate from `mandarin`** — documented in pack |

## Major dialects still outside scope

| Item | Why |
|---|---|
| Deep rural sub-dialects per language | Require user examples before `kental` |
| Full MSA-only Arabic | `arabic` umbrella uses dialect-informed overlays; prefer `arz` for Egyptian |
| Every Indonesian ethnic language | Only documented packs in registry |
| Community-specific Quechua/Guarani variants | Limited packs — ask before thick prose |

Last updated: wave 3 bulk add — 97 real languages, 4 fictional fixtures, 163 overlays, 97 locale techniques, 163 profiles.
