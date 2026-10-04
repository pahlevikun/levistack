# lv-standard profile (summary)

**Language:** `latvian` · **Overlay id:** `lv-standard`

Full rules: [languages/latvian/overlays/lv-standard.md](../languages/latvian/overlays/lv-standard.md).

Latvian overlay — load when `regional_voice: lv-standard` or user names this region/variety.

**When to load:** `language: latvian` + `regional_voice: lv-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/latvian.md](../techniques/locales/latvian.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
