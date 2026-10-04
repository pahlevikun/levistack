# pa-pk — Pakistan Punjabi (light)

**Type:** `regional` | **Status:** `validated`

## When to load

`language: punjabi` + `regional_voice: pa-pk`. Pakistan Punjabi — **light** overlay; Gurmukhi baseline with honesty that Shahmukhi is not fully covered.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `ਤੁਸੀਂ` / respectful forms | Work default | `tipis+` |
| Pakistan context | Ask script (Gurmukhi vs Shahmukhi) if sustained | `tipis` |
| `ਕਿਰਪਾ ਕਰਕੇ` | Softener | `tipis+` |

## Examples (bug explanation)

- `.env` ਵਿੱਚ `API_TOKEN` ਨਹੀਂ, ਇਸ ਲਈ `loadConfig` `undefined` ਦਿੰਦਾ ਹੈ। `npm test -- config` ਚਲਾਓ।

## Caps

- **Light** — say when Shahmukhi or deep Pakistan lexicon is needed beyond pack.
- Prefer user examples for administrative Pakistan Punjabi.

## What NOT to mix

- India-only idioms that clash with Pakistan context.

## Forbidden caricature

- Invented Shahmukhi without user-provided samples.
