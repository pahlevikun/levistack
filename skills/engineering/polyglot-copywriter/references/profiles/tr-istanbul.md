# tr-istanbul profile (summary)

**Language:** `turkish` · **Overlay id:** `tr-istanbul`

Full rules: [languages/turkish/overlays/tr-istanbul.md](../languages/turkish/overlays/tr-istanbul.md).

Turkish overlay — load when `regional_voice: tr-istanbul` or user names this region/variety.

**When to load:** `language: turkish` + `regional_voice: tr-istanbul`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/turkish.md](../techniques/locales/turkish.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
