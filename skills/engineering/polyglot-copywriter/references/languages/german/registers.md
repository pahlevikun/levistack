# german registers

Three registers. Default is `santai`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, investor — on request |
| Work | `profesional` | Email, docs, LinkedIn — on request |
| Casual | `santai` | **Default**: chat, explanations, everyday writing |

## Pronouns and address

ich / wir; Sie (work default); du when peer chat is explicit.

## Examples

### `baku` (formal)

- **Good:** Hiermit teilen wir mit, dass der Dienst am Dienstag wegen Wartung ausfällt.
- **Bad:** The service will be down Tuesday — English pasted.

### `profesional` (work)

- **Good:** `API_TOKEN` fehlt in `.env`, deshalb gibt `loadConfig` `undefined` zurück.
- **Bad:** Please kindly revert.

### `santai` (casual)

- **Good:** `API_TOKEN` fehlt in `.env` — starte `npm test -- config`.
- **Bad:** Fake Bayerisch spelling without overlay.

## What casual is not

- Not du in customer email
- Not English verbs unintegrated
