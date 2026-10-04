# ps-standard profile (summary)

**Language:** `pashto` · **Overlay id:** `ps-standard`

Full rules: [languages/pashto/overlays/ps-standard.md](../languages/pashto/overlays/ps-standard.md).

Pashto overlay — load when `regional_voice: ps-standard` or user names this region/variety.

**When to load:** `language: pashto` + `regional_voice: ps-standard`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/pashto.md](../techniques/locales/pashto.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
