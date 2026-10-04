# tokyo — Tokyo / Standard Japanese

**Type:** `regional` | **Status:** `validated`

## When to load

`language: japanese` + `regional_voice: tokyo` (or `netral` default for regional). Hyōjungo baseline for national media and most workplaces.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `です／ます` | Polite work default; statement + soft close | `tipis+` |
| `だ／である` | Plain explanatory prose in technical docs when register is santai | `sedang+` |
| `〜んです` | Explains cause gently in spoken-style explanation | `sedang+` |
| `〜と思います` | Modest technical claim; caps overconfidence | `tipis+` |

## Examples (bug explanation)

- `API_TOKEN` が `.env` にないので、`loadConfig` が `undefined` を返しています。`npm test -- config` を試してください。
- 設定ファイルにトークンが入っていないのが原因だと思います。

## Caps

- Default regional overlay — do not mix 関西弁 markers in the same sentence unless user asked.
- Keigo depth stays in `speech-levels.md`, not this overlay.
- No anime catchphrases or mascot slang.

## What NOT to mix

- 関西の やねん／へん／あかん in Tokyo-standard output.

## Forbidden caricature

- 関西の やねん／へん／あかん in Tokyo-standard output.
