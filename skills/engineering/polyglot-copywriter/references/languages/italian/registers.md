# italian registers

Three registers. Default is `profesional` for work contexts.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, investor — on request |
| Work | `profesional` | Email, docs, LinkedIn — **default** |
| Casual | `santai` | Chat, explanations, everyday writing |

## Pronouns and address

io / noi; Lei (formal work default); tu when peer chat is explicit.

## Examples

### `baku` (formal)

- **Good:** La informiamo che il servizio sarà sospeso martedì per manutenzione programmata.
- **Bad:** The service will be down Tuesday — English pasted.

### `profesional` (work)

- **Good:** `API_TOKEN` manca in `.env`, quindi `loadConfig` restituisce `undefined`. Eseguire `npm test -- config`.
- **Bad:** Please kindly revert.

### `santai` (casual)

- **Good:** Manca `API_TOKEN` in `.env` — lancia `npm test -- config`.
- **Bad:** Fake Roman dialect spelling without overlay.

## What casual is not

- Not tu in customer email without brand permission
- Not English verbs unintegrated
