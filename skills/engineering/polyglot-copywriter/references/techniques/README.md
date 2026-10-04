# Technique modules index

Modular method docs load **after** language pack, overlay, and use-case pack. They add structure and locale nuance — they do not replace language rules.

Machine index: [index.json](index.json) (validated by `scripts/validate_skill.py`). Schema: [schema/techniques.schema.json](../schema/techniques.schema.json).

## Load order (summary)

1. Language pack (`references/languages/<id>/pack.md`)
2. Overlay (if `regional_voice` set)
3. Use-case pack (`references/usecases/<id>/pack.md`)
4. Generic technique (use-case or always-on rewrite)
5. Locale technique (`locales/<id>.md` when language matches)
6. Humanize pass when applicable

Full routing: [core.md](../core.md) § Technique routing.

## Generic techniques (all languages)

| Module | Load when |
|---|---|
| [marketing-copy.md](marketing-copy.md) | Use case `marketing`, `ads`, `social` |
| [humanize-workflow.md](humanize-workflow.md) | Use case `humanize` or de-AI request |
| [flow-by-relation.md](flow-by-relation.md) | List-like sections, weak hinges, staccato contrast review |
| [natural-writing.md](natural-writing.md) | Any rewrite — calque, stiff prose |
| [translation-vs-voice.md](translation-vs-voice.md) | Translate/localize across languages |

## Generic use-case techniques

| Module | Load when |
|---|---|
| [email-comms.md](email-comms.md) | `email`, `letter`, `announcement` |
| [chat-comms.md](chat-comms.md) | `chat` |
| [incident-comms.md](incident-comms.md) | `incident`, outage/status |
| [academic-writing.md](academic-writing.md) | `academic` |
| [docs-prose.md](docs-prose.md) | `docs`, `technical-doc` |

## Locale techniques

**97 locale files** under `locales/` — one per registry language (fictional fixtures in [fictional-catalog.json](../fictional-catalog.json) have no locale file). Machine list: [index.json](index.json) `locales` array. Sample triggers: [core.md](../core.md) § Locale techniques.

New in this pass: `italian`, `tamil`, `punjabi`, `german`, `arabic` (umbrella, light), `arz`, `bengali`, `urdu`, `russian`, `turkish`, `malay`, `jawa`, `sunda`, `bali`, `swahili`, `hausa`, `pcm`, `marathi`, `telugu`, `minangkabau`, `makassar`, `dayak-ngaju`, `abui`, plus `english` register notes.

Stub: [jp-marketing.md](jp-marketing.md) → [locales/japanese.md#marketing](locales/japanese.md#marketing).

## Routing matrix (use case × locale)

| Use case | Generic technique | Also load locale file when… |
|---|---|---|
| marketing / ads / social | marketing-copy | `language` has a row in [index.json](index.json) `locales` and use case is listed there |
| email / letter / announcement | email-comms | same — see per-file § |
| chat | chat-comms | same |
| incident | incident-comms | same |
| docs / technical-doc | docs-prose | same |
| academic | academic-writing | same |
| humanize | humanize-workflow | optional locale for calque; flow-by-relation when list-like |
| review (development weak) | flow-by-relation | substance + review-prose |
| any rewrite | natural-writing | optional locale |

Indonesian the author voice: [core.md](../core.md) + [voice-fingerprint.md](../voice-fingerprint.md). `english` locale supplements overlay packs; the author fingerprint still applies to English by default.
