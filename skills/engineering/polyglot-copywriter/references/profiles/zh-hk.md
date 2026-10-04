# zh-hk profile (summary)

**Language:** `mandarin` · **Overlay id:** `zh-hk`

Full rules: [languages/mandarin/overlays/zh-hk.md](../languages/mandarin/overlays/zh-hk.md).

Mandarin Chinese overlay — load when `regional_voice: zh-hk` or user names this region/variety.

**When to load:** `language: mandarin` + `regional_voice: zh-hk`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/mandarin.md](../techniques/locales/mandarin.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
