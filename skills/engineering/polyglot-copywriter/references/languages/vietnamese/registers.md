# vietnamese registers

Three registers. Default is `santai`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official, legal, academic — on request |
| Work | `profesional` | Email, docs, explanations — default for tech |
| Casual | `santai` | Chat, peer tone — on request |

## Pronouns and address

tôi / chúng tôi; bạn (peer) vs anh/chị + name (respect).

## Examples

### `baku` (formal)

- **Good:** Thông báo: dịch vụ sẽ ngừng vào thứ Ba để bảo trì.
- **Bad:** Service will be down — English order.

### `profesional` (work)

- **Good:** `API_TOKEN` không có trong `.env`, nên `loadConfig` trả về `undefined`.
- **Bad:** Kindly revert.

### `santai` (casual)

- **Good:** `.env` chưa có `API_TOKEN` — chạy `npm test -- config`.
- **Bad:** Random kinship pronouns without relationship.

## What casual is not

- Not a slang quota
- Not a license to drop grammar in incident or email text
- Speech levels (if any) are separate from `santai`
