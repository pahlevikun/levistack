# as-standard profile (summary)

**Language:** `assamese` · **Overlay id:** `as-standard`

Full rules: [languages/assamese/overlays/as-standard.md](../languages/assamese/overlays/as-standard.md).

Assamese overlay — load when `regional_voice: as-standard` or user names this region/variety.

**When to load:** `language: assamese` + `regional_voice: as-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/assamese.md](../techniques/locales/assamese.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
