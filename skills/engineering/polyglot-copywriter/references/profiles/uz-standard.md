# uz-standard profile (summary)

**Language:** `uzbek` · **Overlay id:** `uz-standard`

Full rules: [languages/uzbek/overlays/uz-standard.md](../languages/uzbek/overlays/uz-standard.md).

Uzbek overlay — load when `regional_voice: uz-standard` or user names this region/variety.

**When to load:** `language: uzbek` + `regional_voice: uz-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/uzbek.md](../techniques/locales/uzbek.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
