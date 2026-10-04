# mks-urban profile (summary)

**Language:** `makassar` · **Overlay id:** `mks-urban`

Full rules: [languages/makassar/overlays/mks-urban.md](../languages/makassar/overlays/mks-urban.md).

Makassar overlay — load when `regional_voice: mks-urban` or user names this region/variety.

**When to load:** `language: makassar` + `regional_voice: mks-urban`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/makassar.md](../techniques/locales/makassar.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
