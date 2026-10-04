# Email communications techniques

Load when use case is **`email`**, **`letter`**, or **`announcement`**. Works with any language — apply structure here, phrasing from active **language pack** + **locale technique** if present.

## Structure (all languages)

1. **Subject / line 1** — answer, ask, or decision (not warmup)
2. **Need-to-know** — who, when, where, link (1–3 sentences max)
3. **Next step** — one action, owner, deadline if exists
4. **Stop** — no recap, no empty "let me know if you have questions"

Full layout patterns: [plain-comms.md](../usecases/plain-comms.md). Calque avoidance: [natural-writing.md](natural-writing.md).

## Register

Default `profesional` for email use case. `santai` only when user or thread tone is clearly casual. `baku` for formal letters on request.

## Cross-language rules

- Complete sentences — no telegram fragments in email body
- Protected artifacts (commands, paths, ticket IDs) unchanged
- Timezone on deadlines (`Fri 19 Sep, 14:00 WIB`)
- One thread = one primary ask

## Locale routing

After this file, load locale technique when `language` matches:

| Language | Locale file |
|---|---|
| japanese | [locales/japanese.md](locales/japanese.md) § Email / chat |
| indonesia | [locales/indonesia.md](locales/indonesia.md) § Email / chat |
| mandarin | [locales/mandarin.md](locales/mandarin.md) § Email / WeChat |
| korean | [locales/korean.md](locales/korean.md) § Email / chat |
| vietnamese | [locales/vietnamese.md](locales/vietnamese.md) § Email |
| spanish | [locales/spanish.md](locales/spanish.md) § Email |
| french | [locales/french.md](locales/french.md) § Email |
| portuguese | [locales/portuguese.md](locales/portuguese.md) § Email |
| hindi | [locales/hindi.md](locales/hindi.md) § Email |
| tagalog | [locales/tagalog.md](locales/tagalog.md) § Email |

English / Indonesian: [core.md](../core.md) + [voice-fingerprint.md](../voice-fingerprint.md) when the author voice.

## Good vs bad (pattern)

| Bad | Good |
|---|---|
| Warmup paragraph then the ask in paragraph 4 | Revised quote attached — please confirm by Friday |
| Kindly be informed that… | We shipped v2.3 today; breaking change is the auth header |

## Related

- [usecases/email/pack.md](../usecases/email/pack.md)
- [chat-comms.md](chat-comms.md) — when channel is Slack/Lark not email
