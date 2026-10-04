# es-cl — Chile Spanish

**Type:** `regional` | **Status:** `validated`

## When to load

`language: spanish` + `regional_voice: es-cl`. Chilean Spanish — professional default with light Chilean markers in casual only.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `usted` | Work email default | `tipis+` |
| `tú` | Internal casual when user set tone | `tipis+` |
| `por favor` | Softener | `tipis+` |
| `entonces` / `po` | Transition (`po` **santai only**, light) | `tipis` |

## Examples (bug explanation)

- No está `API_TOKEN` en `.env`, entonces `loadConfig` devuelve `undefined`. Ejecute `npm test -- config`, por favor.

## Caps

- `po` and heavy Chilean colloquial only in `santai`.
- Not Argentina voseo unless user asked es-ar.

## What NOT to mix

- Mexico `computadora` vs Chile `computador` — pick Chile forms in this overlay.

## Forbidden caricature

- `po` in every sentence or in incident status page.
