# si-standard profile (summary)

**Language:** `sinhala` · **Overlay id:** `si-standard`

Full rules: [languages/sinhala/overlays/si-standard.md](../languages/sinhala/overlays/si-standard.md).

Sinhala overlay — load when `regional_voice: si-standard` or user names this region/variety.

**When to load:** `language: sinhala` + `regional_voice: si-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/sinhala.md](../techniques/locales/sinhala.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
