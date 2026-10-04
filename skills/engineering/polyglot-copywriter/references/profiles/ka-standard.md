# ka-standard profile (summary)

**Language:** `georgian` · **Overlay id:** `ka-standard`

Full rules: [languages/georgian/overlays/ka-standard.md](../languages/georgian/overlays/ka-standard.md).

Georgian overlay — load when `regional_voice: ka-standard` or user names this region/variety.

**When to load:** `language: georgian` + `regional_voice: ka-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/georgian.md](../techniques/locales/georgian.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
