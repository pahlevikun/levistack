# ta-in — India Tamil

**Type:** `regional` | **Status:** `validated`

## When to load

`language: tamil` + `regional_voice: ta-in`. Tamil Nadu / India standard Tamil — default overlay.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `நீங்கள்` | Respectful work default | `tipis+` |
| `தயவுசெய்து` | Softener on requests | `tipis+` |
| `அதனால்` | Therefore | `tipis+` |

## Examples (bug explanation)

- `.env` இல் `API_TOKEN` இல்லை, அதனால் `loadConfig` `undefined` தருகிறது. `npm test -- config` இயக்கவும், தயவுசெய்து.

## Caps

- Default India Tamil; Tamil script unless user asked Roman.

## What NOT to mix

- Sri Lanka-specific administrative vocabulary without `ta-lk`.

## Forbidden caricature

- Random Tanglish in formal email.
