# Technical docs prose techniques

Load when use case is **`docs`**, **`technical-doc`**, or user asks for runbook, how-to, internal guide readability. All languages.

## Sentence 1 job

What this doc is for, or the most important fact.

## Section order

1. **Purpose / when to use**
2. **Steps or facts** — scannable headings, numbered procedures
3. **Troubleshooting / owners** — if known

Aligns with [usecases/docs/pack.md](../usecases/docs/pack.md) and [technical-doc/pack.md](../usecases/technical-doc/pack.md).

## Register

Default `profesional`. Commands, flags, paths, code fences are **protected** — style applies to surrounding prose only.

## Readability rules

- One idea per heading block
- Imperative steps: "Run …", "Check …" (localized via language pack)
- Warnings before destructive steps
- `technical_terms: repo-natural` — match repo vocabulary
- No marketing hooks in runbooks

## Locale routing

| Language | Locale file |
|---|---|
| japanese | [locales/japanese.md](locales/japanese.md) § Docs |
| indonesia | [locales/indonesia.md](locales/indonesia.md) § Docs |
| mandarin | [locales/mandarin.md](locales/mandarin.md) § Docs |

## Good vs bad

| Bad | Good |
|---|---|
| This comprehensive guide will walk you through leveraging our robust pipeline | Use this runbook when deploy fails after migration. Step 1: check `kubectl get pods -n prod`. |
| Utilize the aforementioned configuration | Edit `config.yaml` and set `replicas: 3`. |

## Related

- [natural-writing.md](natural-writing.md)
- [core.md](../core.md) § Protected artifacts
