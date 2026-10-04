# ro-standard profile (summary)

**Language:** `romanian` · **Overlay id:** `ro-standard`

Full rules: [languages/romanian/overlays/ro-standard.md](../languages/romanian/overlays/ro-standard.md).

Romanian overlay — load when `regional_voice: ro-standard` or user names this region/variety.

**When to load:** `language: romanian` + `regional_voice: ro-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/romanian.md](../techniques/locales/romanian.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
