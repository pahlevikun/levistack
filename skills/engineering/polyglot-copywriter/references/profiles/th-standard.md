# th-standard profile (summary)

**Language:** `thai` · **Overlay id:** `th-standard`

Full rules: [languages/thai/overlays/th-standard.md](../languages/thai/overlays/th-standard.md).

Thai overlay — load when `regional_voice: th-standard` or user names this region/variety.

**When to load:** `language: thai` + `regional_voice: th-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/thai.md](../techniques/locales/thai.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
