# pt-pt — European Portuguese

**Type:** `regional` | **Status:** `validated`

## When to load

`language: portuguese` + `regional_voice: pt-pt`. Portugal Portuguese — not Brazilian default.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `tu/você` | Match formality; PT-PT often avoids Brazilian você default in formal | `tipis+` |
| `ecrã` | Screen (PT) | `tipis+` |
| `ficheiro` | File (PT) | `tipis+` |
| `está a` | Progressive (PT-PT) | `tipis+` |

## Examples (bug explanation)

- Falta `API_TOKEN` no `.env`, por isso `loadConfig` devolve `undefined`. Execute `npm test -- config`.

## Caps

- Do not use Brazilian a gente/tá as default.

## What NOT to mix

- pt-br overlay markers in pt-pt output.

## Forbidden caricature

- pt-br overlay markers in pt-pt output.
