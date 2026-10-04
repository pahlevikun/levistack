# it-ch — Swiss Italian (light)

**Type:** `regional` | **Status:** `validated`

## When to load

`language: italian` + `regional_voice: it-ch`. Swiss Italian — **light** overlay; standard grammar with occasional Swiss lexicon.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `Lei` | Formal work default | `tipis+` |
| Swiss lexicon | `billette` (ticket), `colazione` context — only when natural | `tipis` |
| `per favore` | Softener | `tipis+` |

## Examples (bug explanation)

- `API_TOKEN` manca nel file `.env`, quindi `loadConfig` restituisce `undefined`. Eseguire `npm test -- config`.

## Caps

- **Light** — do not force Helveticisms every sentence.
- Not German or French code-switch unless user asked.

## What NOT to mix

- Full it-it Roman slang or it-it-only idioms that clash with Swiss context.

## Forbidden caricature

- Forcing Swiss German words into Italian prose.
