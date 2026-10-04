# es-pe — Peru Spanish

**Type:** `regional` | **Status:** `validated`

## When to load

`language: spanish` + `regional_voice: es-pe`. Peruvian Spanish — neutral Latin American work tone.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `usted` | Default polite for work | `tipis+` |
| `por favor` / `porfa` | Softener (`porfa` casual only) | `tipis+` |
| `ya` | Acknowledgment / already done | `tipis` |
| `entonces` | Therefore | `tipis+` |

## Examples (bug explanation)

- Falta `API_TOKEN` en `.env`, entonces `loadConfig` devuelve `undefined`. Ejecute `npm test -- config`, por favor.

## Caps

- Peru lexicon light — `chamba` only in `santai` if at all.
- Not Mexico-only slang as default.

## What NOT to mix

- Caribbean or Argentine markers unless user switched overlay.

## Forbidden caricature

- Comic Andean spelling in formal email.
