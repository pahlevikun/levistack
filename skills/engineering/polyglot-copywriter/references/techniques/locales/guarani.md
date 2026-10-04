# Guarani locale techniques

Load when **`language` is `guarani`**. Base: [languages/guarani/pack.md](../../languages/guarani/pack.md), [culture.md](../../languages/guarani/culture.md). Overlays under [languages/guarani/overlays/](../../languages/guarani/overlays/).

**Transcreation** — Limited coverage — ask regional variety; no invented dialect forms.

## Register defaults by use case

| Use case | Default register | Notes |
|---|---|---|
| marketing | `profesional` | Benefit-first; match overlay lexicon |
| email | `profesional` | Complete sentences |
| chat | `santai` | Shorter OK; still grammatical |
| incident | `profesional` | Impact first |

Set `regional_voice` from user region name. One overlay at a time.

## Email / chat

- Line 1: answer or request — no warmup opener
- Match register to channel (chat may be shorter, still complete)

| Bad | Good |
|---|---|
| We wish to inform you that… | Line 1 = answer or request |

## Docs

- Procedure steps as numbered list when helpful
- Keep technical terms repo-natural
- Complete sentences in `profesional` register

## Related

- [marketing-copy.md](../marketing-copy.md)
- [email-comms.md](../email-comms.md)
- [incident-comms.md](../incident-comms.md)
