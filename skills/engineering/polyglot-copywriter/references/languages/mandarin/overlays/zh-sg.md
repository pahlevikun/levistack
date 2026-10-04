# zh-sg — Singapore Mandarin

**Type:** `regional` | **Status:** `validated`

## When to load

`language: mandarin` + `regional_voice: zh-sg`. Singapore Mandarin with local lexical choices.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `Simplified + SG lexicon` | 软件、视频、程序 — SG usage | `tipis+` |
| `吗 → 吗/呢` | Question particle as in local spoken Mandarin | `tipis+` |
| `先` | Do X first (spoken instruction ordering) | `tipis+` |

## Examples (bug explanation)

- `.env` 里没有 `API_TOKEN`，所以 `loadConfig` 返回 `undefined`。先跑 `npm test -- config` 试试。

## Caps

- Singlish particles (lah/leh) belong in `english/singlish` mix, not this overlay.

## What NOT to mix

- lah/leh in Mandarin sentences unless user asked Singlish mix.

## Forbidden caricature

- lah/leh in Mandarin sentences unless user asked Singlish mix.
