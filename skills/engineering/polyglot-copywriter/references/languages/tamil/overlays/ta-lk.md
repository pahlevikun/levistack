# ta-lk — Sri Lanka Tamil (light)

**Type:** `regional` | **Status:** `validated`

## When to load

`language: tamil` + `regional_voice: ta-lk`. Sri Lanka Tamil — **light** overlay; India Tamil baseline with SL-appropriate vocabulary where documented.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `நீங்கள்` | Respectful work default | `tipis+` |
| SL lexicon light | Only when user names Sri Lanka context | `tipis` |
| `தயவுசெய்து` | Softener | `tipis+` |

## Examples (bug explanation)

- `.env` கோப்பில் `API_TOKEN` இல்லை, அதனால் `loadConfig` `undefined` தருகிறது. `npm test -- config` இயக்கவும்.

## Caps

- **Light** — limited SL-specific forms in pack; ask for user examples for deep administrative style.
- Not Sinhala mix unless user asked.

## What NOT to mix

- Heavy India-only colloquialisms that read wrong in SL context.

## Forbidden caricature

- Invented Sri Lankan spellings not in user examples.
