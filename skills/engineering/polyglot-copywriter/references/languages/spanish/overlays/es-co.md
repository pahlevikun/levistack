# es-co — Colombia Spanish

**Type:** `regional` | **Status:** `validated`

## When to load

`language: spanish` + `regional_voice: es-co`. Colombian Spanish — polite default, clear work tone.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `usted` | Default polite for work unless user asked casual tú | `tipis+` |
| `por favor／si puede` | Softener on requests | `tipis+` |
| `listo` | Acknowledgment / ready to proceed | `tipis+` |
| `entonces` | Therefore in explanation | `tipis+` |

## Examples (bug explanation)

- No está `API_TOKEN` en `.env`, entonces `loadConfig` devuelve `undefined`. Ejecute `npm test -- config`, por favor.

## Caps

- Do not use Mexico-only slang as default.

## What NOT to mix

- Random voseo unless user asked Argentine-style.

## Forbidden caricature

- Random voseo unless user asked Argentine-style.
