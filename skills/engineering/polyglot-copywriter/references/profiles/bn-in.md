# bn-in profile (summary)

**Language:** `bengali` · **Overlay id:** `bn-in`

Full rules: [languages/bengali/overlays/bn-in.md](../languages/bengali/overlays/bn-in.md).

Bengali overlay — load when `regional_voice: bn-in` or user names this region/variety.

**When to load:** `language: bengali` + `regional_voice: bn-in`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/bengali.md](../techniques/locales/bengali.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
