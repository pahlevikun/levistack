# Incident communications techniques

Load when use case is **`incident`**, or user asks for outage update, status page, SEV comms. All languages.

## Sentence 1 job

**Severity + user impact + current state** — not apology-first, not "we are investigating" without scope.

## Section order

1. **Impact and scope** — what broke, who is affected, since when
2. **Current status / mitigation** — what was done, what is still broken
3. **Next update** — time or "next update in ~30 min"
4. **Workaround** — if any; else omit

Structure aligns with [usecases/incident/pack.md](../usecases/incident/pack.md).

## Register

Default `profesional`. `santai` must not hide severity or soften data-loss warnings. No marketing tone, no poetic metaphor on outages.

## Cross-language rules

- Numbers and timestamps from user only — do not invent error rates
- Product/service names exact
- Separate fact vs hypothesis ("likely cache" vs "confirmed cache")
- Status vocabulary consistent: Investigating → Identified → Monitoring → Resolved

## Locale routing

| Language | Locale file |
|---|---|
| japanese | [locales/japanese.md](locales/japanese.md) § Incident |
| indonesia | [locales/indonesia.md](locales/indonesia.md) § Incident |
| mandarin | [locales/mandarin.md](locales/mandarin.md) § Incident |
| korean | [locales/korean.md](locales/korean.md) § Incident |
| vietnamese | [locales/vietnamese.md](locales/vietnamese.md) § Incident |
| spanish | [locales/spanish.md](locales/spanish.md) § Incident |

## Good vs bad

| Bad | Good |
|---|---|
| We apologize for any inconvenience. Our team is working hard. | Checkout timeouts affected ~3% of sessions for 20 min; rollback at 14:32 UTC restored normal error rates. Next update 15:00 UTC. |
| Everything is fine now! | Error rate back to baseline since 14:32 UTC; we are monitoring for 1 hour. |

## Related

- [natural-writing.md](natural-writing.md) — plain words under stress
- [noslop-prose.md](../noslop-prose.md) — no hollow reassurance clusters
