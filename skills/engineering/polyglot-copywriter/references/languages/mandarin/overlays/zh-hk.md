# zh-hk — Hong Kong Mandarin (written)

**Type:** `regional` | **Status:** `validated`

## When to load

`language: mandarin` + `regional_voice: zh-hk`. Mandarin for HK readers — **Cantonese is a separate language**.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `HK lexical choices in Mandarin` | 程序、软件 — HK preference in Mandarin prose | `tipis+` |
| `请／麻烦` | Polite request framing common in HK service tone | `tipis+` |

## Examples (bug explanation)

- `.env` 缺少 `API_TOKEN`，`loadConfig` 因此返回 `undefined`。麻烦先执行 `npm test -- config`。

## Caps

- This is Mandarin for HK context, not Cantonese.
- If user wants Cantonese, say it is not in registry as `mandarin`.

## What NOT to mix

- Cantonese characters/grammar presented as Mandarin.

## Forbidden caricature

- Cantonese characters/grammar presented as Mandarin.
