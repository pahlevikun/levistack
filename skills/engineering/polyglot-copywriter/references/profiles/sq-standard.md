# sq-standard profile (summary)

**Language:** `albanian` · **Overlay id:** `sq-standard`

Full rules: [languages/albanian/overlays/sq-standard.md](../languages/albanian/overlays/sq-standard.md).

Albanian overlay — load when `regional_voice: sq-standard` or user names this region/variety.

**When to load:** `language: albanian` + `regional_voice: sq-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/albanian.md](../techniques/locales/albanian.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
