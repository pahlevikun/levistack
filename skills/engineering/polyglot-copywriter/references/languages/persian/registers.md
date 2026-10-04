# persian registers

Three registers. Default is `profesional`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, academic — on request |
| Work | `profesional` | Email, docs, status updates — **default** for work |
| Casual | `santai` | Chat, explanations, everyday writing |

## Pronouns and address

Standard Persian pronouns — formal for external work; casual only when user set tone.

## Examples

### `baku` (formal)

- **Good:** به اطلاع می‌رساند سرویس روز سه‌شنبه برای نگهداری قطع می‌شود.
- **Bad:** Service will be down Tuesday — English pasted without natural grammar.

### `profesional` (work)

- **Good:** `API_TOKEN` در `.env` نیست؛ `loadConfig` مقدار `undefined` برمی‌گرداند.
- **Bad:** Kindly revert regarding the token issue.

### `santai` (casual)

- **Good:** `API_TOKEN` توی `.env` نیست — `npm test -- config` بزن.
- **Bad:** Random dialect mix or English filler in every Persian sentence.

## What casual is not

- Not English sentence with one Persian word
- Not slang quota in incident or customer email
