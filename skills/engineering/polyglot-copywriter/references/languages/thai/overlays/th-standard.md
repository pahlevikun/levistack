# th-standard — Thai standard

**Type:** `regional` | **Status:** `validated`

## When to load

`language: thai` + `regional_voice: th-standard`. Default overlay for Thai.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| formal pronoun | Respectful work default | `tipis+` |
| polite softener | One request soften | `tipis` |

## Examples (bug explanation)

- ไม่มี `API_TOKEN` ใน `.env` เลย `loadConfig` คืนค่า `undefined`

## Caps

- Standard Thai orthography; no dialect caricature.
- Technical literals (`API_TOKEN`, paths) unchanged.
- One overlay at a time.

## What NOT to mix

- Markers from another language pack without explicit user ask.

## Forbidden caricature

- Random English filler every sentence.
- Invented dialect spellings outside this overlay.
