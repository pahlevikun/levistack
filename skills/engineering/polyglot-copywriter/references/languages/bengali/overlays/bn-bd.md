# bn-bd — Bangladesh Bengali

**Type:** `regional` | **Status:** `validated`

## When to load

`language: bengali` + `regional_voice: bn-bd`. Bangladesh standard prose.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `নেই` | Absent | `tipis+` |
| `তাই` | Therefore | `tipis+` |
| `হচ্ছে` | Ongoing/result state | `tipis+` |

## Examples (bug explanation)

- `.env`-এ `API_TOKEN` নেই, তাই `loadConfig` `undefined` রিটার্ন করছে। `npm test -- config` চালান।

## Caps

- Bangladesh usage — do not force Kolkata idioms.

## What NOT to mix

- West Bengal-only lexical choices presented as BD default.

## Forbidden caricature

- West Bengal-only lexical choices presented as BD default.
