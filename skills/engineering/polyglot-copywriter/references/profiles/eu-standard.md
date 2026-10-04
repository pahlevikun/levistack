# eu-standard profile (summary)

**Language:** `basque` · **Overlay id:** `eu-standard`

Full rules: [languages/basque/overlays/eu-standard.md](../languages/basque/overlays/eu-standard.md).

Basque overlay — load when `regional_voice: eu-standard` or user names this region/variety.

**When to load:** `language: basque` + `regional_voice: eu-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/basque.md](../techniques/locales/basque.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
