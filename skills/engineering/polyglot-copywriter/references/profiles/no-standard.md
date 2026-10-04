# no-standard profile (summary)

**Language:** `norwegian` · **Overlay id:** `no-standard`

Full rules: [languages/norwegian/overlays/no-standard.md](../languages/norwegian/overlays/no-standard.md).

Norwegian overlay — load when `regional_voice: no-standard` or user names this region/variety.

**When to load:** `language: norwegian` + `regional_voice: no-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/norwegian.md](../techniques/locales/norwegian.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
