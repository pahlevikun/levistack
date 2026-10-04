# french registers

Three registers. Default is `santai`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official, legal, academic — on request |
| Work | `profesional` | Email, docs, explanations — default for tech |
| Casual | `santai` | Chat, peer tone — on request |

## Pronouns and address

je / nous; tu (peer) vs vous (work).

## Examples

### `baku` (formal)

- **Good:** Nous vous informons que le service sera indisponible mardi pour maintenance.
- **Bad:** Service will be down Tuesday — English pasted.

### `profesional` (work)

- **Good:** `API_TOKEN` manque dans `.env`, donc `loadConfig` renvoie `undefined`.
- **Bad:** Kindly revert.

### `santai` (casual)

- **Good:** Il n'y a pas de `API_TOKEN` dans `.env` — lance `npm test -- config`.
- **Bad:** Franglais every noun.

## What casual is not

- Not a slang quota
- Not a license to drop grammar in incident or email text
- Speech levels (if any) are separate from `santai`
