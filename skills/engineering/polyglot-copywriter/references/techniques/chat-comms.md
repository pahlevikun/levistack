# Chat communications techniques

Load when use case is **`chat`**, or user mentions Slack, Lark, Teams, DM, standup thread. All languages.

## Sentence 1 job

Answer, ask, or status — reader should not scroll for the point.

## Shape

- **Short but complete** — real grammar; not email length, not telegram fragments
- **One ask per message** when possible
- **@name** when assigning; timezone on times
- Emoji: rare; never replace severity in incident threads

Aligns with [usecases/chat/pack.md](../usecases/chat/pack.md).

## Register

Default `santai` for chat use case. Upgrade to `profesional` for customer-facing channels or exec threads.

## Cross-language rules

- Code, ticket IDs, links unchanged
- Thread context: don't repeat entire email in chat
- If incident: load [incident-comms.md](incident-comms.md) — severity still first

## Locale routing

| Language | Locale file |
|---|---|
| japanese | [locales/japanese.md](locales/japanese.md) § Email / chat |
| indonesia | [locales/indonesia.md](locales/indonesia.md) § Email / chat |
| korean | [locales/korean.md](locales/korean.md) § Email / chat |
| mandarin | [locales/mandarin.md](locales/mandarin.md) § Email / WeChat |

English / Indonesian the author chat: [core.md](../core.md) + [voice-fingerprint.md](../voice-fingerprint.md).

## Good vs bad

| Bad | Good |
|---|---|
| Hi team! Hope everyone is doing well. Just wanted to circle back… | Standup moves to 10:00 WIB from Monday — same Zoom link. |
| Need review. Tomorrow. | Can you review PR #482 today? I want to merge tomorrow morning. |

## Related

- [email-comms.md](email-comms.md) — when promoting thread to email
- [natural-writing.md](natural-writing.md)
