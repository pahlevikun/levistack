# ur-in profile (summary)

**Language:** `urdu` · **Overlay id:** `ur-in`

Full rules: [languages/urdu/overlays/ur-in.md](../languages/urdu/overlays/ur-in.md).

Urdu overlay — load when `regional_voice: ur-in` or user names this region/variety.

**When to load:** `language: urdu` + `regional_voice: ur-in`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/urdu.md](../techniques/locales/urdu.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
