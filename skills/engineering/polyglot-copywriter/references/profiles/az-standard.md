# az-standard profile (summary)

**Language:** `azerbaijani` · **Overlay id:** `az-standard`

Full rules: [languages/azerbaijani/overlays/az-standard.md](../languages/azerbaijani/overlays/az-standard.md).

Azerbaijani overlay — load when `regional_voice: az-standard` or user names this region/variety.

**When to load:** `language: azerbaijani` + `regional_voice: az-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/azerbaijani.md](../techniques/locales/azerbaijani.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
