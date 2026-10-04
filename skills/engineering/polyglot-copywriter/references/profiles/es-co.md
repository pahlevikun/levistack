# es-co profile (summary)

**Language:** `spanish` · **Overlay id:** `es-co`

Full rules: [languages/spanish/overlays/es-co.md](../languages/spanish/overlays/es-co.md).

Spanish overlay — load when `regional_voice: es-co` or user names this region/variety.

**When to load:** `language: spanish` + `regional_voice: es-co`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/spanish.md](../techniques/locales/spanish.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
