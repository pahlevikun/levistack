# Arabic locale techniques

Load when **`language` is `arabic`**. Base: [languages/arabic/pack.md](../../languages/arabic/pack.md), [culture.md](../../languages/arabic/culture.md). Overlays under [languages/arabic/overlays/](../../languages/arabic/overlays/).

**Transcreation** — Umbrella — route to dialect overlay or `arz` for Egyptian. Marketing/email/incident sections are light.

## Honesty (umbrella)

- `arabic` is umbrella — prefer `arz` for sustained Egyptian, or a named dialect overlay (Levantine, Gulf).
- Do not write textbook MSA-only unless user asked; do not invent dialect forms.
- Marketing/email/incident guidance here is **light** — defer to active overlay pack.


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
- Umbrella — route to dialect overlay or `arz` for Egyptian. Marketing/email/incident sections are light.

| Bad (calque) | Good |
|---|---|
| Leverage our innovative solution | Reduce weekly reporting from 4 hours to 15 minutes |

## Email / chat

- Line 1: answer or request — no warmup opener
- Match register to channel (chat may be shorter, still complete)

| Bad | Good |
|---|---|
| We wish to inform you that… | Attached is the revised quote — please confirm by Friday |

## Related

- [marketing-copy.md](../marketing-copy.md)
- [email-comms.md](../email-comms.md)
- [incident-comms.md](../incident-comms.md)
