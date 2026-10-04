# tagalog registers

Three registers. Default is `santai`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official, legal, academic — on request |
| Work | `profesional` | Email, docs, explanations — default for tech |
| Casual | `santai` | Chat, peer tone — on request |

## Pronouns and address

ako / kami; ikaw (close) vs po/ho respect particles in work.

## Examples

### `baku` (formal)

- **Good:** Ipinapaalam na ang serbisyo ay hindi magagamit sa Martes para sa maintenance.
- **Bad:** Service will be down — English pasted.

### `profesional` (work)

- **Good:** Wala ang `API_TOKEN` sa `.env`, kaya `undefined` ang ibinabalik ng `loadConfig`.
- **Bad:** Kindly revert.

### `santai` (casual)

- **Good:** Walang `API_TOKEN` sa `.env` — patakbuhin ang `npm test -- config`.
- **Bad:** Taglish every word without overlay.

## What casual is not

- Not a slang quota
- Not a license to drop grammar in incident or email text
- Speech levels (if any) are separate from `santai`
