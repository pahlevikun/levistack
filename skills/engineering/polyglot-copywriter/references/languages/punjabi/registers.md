# punjabi registers

Three registers. Default is `profesional` for work contexts.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal — on request |
| Work | `profesional` | Email, docs, status — **default** |
| Casual | `santai` | Chat, explanations |

## Pronouns and address

ਮੈਂ / ਅਸੀਂ; ਤੁਸੀਂ (respectful work default); ਤੂੰ in close peer chat only when user set that tone.

## Examples

### `baku` (formal)

- **Good:** ਸਾਨੂੰ ਸੂਚਿਤ ਕਰਨਾ ਹੈ ਕਿ ਸੇਵਾ ਮੰਗਲਵਾਰ ਨੂੰ ਰੱਖ-ਰਖਾਅ ਲਈ ਬੰਦ ਰਹੇਗੀ।
- **Bad:** Service will be down Tuesday — English pasted.

### `profesional` (work)

- **Good:** `.env` ਵਿੱਚ `API_TOKEN` ਨਹੀਂ ਹੈ, ਇਸ ਲਈ `loadConfig` `undefined` ਦਿੰਦਾ ਹੈ। `npm test -- config` ਚਲਾਓ।
- **Bad:** Please kindly revert.

### `santai` (casual)

- **Good:** `.env` ਵਿੱਚ `API_TOKEN` ਨੀਂ — `npm test -- config` ਚਲਾ ਲੈ।
- **Bad:** Random Urdu mix without overlay.

## What casual is not

- Not ਤੂੰ in customer email
- Not Pakistan Shahmukhi when `pa-in` overlay active
