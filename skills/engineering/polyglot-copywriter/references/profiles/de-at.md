# de-at profile (summary)

**Language:** `german` · **Overlay id:** `de-at`

Full rules: [languages/german/overlays/de-at.md](../languages/german/overlays/de-at.md).

German overlay — load when `regional_voice: de-at` or user names this region/variety.

**When to load:** `language: german` + `regional_voice: de-at`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/german.md](../techniques/locales/german.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
