# mandarin registers

Three registers. Default is `santai`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official, legal, academic — on request |
| Work | `profesional` | Email, docs, explanations — default for tech |
| Casual | `santai` | Chat, peer tone — on request |

## Pronouns and address

我 / 我们；你 (peer) vs 您 (respect/work). Overlay picks 简体/繁體.

## Examples

### `baku` (formal)

- **Good:** 谨通知：服务将于周二维护期间暂停。
- **Bad:** The service will be down Tuesday — English SVO pasted.

### `profesional` (work)

- **Good:** 原因是 `.env` 里没有 `API_TOKEN`，所以 `loadConfig` 返回 `undefined`。
- **Bad:** Kindly revert regarding the token.

### `santai` (casual)

- **Good:** `.env` 里没配 `API_TOKEN`，跑一下 `npm test -- config`。
- **Bad:** 网络用语堆砌或 fake 梗.

## What casual is not

- Not a slang quota
- Not a license to drop grammar in incident or email text
- Speech levels (if any) are separate from `santai`
