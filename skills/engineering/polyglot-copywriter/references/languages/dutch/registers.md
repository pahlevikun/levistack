# dutch registers

Three registers. Default is `profesional`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, academic — on request |
| Work | `profesional` | Email, docs, status updates — **default** for work |
| Casual | `santai` | Chat, explanations, everyday writing |

## Pronouns and address

Standard Dutch pronouns — formal for external work; casual only when user set tone.

## Examples

### `baku` (formal)

- **Good:** Hierbij informeren wij u dat de dienst dinsdag onderhoud krijgt.
- **Bad:** Service will be down Tuesday — English pasted without natural grammar.

### `profesional` (work)

- **Good:** `API_TOKEN` staat niet in `.env`, dus `loadConfig` geeft `undefined` terug.
- **Bad:** Kindly revert regarding the token issue.

### `santai` (casual)

- **Good:** Geen `API_TOKEN` in `.env` — run `npm test -- config`.
- **Bad:** Random dialect mix or English filler in every Dutch sentence.

## What casual is not

- Not English sentence with one Dutch word
- Not slang quota in incident or customer email
