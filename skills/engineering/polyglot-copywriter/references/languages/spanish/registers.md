# spanish registers

Three registers. Default is `santai`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official, legal, academic — on request |
| Work | `profesional` | Email, docs, explanations — default for tech |
| Casual | `santai` | Chat, peer tone — on request |

## Pronouns and address

yo / nosotros; tú (peer) vs usted (work external).

## Examples

### `baku` (formal)

- **Good:** Se informa que el servicio estará indisponible el martes por mantenimiento.
- **Bad:** The service will be down Tuesday — English calque.

### `profesional` (work)

- **Good:** Falta `API_TOKEN` en `.env`, así que `loadConfig` devuelve `undefined`.
- **Bad:** Kindly revert the configuration.

### `santai` (casual)

- **Good:** No está el `API_TOKEN` en `.env` — corre `npm test -- config`.
- **Bad:** Random regional slang mix (es-ar + es-mx).

## What casual is not

- Not a slang quota
- Not a license to drop grammar in incident or email text
- Speech levels (if any) are separate from `santai`
