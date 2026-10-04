# am-standard profile (summary)

**Language:** `amharic` · **Overlay id:** `am-standard`

Full rules: [languages/amharic/overlays/am-standard.md](../languages/amharic/overlays/am-standard.md).

Amharic overlay — load when `regional_voice: am-standard` or user names this region/variety.

**When to load:** `language: amharic` + `regional_voice: am-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/amharic.md](../techniques/locales/amharic.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
