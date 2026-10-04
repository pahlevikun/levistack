# si-standard — Sinhala standard

**Type:** `regional` | **Status:** `validated`

## When to load

`language: sinhala` + `regional_voice: si-standard`. Default overlay for Sinhala.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| formal pronoun | Respectful work default | `tipis+` |
| polite softener | One request soften | `tipis` |

## Examples (bug explanation)

- `API_TOKEN` missing in `.env`; `loadConfig` returns `undefined`. Run `npm test -- config`.

## Caps

- Standard Sinhala orthography; no dialect caricature.
- Technical literals (`API_TOKEN`, paths) unchanged.
- One overlay at a time.

## What NOT to mix

- Markers from another language pack without explicit user ask.

## Forbidden caricature

- Random English filler every sentence.
- Invented dialect spellings outside this overlay.
