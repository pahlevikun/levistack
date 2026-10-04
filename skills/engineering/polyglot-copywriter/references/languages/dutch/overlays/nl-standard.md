# nl-standard — Dutch standard

**Type:** `regional` | **Status:** `validated`

## When to load

`language: dutch` + `regional_voice: nl-standard`. Default overlay for Dutch.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| formal pronoun | Respectful work default | `tipis+` |
| polite softener | One request soften | `tipis` |

## Examples (bug explanation)

- `API_TOKEN` staat niet in `.env`, dus `loadConfig` geeft `undefined` terug.

## Caps

- Standard Dutch orthography; no dialect caricature.
- Technical literals (`API_TOKEN`, paths) unchanged.
- One overlay at a time.

## What NOT to mix

- Markers from another language pack without explicit user ask.

## Forbidden caricature

- Random English filler every sentence.
- Invented dialect spellings outside this overlay.
