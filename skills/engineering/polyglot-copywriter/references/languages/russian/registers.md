# russian registers

Three registers. Default is `santai`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official letters, legal, investor — on request |
| Work | `profesional` | Email, docs, LinkedIn — on request |
| Casual | `santai` | **Default**: chat, explanations, everyday writing |

## Pronouns and address

я / мы; вы (work default); ты only when user signals close peer chat.

## Examples

### `baku` (formal)

- **Good:** Сообщаем, что во вторник сервис будет недоступен из‑за обслуживания.
- **Bad:** Service will be down Tuesday — English calque.

### `profesional` (work)

- **Good:** `API_TOKEN` нет в `.env`, поэтому `loadConfig` возвращает `undefined`.
- **Bad:** Kindly revert the configuration.

### `santai` (casual)

- **Good:** `API_TOKEN` в `.env` нет — запусти `npm test -- config`.
- **Bad:** Fake mat or 90s slang in incident text.

## What casual is not

- Not ты to executives without signal
- Not transliterated English every noun
