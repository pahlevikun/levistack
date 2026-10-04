# ha-nigeria profile (summary)

**Language:** `hausa` · **Overlay id:** `ha-nigeria`

Full rules: [languages/hausa/overlays/ha-nigeria.md](../languages/hausa/overlays/ha-nigeria.md).

Hausa overlay — load when `regional_voice: ha-nigeria` or user names this region/variety.

**When to load:** `language: hausa` + `regional_voice: ha-nigeria`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/hausa.md](../techniques/locales/hausa.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
