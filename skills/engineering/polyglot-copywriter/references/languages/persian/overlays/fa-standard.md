# fa-standard — Persian standard

**Type:** `regional` | **Status:** `validated`

## When to load

`language: persian` + `regional_voice: fa-standard`. Default overlay for Persian.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| formal pronoun | Respectful work default | `tipis+` |
| polite softener | One request soften | `tipis` |

## Examples (bug explanation)

- `API_TOKEN` در `.env` نیست؛ `loadConfig` مقدار `undefined` برمی‌گرداند.

## Caps

- Standard Persian orthography; no dialect caricature.
- Technical literals (`API_TOKEN`, paths) unchanged.
- One overlay at a time.

## What NOT to mix

- Markers from another language pack without explicit user ask.

## Forbidden caricature

- Random English filler every sentence.
- Invented dialect spellings outside this overlay.
