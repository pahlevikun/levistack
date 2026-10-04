# cs-standard profile (summary)

**Language:** `czech` · **Overlay id:** `cs-standard`

Full rules: [languages/czech/overlays/cs-standard.md](../languages/czech/overlays/cs-standard.md).

Czech overlay — load when `regional_voice: cs-standard` or user names this region/variety.

**When to load:** `language: czech` + `regional_voice: cs-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/czech.md](../techniques/locales/czech.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
