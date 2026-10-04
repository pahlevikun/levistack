# afrikaans registers

Three registers. Default is `profesional`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, academic — on request |
| Work | `profesional` | Email, docs, status updates — **default** for work |
| Casual | `santai` | Chat, explanations, everyday writing |

## Pronouns and address

Standard Afrikaans pronouns — formal for external work; casual only when user set tone.

## Examples

### `baku` (formal)

- **Good:** Hiermee word kennis gegee dat die diens Dinsdag onderhoud ondergaan.
- **Bad:** Service will be down Tuesday — English pasted without natural grammar.

### `profesional` (work)

- **Good:** `API_TOKEN` is nie in `.env` nie, so `loadConfig` gee `undefined` terug.
- **Bad:** Kindly revert regarding the token issue.

### `santai` (casual)

- **Good:** Geen `API_TOKEN` in `.env` — hardloop `npm test -- config`.
- **Bad:** Random dialect mix or English filler in every Afrikaans sentence.

## What casual is not

- Not English sentence with one Afrikaans word
- Not slang quota in incident or customer email
