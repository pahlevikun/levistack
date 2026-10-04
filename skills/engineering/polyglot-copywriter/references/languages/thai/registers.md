# thai registers

Three registers. Default is `profesional`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, academic — on request |
| Work | `profesional` | Email, docs, status updates — **default** for work |
| Casual | `santai` | Chat, explanations, everyday writing |

## Pronouns and address

Standard Thai pronouns — formal for external work; casual only when user set tone.

## Examples

### `baku` (formal)

- **Good:** แจ้งให้ทราบว่าบริการจะหยุดให้บริการวันอังคารเพื่อบำรุงรักษา
- **Bad:** Service will be down Tuesday — English pasted without natural grammar.

### `profesional` (work)

- **Good:** ไม่มี `API_TOKEN` ใน `.env` เลย `loadConfig` คืนค่า `undefined`
- **Bad:** Kindly revert regarding the token issue.

### `santai` (casual)

- **Good:** `.env` ไม่มี `API_TOKEN` — รัน `npm test -- config` นะ
- **Bad:** Random dialect mix or English filler in every Thai sentence.

## What casual is not

- Not English sentence with one Thai word
- Not slang quota in incident or customer email
