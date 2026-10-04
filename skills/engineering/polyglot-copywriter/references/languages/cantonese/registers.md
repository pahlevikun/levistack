# cantonese registers

Three registers. Default is `profesional`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, academic — on request |
| Work | `profesional` | Email, docs, status updates — **default** for work |
| Casual | `santai` | Chat, explanations, everyday writing |

## Pronouns and address

Standard Cantonese pronouns — formal for external work; casual only when user set tone.

## Examples

### `baku` (formal)

- **Good:** 特此通知：服務將於星期二維護期間暫停。
- **Bad:** Service will be down Tuesday — English pasted without natural grammar.

### `profesional` (work)

- **Good:** `.env` 冇 `API_TOKEN`，所以 `loadConfig` 返回 `undefined`。
- **Bad:** Kindly revert regarding the token issue.

### `santai` (casual)

- **Good:** `.env` 冇 `API_TOKEN` — 跑 `npm test -- config`。
- **Bad:** Random dialect mix or English filler in every Cantonese sentence.

## What casual is not

- Not English sentence with one Cantonese word
- Not slang quota in incident or customer email
