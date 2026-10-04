# burmese registers

Three registers. Default is `profesional`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, academic — on request |
| Work | `profesional` | Email, docs, status updates — **default** for work |
| Casual | `santai` | Chat, explanations, everyday writing |

## Pronouns and address

Standard Burmese pronouns — formal for external work; casual only when user set tone.

## Examples

### `baku` (formal)

- **Good:** [Formal Burmese maintenance notice — use standard orthography.]
- **Bad:** Service will be down Tuesday — English pasted without natural grammar.

### `profesional` (work)

- **Good:** `API_TOKEN` missing in `.env`; `loadConfig` returns `undefined`. Run `npm test -- config`.
- **Bad:** Kindly revert regarding the token issue.

### `santai` (casual)

- **Good:** No `API_TOKEN` in `.env` — run `npm test -- config`.
- **Bad:** Random dialect mix or English filler in every Burmese sentence.

## What casual is not

- Not English sentence with one Burmese word
- Not slang quota in incident or customer email
