# hokkien registers

Three registers. Default is `profesional`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, academic — on request |
| Work | `profesional` | Email, docs, status updates — **default** for work |
| Casual | `santai` | Chat, explanations, everyday writing |

## Pronouns and address

Standard Hokkien pronouns — formal for external work; casual only when user set tone.

## Examples

### `baku` (formal)

- **Good:** 通知：服務禮拜二會停機維修。
- **Bad:** Service will be down Tuesday — English pasted without natural grammar.

### `profesional` (work)

- **Good:** `.env` 無 `API_TOKEN`，所以 `loadConfig` 回傳 `undefined`。
- **Bad:** Kindly revert regarding the token issue.

### `santai` (casual)

- **Good:** `.env` 無 `API_TOKEN` — 跑 `npm test -- config`。
- **Bad:** Random dialect mix or English filler in every Hokkien sentence.

## What casual is not

- Not English sentence with one Hokkien word
- Not slang quota in incident or customer email
