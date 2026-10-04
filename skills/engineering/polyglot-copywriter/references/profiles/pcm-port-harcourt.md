# pcm-port-harcourt profile (summary)

**Language:** `pcm` · **Overlay id:** `pcm-port-harcourt`

Full rules: [languages/pcm/overlays/pcm-port-harcourt.md](../languages/pcm/overlays/pcm-port-harcourt.md).

Nigerian Pidgin overlay — load when `regional_voice: pcm-port-harcourt` or user names this region/variety.

**When to load:** `language: pcm` + `regional_voice: pcm-port-harcourt`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/pcm.md](../techniques/locales/pcm.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
