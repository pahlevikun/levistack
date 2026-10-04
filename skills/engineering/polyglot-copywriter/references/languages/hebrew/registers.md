# hebrew registers

Three registers. Default is `profesional`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, academic — on request |
| Work | `profesional` | Email, docs, status updates — **default** for work |
| Casual | `santai` | Chat, explanations, everyday writing |

## Pronouns and address

Standard Hebrew pronouns — formal for external work; casual only when user set tone.

## Examples

### `baku` (formal)

- **Good:** הודעה: השירות יושבת ביום שלישי לצורך תחזוקה.
- **Bad:** Service will be down Tuesday — English pasted without natural grammar.

### `profesional` (work)

- **Good:** חסר `API_TOKEN` ב־`.env`, ולכן `loadConfig` מחזיר `undefined`.
- **Bad:** Kindly revert regarding the token issue.

### `santai` (casual)

- **Good:** אין `API_TOKEN` ב־`.env` — תריץ `npm test -- config`.
- **Bad:** Random dialect mix or English filler in every Hebrew sentence.

## What casual is not

- Not English sentence with one Hebrew word
- Not slang quota in incident or customer email
