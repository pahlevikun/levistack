# bali-urban profile (summary)

**Language:** `bali` · **Overlay id:** `bali-urban`

Full rules: [languages/bali/overlays/bali-urban.md](../languages/bali/overlays/bali-urban.md).

Balinese overlay — load when `regional_voice: bali-urban` or user names this region/variety.

**When to load:** `language: bali` + `regional_voice: bali-urban`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/bali.md](../techniques/locales/bali.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
