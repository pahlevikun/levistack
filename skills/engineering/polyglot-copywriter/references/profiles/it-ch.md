# it-ch profile (summary)

**Language:** `italian` · **Overlay id:** `it-ch`

Full rules: [languages/italian/overlays/it-ch.md](../languages/italian/overlays/it-ch.md).

Italian overlay — load when `regional_voice: it-ch` or user names this region/variety.

**When to load:** `language: italian` + `regional_voice: it-ch`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Load when `regional_voice` matches this overlay id.
- Default register: `profesional` for work email; `santai` for chat unless user says otherwise.
- One overlay at a time — no dialect soup.
- Lead with impact; protected code/paths stay literal.
- Follow overlay caps — light regional colour, not caricature.

**Locale techniques:** [locales/italian.md](../techniques/locales/italian.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
