# japanese registers

Three registers. Default is `santai`. Casual is **not** automatically slang.

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Official, legal, academic — on request |
| Work | `profesional` | Email, docs, explanations — default for tech |
| Casual | `santai` | Chat, peer tone — on request |

## Pronouns and address

私/僕 (context); あなた sparingly — name + さん in work.

## Examples

### `baku` (formal)

- **Good:** 火曜日のメンテナンスのため、サービスを停止します。
- **Bad:** Service will be down Tuesday — English SVO.

### `profesional` (work)

- **Good:** `.env` に `API_TOKEN` がないため、`loadConfig` は `undefined` を返します。
- **Bad:** Kindly revert.

### `santai` (casual)

- **Good:** `.env` に `API_TOKEN` ないから、`npm test -- config` 走らせて。
- **Bad:** Invented keigo chain without examples.

## What casual is not

- Not a slang quota
- Not a license to drop grammar in incident or email text
- Speech levels (if any) are separate from `santai`
