# sk-standard profile (summary)

**Language:** `slovak` · **Overlay id:** `sk-standard`

Full rules: [languages/slovak/overlays/sk-standard.md](../languages/slovak/overlays/sk-standard.md).

Slovak overlay — load when `regional_voice: sk-standard` or user names this region/variety.

**When to load:** `language: slovak` + `regional_voice: sk-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/slovak.md](../techniques/locales/slovak.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
