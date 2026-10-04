# Tamil locale techniques

Load when **`language` is `tamil`**. Base: [languages/tamil/pack.md](../../languages/tamil/pack.md), [culture.md](../../languages/tamil/culture.md). Overlays under [languages/tamil/overlays/](../../languages/tamil/overlays/).

**Transcreation** — Transcreation — adapt for region and register, not translate-then-polish.

## Register defaults by use case

| Use case | Default register | Notes |
|---|---|---|
| marketing | `profesional` | Benefit-first; match overlay lexicon |
| email | `profesional` | Complete sentences |
| chat | `santai` | Shorter OK; still grammatical |
| incident | `profesional` | Impact first |

Set `regional_voice` from user region name. One overlay at a time.

## Marketing

- Headline: concrete benefit + proof if available
- One primary CTA; no fabricated stats
- Transcreation — adapt for region and register, not translate-then-polish.

| Bad (calque) | Good |
|---|---|
| Leverage our innovative solution | Concrete benefit + proof when available |

## Email / chat

- Line 1: answer or request — no warmup opener
- Match register to channel (chat may be shorter, still complete)

| Bad | Good |
|---|---|
| We wish to inform you that… | Line 1 = answer or request |

## Incident

- Sentence 1: impact + current status
- Next update time when known
- No marketing tone

| Bad | Good |
|---|---|
| We apologize for any inconvenience | Impact + current status in sentence 1 |

## Docs

- Procedure steps as numbered list when helpful
- Keep technical terms repo-natural
- Complete sentences in `profesional` register

## Academic

- `baku` register; hedging where evidence requires
- No marketing adjectives in critique sections

## Related

- [marketing-copy.md](../marketing-copy.md)
- [email-comms.md](../email-comms.md)
- [incident-comms.md](../incident-comms.md)
