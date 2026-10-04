# kk-standard profile (summary)

**Language:** `kazakh` · **Overlay id:** `kk-standard`

Full rules: [languages/kazakh/overlays/kk-standard.md](../languages/kazakh/overlays/kk-standard.md).

Kazakh overlay — load when `regional_voice: kk-standard` or user names this region/variety.

**When to load:** `language: kazakh` + `regional_voice: kk-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/kazakh.md](../techniques/locales/kazakh.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
