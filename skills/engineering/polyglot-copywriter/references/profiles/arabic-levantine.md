# arabic-levantine profile (summary)

**Language:** `arabic` · **Overlay id:** `arabic-levantine`

Full rules: [languages/arabic/overlays/arabic-levantine.md](../languages/arabic/overlays/arabic-levantine.md).

Arabic overlay — load when `regional_voice: arabic-levantine` or user names this region/variety.

**When to load:** `language: arabic` + `regional_voice: arabic-levantine`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/arabic.md](../techniques/locales/arabic.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
