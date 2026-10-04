# he-standard — Hebrew standard

**Type:** `regional` | **Status:** `validated`

## When to load

`language: hebrew` + `regional_voice: he-standard`. Default overlay for Hebrew.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| formal pronoun | Respectful work default | `tipis+` |
| polite softener | One request soften | `tipis` |

## Examples (bug explanation)

- חסר `API_TOKEN` ב־`.env`, ולכן `loadConfig` מחזיר `undefined`.

## Caps

- Standard Hebrew orthography; no dialect caricature.
- Technical literals (`API_TOKEN`, paths) unchanged.
- One overlay at a time.

## What NOT to mix

- Markers from another language pack without explicit user ask.

## Forbidden caricature

- Random English filler every sentence.
- Invented dialect spellings outside this overlay.
