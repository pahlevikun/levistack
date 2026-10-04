# polish registers

Three registers. Default is `profesional`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, academic — on request |
| Work | `profesional` | Email, docs, status updates — **default** for work |
| Casual | `santai` | Chat, explanations, everyday writing |

## Pronouns and address

Standard Polish pronouns — formal for external work; casual only when user set tone.

## Examples

### `baku` (formal)

- **Good:** Informujemy, że usługa będzie niedostępna we wtorek z powodu konserwacji.
- **Bad:** Service will be down Tuesday — English pasted without natural grammar.

### `profesional` (work)

- **Good:** Brakuje `API_TOKEN` w `.env`, więc `loadConfig` zwraca `undefined`.
- **Bad:** Kindly revert regarding the token issue.

### `santai` (casual)

- **Good:** Nie ma `API_TOKEN` w `.env` — odpal `npm test -- config`.
- **Bad:** Random dialect mix or English filler in every Polish sentence.

## What casual is not

- Not English sentence with one Polish word
- Not slang quota in incident or customer email
