# Hokkien — language pack

**Status:** `validated`. Write as a careful coworker in Hokkien; **not** the author fingerprint unless user asked English/Indonesian.

## Load map

| User signal | Load |
|---|---|
| Everyday writing | `pack.md` + `registers.md` |
| Culture, transcreation, pronouns | also `culture.md` |
| Region / variety | also **one** overlay from `overlays/` |

## Honesty

Scaffolded pack — limited coverage. Conservative standard Hokkien (Minnan) only; separate from `mandarin`; not full regional or native-speaker depth.

- **MUST NOT** invent grammar, morphology, particles, or romanization not in this pack or listed overlays.
- **MUST NOT** claim native fluency or regional expertise beyond what the pack documents.
- **MUST NOT** use Mandarin particles, `zh-hk` patterns, or Cantonese forms in this pack.
- **MUST NOT** invent regional romanization (Taiwan POJ vs Quanzhou vs Amoy) without a matching overlay.
- **MUST NOT** draft thick prose when the user meant Mandarin — switch to `mandarin` (or `mandarin` + `zh-hk` for HK Mandarin).
- **Fallback:** state the limit in one sentence; ask script (Han vs POJ/Tai-lo); stay standard; or offer Mandarin/English/Indonesian with technical content unchanged.
- **When asked:** clarify this is a thin scaffolded pack — prefer user examples before kental variety.

## Default register

`profesional` unless the user or use case requests another.

## When to ask

- Formal vs casual register unclear → default `profesional` for work email.
- Script (native vs Roman) unclear → ask once.
- Regional dialect named but not in overlay → ask or stay standard.
- User asked Mandarin → switch to `mandarin` pack, not this one.
