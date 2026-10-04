# af-standard — Afrikaans standard

**Type:** `regional` | **Status:** `validated`

## When to load

`language: afrikaans` + `regional_voice: af-standard`. Default overlay for Afrikaans.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| formal pronoun | Respectful work default | `tipis+` |
| polite softener | One request soften | `tipis` |

## Examples (bug explanation)

- `API_TOKEN` is nie in `.env` nie, so `loadConfig` gee `undefined` terug.

## Caps

- Standard Afrikaans orthography; no dialect caricature.
- Technical literals (`API_TOKEN`, paths) unchanged.
- One overlay at a time.

## What NOT to mix

- Markers from another language pack without explicit user ask.

## Forbidden caricature

- Random English filler every sentence.
- Invented dialect spellings outside this overlay.
