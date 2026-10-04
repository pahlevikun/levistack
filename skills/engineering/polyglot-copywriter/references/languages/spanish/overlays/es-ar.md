# es-ar — Argentina Spanish

**Type:** `regional` | **Status:** `validated`

## When to load

`language: spanish` + `regional_voice: es-ar`. Rioplatense voseo for casual; usted for formal work.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `vos + verb` | Casual address when register is santai | `sedang+` |
| `usted` | External/formal work email | `tipis+` |
| `che` | Peer attention (casual only, rare) | `sedang+` |
| `acá／aquí` | Local deictic preference | `tipis+` |

## Examples (bug explanation)

- Falta `API_TOKEN` en `.env`, por eso `loadConfig` devuelve `undefined`. Probá `npm test -- config`.

## Caps

- Match tú/usted/vos to register and audience.

## What NOT to mix

- Spain vosotros default; che in formal client email.

## Forbidden caricature

- Spain vosotros default; che in formal client email.
