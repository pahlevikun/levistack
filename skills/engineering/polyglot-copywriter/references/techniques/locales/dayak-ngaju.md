# Dayak Ngaju locale techniques

Load when **`language` is `dayak-ngaju`**. Base: [languages/dayak-ngaju/pack.md](../../languages/dayak-ngaju/pack.md), [culture.md](../../languages/dayak-ngaju/culture.md). Overlays under [languages/dayak-ngaju/overlays/](../../languages/dayak-ngaju/overlays/).

**Transcreation** — Limited coverage — follow pack honesty; no invented Ngaju forms.

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
