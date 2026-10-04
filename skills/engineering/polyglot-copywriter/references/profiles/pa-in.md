# pa-in profile (summary)

**Language:** `punjabi` · **Overlay id:** `pa-in`

Full rules: [languages/punjabi/overlays/pa-in.md](../languages/punjabi/overlays/pa-in.md).

Punjabi overlay — load when `regional_voice: pa-in` or user names this region/variety.

**When to load:** `language: punjabi` + `regional_voice: pa-in`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/punjabi.md](../techniques/locales/punjabi.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
