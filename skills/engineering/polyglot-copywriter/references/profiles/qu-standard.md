# qu-standard profile (summary)

**Language:** `quechua` · **Overlay id:** `qu-standard`

Full rules: [languages/quechua/overlays/qu-standard.md](../languages/quechua/overlays/qu-standard.md).

Quechua overlay — load when `regional_voice: qu-standard` or user names this region/variety.

**When to load:** `language: quechua` + `regional_voice: qu-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/quechua.md](../techniques/locales/quechua.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
