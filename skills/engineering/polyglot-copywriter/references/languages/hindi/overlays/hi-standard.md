# hi-standard — Standard Hindi (Delhi / national)

**Type:** `regional` | **Status:** `validated`

## When to load

`language: hindi` + `regional_voice: hi-standard` or `netral`. Khari Boli baseline for work.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `है／हैं` | Present state copula | `tipis+` |
| `नहीं` | Negation — clear diagnostic | `tipis+` |
| `इसलिए` | Therefore — cause link | `tipis+` |

## Examples (bug explanation)

- `.env` में `API_TOKEN` नहीं है, इसलिए `loadConfig` `undefined` लौटा रहा है। `npm test -- config` चलाएँ।

## Caps

- Default Hindi regional — Hinglish is separate mix overlay.

## What NOT to mix

- Random English insertions (Hinglish) without mix overlay.

## Forbidden caricature

- Random English insertions (Hinglish) without mix overlay.
