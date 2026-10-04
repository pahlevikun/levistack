# gu-standard profile (summary)

**Language:** `gujarati` · **Overlay id:** `gu-standard`

Full rules: [languages/gujarati/overlays/gu-standard.md](../languages/gujarati/overlays/gu-standard.md).

Gujarati overlay — load when `regional_voice: gu-standard` or user names this region/variety.

**When to load:** `language: gujarati` + `regional_voice: gu-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/gujarati.md](../techniques/locales/gujarati.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
