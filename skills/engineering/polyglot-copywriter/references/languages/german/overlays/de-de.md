# de-de — Germany German

**Type:** `regional` | **Status:** `validated`

## When to load

`language: german` + `regional_voice: de-de`. Standard Germany German.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `Sie` | Formal work default | `tipis+` |
| `nicht` | Negation | `tipis+` |
| `deshalb` | Therefore | `tipis+` |

## Examples (bug explanation)

- `API_TOKEN` fehlt in `.env`, deshalb gibt `loadConfig` `undefined` zurück. Führen Sie `npm test -- config` aus.

## Caps

- Default German overlay.

## What NOT to mix

- Swiss ß/ss or Austrian particles in de-de output.

## Forbidden caricature

- Swiss ß/ss or Austrian particles in de-de output.
