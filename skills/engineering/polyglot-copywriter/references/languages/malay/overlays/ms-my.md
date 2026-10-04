# ms-my — Malaysia Malay

**Type:** `regional` | **Status:** `validated`

## When to load

`language: malay` + `regional_voice: ms-my`. Malaysian Malay baseline.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `tiada` | Absent (MY preference in formal) | `tipis+` |
| `jadi` | Therefore/so | `tipis+` |
| `sila` | Please (work polite) | `tipis+` |

## Examples (bug explanation)

- `API_TOKEN` tiada dalam `.env`, jadi `loadConfig` memulangkan `undefined`. Sila jalankan `npm test -- config`.

## Caps

- Manglish is separate mix overlay.

## What NOT to mix

- Indonesian jakarta particles in ms-my output.

## Forbidden caricature

- Indonesian jakarta particles in ms-my output.
