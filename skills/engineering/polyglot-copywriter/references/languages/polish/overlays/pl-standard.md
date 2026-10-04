# pl-standard — Polish standard

**Type:** `regional` | **Status:** `validated`

## When to load

`language: polish` + `regional_voice: pl-standard`. Default overlay for Polish.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| formal pronoun | Respectful work default | `tipis+` |
| polite softener | One request soften | `tipis` |

## Examples (bug explanation)

- Brakuje `API_TOKEN` w `.env`, więc `loadConfig` zwraca `undefined`.

## Caps

- Standard Polish orthography; no dialect caricature.
- Technical literals (`API_TOKEN`, paths) unchanged.
- One overlay at a time.

## What NOT to mix

- Markers from another language pack without explicit user ask.

## Forbidden caricature

- Random English filler every sentence.
- Invented dialect spellings outside this overlay.
