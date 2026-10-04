# portuguese registers

Three registers. Default is `santai`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official, legal, academic — on request |
| Work | `profesional` | Email, docs, explanations — default for tech |
| Casual | `santai` | Chat, peer tone — on request |

## Pronouns and address

eu / nós; tu/você (BR) vs você (formal).

## Examples

### `baku` (formal)

- **Good:** Informamos que o serviço ficará indisponível na terça-feira para manutenção.
- **Bad:** Service will be down — English order.

### `profesional` (work)

- **Good:** `API_TOKEN` não está no `.env`, então `loadConfig` retorna `undefined`.
- **Bad:** Kindly revert.

### `santai` (casual)

- **Good:** Não tem `API_TOKEN` no `.env` — roda `npm test -- config`.
- **Bad:** pt-pt and pt-br mixed without overlay.

## What casual is not

- Not a slang quota
- Not a license to drop grammar in incident or email text
- Speech levels (if any) are separate from `santai`
