# bg-standard profile (summary)

**Language:** `bulgarian` · **Overlay id:** `bg-standard`

Full rules: [languages/bulgarian/overlays/bg-standard.md](../languages/bulgarian/overlays/bg-standard.md).

Bulgarian overlay — load when `regional_voice: bg-standard` or user names this region/variety.

**When to load:** `language: bulgarian` + `regional_voice: bg-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/bulgarian.md](../techniques/locales/bulgarian.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
