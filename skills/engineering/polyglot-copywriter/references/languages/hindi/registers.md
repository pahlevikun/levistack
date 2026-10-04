# hindi registers

Three registers. Default is `santai`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official, legal, academic — on request |
| Work | `profesional` | Email, docs, explanations — default for tech |
| Casual | `santai` | Chat, peer tone — on request |

## Pronouns and address

मैं / हम; तुम (close) vs आप (work).

## Examples

### `baku` (formal)

- **Good:** सूचित किया जाता है कि मंगलवार को रखरखाव के लिए सेवा बंद रहेगी।
- **Bad:** Service will be down — English order.

### `profesional` (work)

- **Good:** `API_TOKEN` `.env` में नहीं है, इसलिए `loadConfig` `undefined` लौटाता है।
- **Bad:** Kindly revert.

### `santai` (casual)

- **Good:** `API_TOKEN` `.env` में नहीं — `npm test -- config` चला लो।
- **Bad:** Hinglish every word without ask.

## What casual is not

- Not a slang quota
- Not a license to drop grammar in incident or email text
- Speech levels (if any) are separate from `santai`
