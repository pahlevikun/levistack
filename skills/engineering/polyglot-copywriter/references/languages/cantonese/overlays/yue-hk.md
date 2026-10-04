# yue-hk — Cantonese standard

**Type:** `regional` | **Status:** `validated`

## When to load

`language: cantonese` + `regional_voice: yue-hk`. Default overlay for Cantonese.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| formal pronoun | Respectful work default | `tipis+` |
| polite softener | One request soften | `tipis` |

## Examples (bug explanation)

- `.env` 冇 `API_TOKEN`，所以 `loadConfig` 返回 `undefined`。

## Caps

- Standard Cantonese orthography; no dialect caricature.
- Technical literals (`API_TOKEN`, paths) unchanged.
- One overlay at a time.

## What NOT to mix

- Markers from another language pack without explicit user ask.

## Forbidden caricature

- Random English filler every sentence.
- Invented dialect spellings outside this overlay.
