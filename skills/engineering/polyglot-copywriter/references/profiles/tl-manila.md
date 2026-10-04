# tl-manila profile (summary)

**Language:** `tagalog` · **Overlay id:** `tl-manila`

Full rules: [languages/tagalog/overlays/tl-manila.md](../languages/tagalog/overlays/tl-manila.md).

Tagalog overlay — load when `regional_voice: tl-manila` or user names this region/variety.

**When to load:** `language: tagalog` + `regional_voice: tl-manila`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/tagalog.md](../techniques/locales/tagalog.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
