# pa-in — India Punjabi (Gurmukhi)

**Type:** `regional` | **Status:** `validated`

## When to load

`language: punjabi` + `regional_voice: pa-in`. India Punjabi in Gurmukhi script — default overlay.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `ਤੁਸੀਂ` | Respectful work default | `tipis+` |
| `ਕਿਰਪਾ ਕਰਕੇ` | Softener on requests | `tipis+` |
| `ਇਸ ਲਈ` | Therefore | `tipis+` |

## Examples (bug explanation)

- `.env` ਵਿੱਚ `API_TOKEN` ਨਹੀਂ ਹੈ, ਇਸ ਲਈ `loadConfig` `undefined` ਦਿੰਦਾ ਹੈ। `npm test -- config` ਚਲਾਓ, ਕਿਰਪਾ ਕਰਕੇ।

## Caps

- Gurmukhi script default; not Shahmukhi.

## What NOT to mix

- Pakistan Urdu-script forms when `pa-in` active.

## Forbidden caricature

- Random Hindi/Urdu words without user mix request.
