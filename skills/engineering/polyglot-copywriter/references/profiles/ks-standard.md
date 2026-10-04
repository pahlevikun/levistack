# ks-standard profile (summary)

**Language:** `kashmiri` · **Overlay id:** `ks-standard`

Full rules: [languages/kashmiri/overlays/ks-standard.md](../languages/kashmiri/overlays/ks-standard.md).

Kashmiri overlay — load when `regional_voice: ks-standard` or user names this region/variety.

**When to load:** `language: kashmiri` + `regional_voice: ks-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/kashmiri.md](../techniques/locales/kashmiri.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
