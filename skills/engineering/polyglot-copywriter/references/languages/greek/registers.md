# greek registers

Three registers. Default is `profesional`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, academic — on request |
| Work | `profesional` | Email, docs, status updates — **default** for work |
| Casual | `santai` | Chat, explanations, everyday writing |

## Pronouns and address

Standard Greek pronouns — formal for external work; casual only when user set tone.

## Examples

### `baku` (formal)

- **Good:** Ενημερώνουμε ότι η υπηρεσία θα διακοπεί την Τρίτη για συντήρηση.
- **Bad:** Service will be down Tuesday — English pasted without natural grammar.

### `profesional` (work)

- **Good:** Το `API_TOKEN` λείπει από το `.env`, οπότε το `loadConfig` επιστρέφει `undefined`.
- **Bad:** Kindly revert regarding the token issue.

### `santai` (casual)

- **Good:** Δεν έχει `API_TOKEN` στο `.env` — τρέξε `npm test -- config`.
- **Bad:** Random dialect mix or English filler in every Greek sentence.

## What casual is not

- Not English sentence with one Greek word
- Not slang quota in incident or customer email
