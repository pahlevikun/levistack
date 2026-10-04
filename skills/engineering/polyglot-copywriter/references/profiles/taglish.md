# taglish profile (summary)

**Language:** `tagalog` · **Overlay id:** `taglish`

Full rules: [languages/tagalog/overlays/taglish.md](../languages/tagalog/overlays/taglish.md).

Tagalog overlay — load when `regional_voice: taglish` or user names this region/variety.

**When to load:** `language: tagalog` + `regional_voice: taglish`.

**Register default:** `profesional` for email/docs/incident; `santai` for chat unless user overrides.

**Voice / grammar:**
- Mix overlay — load only when user explicitly asked.
- Cap loanwords; keep grammar of the primary language.
- No marker quota — pragmatic function over iconic vocabulary.
- Protected artifacts unchanged.

**Locale techniques:** [locales/tagalog.md](../techniques/locales/tagalog.md) when use case matches.

**Not:** Mixing another overlay's markers unless user asked for a named mix.

**Not:** Inventing forms outside the overlay pack (umbrella/limited packs — see pack honesty).
