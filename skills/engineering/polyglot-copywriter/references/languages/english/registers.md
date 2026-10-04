# English registers

| Register | Config key | When |
|---|---|---|
| Formal / careful | `baku` | Legal, investor, complete sentences — on request |
| Work | `profesional` | Email, docs, LinkedIn — on request |
| Casual | `santai` | **Default**: chat, explanations, MR review |

## Pronouns

- `I` / `we` for ownership and coordination (the author fingerprint when active).
- `you` for the reader. External email uses their name, not honorifics.

## Examples

### `baku` (formal)

- **Good:** The service will be unavailable on Tuesday for scheduled maintenance.
- **Bad:** Hey team, we're gonna take the thing down Tuesday lol.

### `profesional` (work)

- **Good:** `API_TOKEN` is missing from `.env`, so `loadConfig` returns `undefined`. Run `npm test -- config`.
- **Bad:** Kindly revert regarding the aforementioned token configuration issue.

### `santai` (casual)

- **Good:** `API_TOKEN` isn't in `.env` — try `npm test -- config`.
- **Bad:** Valley-girl filler or `lah` on every line without Singlish overlay.

## What casual is not

- Not `kindly`, `please revert`, `circle back`, `leverage`, `utilize`
- Not valley-girl, Cockney, or phonetic accent spelling
- Not a particle quota (`lah` on every line)

## Simple prose default

Every register uses [simple-prose.md](../../simple-prose.md): common words, short active sentences, one idea per line. `baku` and `profesional` change **formality**, not vocabulary difficulty — no rare words or nested grammar for show.
