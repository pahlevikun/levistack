# fa-standard profile (summary)

**Language:** `persian` · **Overlay id:** `fa-standard`

Full rules: [languages/persian/overlays/fa-standard.md](../languages/persian/overlays/fa-standard.md).

Persian overlay — load when `regional_voice: fa-standard` or user names this region/variety.

**When to load:** `language: persian` + `regional_voice: fa-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/persian.md](../techniques/locales/persian.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
