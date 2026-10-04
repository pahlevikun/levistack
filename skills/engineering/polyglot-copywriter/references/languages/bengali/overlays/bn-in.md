# bn-in — West Bengal Bengali

**Type:** `regional` | **Status:** `validated`

## When to load

`language: bengali` + `regional_voice: bn-in`. Kolkata/West Bengal standard prose.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `নেই` | Absent/not there | `tipis+` |
| `তাই` | Therefore | `tipis+` |
| `হচ্ছে` | Ongoing state (returns undefined) | `tipis+` |

## Examples (bug explanation)

- `.env`-এ `API_TOKEN` নেই, তাই `loadConfig` `undefined` ফেরত দিচ্ছে। `npm test -- config` চালান।

## Caps

- India Bengali script and vocabulary default.

## What NOT to mix

- Bangladesh-specific spelling in bn-in output.

## Forbidden caricature

- Bangladesh-specific spelling in bn-in output.
