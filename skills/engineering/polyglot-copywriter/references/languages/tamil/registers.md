# tamil registers

Three registers. Default is `profesional` for work contexts.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, academic — on request |
| Work | `profesional` | Email, docs, status updates — **default** |
| Casual | `santai` | Chat, explanations, everyday writing |

## Pronouns and address

நான் / நாங்கள்; நீங்கள் (respectful default in work); நீ in close peer chat only when user set that tone.

## Examples

### `baku` (formal)

- **Good:** சேவை செவ்வாய்க்கிழமை பராமரிப்பு காரணமாக இடைநிறுத்தப்படும் என்பதை தெரிவித்துக் கொள்கிறோம்.
- **Bad:** Service will be down Tuesday — English pasted.

### `profesional` (work)

- **Good:** `.env` இல் `API_TOKEN` இல்லை, அதனால் `loadConfig` `undefined` தருகிறது. `npm test -- config` இயக்கவும்.
- **Bad:** Please kindly revert.

### `santai` (casual)

- **Good:** `.env` ல `API_TOKEN` இல்ல — `npm test -- config` ரன் பண்ணு.
- **Bad:** Random Tanglish without user asking mix.

## What casual is not

- Not நீ in customer email
- Not full English sentence with one Tamil word
