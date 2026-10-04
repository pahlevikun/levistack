# mr-mumbai profile (summary)

**Language:** `marathi` · **Overlay id:** `mr-mumbai`

Full rules: [languages/marathi/overlays/mr-mumbai.md](../languages/marathi/overlays/mr-mumbai.md).

Marathi overlay — load when `regional_voice: mr-mumbai` or user names this region/variety.

**When to load:** `language: marathi` + `regional_voice: mr-mumbai`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/marathi.md](../techniques/locales/marathi.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
