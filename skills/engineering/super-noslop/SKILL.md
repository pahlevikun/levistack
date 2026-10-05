---
name: super-noslop
description: "Super noslop: domain router for the no-slop filter on backend handlers, APIs, frontend UI, database access, infra/config, tests, and code comments. Stops tutorial layering, generic errors, OpenAPI filler, a11y/perf theater, N+1 queries, and AI comment noise. Pairs with glab-code-review (noslop dimension) and polyglot-copywriter for review/MR prose. Use when generating or auditing code that must fit this repo—not a paste. Subskill super-noslop-code is comments-only. Default mode: during; after mode for audits."
metadata:
  version: "2.0.0"
---

# Super noslop

> No Slop: tight, intentional code and messages for AI-assisted work

Apply when generating or editing executable code, API/CLI copy, OpenAPI, config, migrations, or comments. Code must **fit this repo's boundaries and vocabulary**, not a tutorial paste.

Ask the user (in their chat language) when super-noslop applies: **during** the work or **after**. **Auto mode:** during.

Rule: [`noslop.md`](../../../rules/core/noslop.md). Gate order: [workflow-gates.md](references/core/workflow-gates.md).

## Step 0: detect the domain

Do this first; load only what the task needs. Index: [references/domains/README.md](references/domains/README.md).

| If the diff or task touches… | Domain | Load |
|---|---|---|
| Handlers, services, workers, jobs, domain logic | **backend** | [backend.md](references/domains/backend.md) + core pack below |
| HTTP routes, status codes, envelopes, OpenAPI, webhooks | **api** | [api.md](references/domains/api.md) + core pack |
| SQL, ORM, migrations, indexes, transactions | **database** | [database.md](references/domains/database.md) + core pack |
| Components, CSS, layout, client state, a11y | **frontend** | [frontend.md](references/domains/frontend.md) + core pack |
| Env, feature flags, IaC snippets, deploy config in diff | **infra-config** | [infra-config.md](references/domains/infra-config.md) + core pack |
| Test files, fixtures, mocks, assertions | **tests** | [tests.md](references/domains/tests.md) + core pack |
| README/CHANGELOG-only or pure docs with no code surface | **docs** | [docs-exclusions.md](references/domains/docs-exclusions.md) — prose skills instead |
| Code comments only (no logic edits) | **comments** | Core delivery gate + [`super-noslop-code`](skills/super-noslop-code/SKILL.md) |

**Core pack** (all executable domains): [slop-patterns.md](references/core/slop-patterns.md) + [mandatory-rules.md](references/core/mandatory-rules.md) + [delivery-gate.md](references/core/delivery-gate.md). User-facing CLI/API copy: add [principles-and-cli-copy.md](references/core/principles-and-cli-copy.md).

## Package layout

```
super-noslop/
├── SKILL.md                      # router (this file)
├── references/
│   ├── core/                     # R-01–R-38, gates, patterns, workflow
│   └── domains/                  # per-layer checklists
├── templates/                    # architecture read, audit, AGENTS pointer
└── skills/
    └── super-noslop-code/        # comment hygiene; never touches executable code
```

## What this is (and is not)

**Filter**, not a framework mandate.

- Does **not** require DDD, microservices, or Clean Architecture unless the repo already uses them.
- Does **not** ban interfaces, middleware, or retries — rejects **patterns without purpose**.
- Does **not** replace **polyglot-copywriter** for human-facing prose (MR bodies, essays).

Every layer, type, and error shape must pass the purpose test (R-31). Details: [mandatory-rules.md](references/core/mandatory-rules.md).

## Core principle

Before adding a file, layer, or dependency: **what does this serve?** If the answer is "every tutorial does this" or "it's best practice", rework.

> **Swap-company test:** if the product name changed, would this module still belong in *this* codebase?

**Done** when: rules pass; edge paths are real; R-35 verify evidence exists in the current turn (a command run this turn, not memory).

## Craftsmanship standard

| Id | Standard |
|----|----------|
| C-1 | Intentionality — "AI default" is a red flag |
| C-2 | Functional completeness — real work or honest errors, no fake success |
| C-3 | Content-driven structure — modules exist for this product's flow |
| C-4 | Resilience — empty, validation, timeout, rate limit, upstream failure |
| C-5 | Evidence over claims — metrics and compliance real or omitted |

**Principles** (KISS/YAGNI/deletion test): [principles-and-cli-copy.md](references/core/principles-and-cli-copy.md).

## Two usage modes

> **When do you want to use super-noslop?**
> 1. **DURING** — apply [mandatory-rules.md](references/core/mandatory-rules.md) while coding; finish with [delivery-gate.md](references/core/delivery-gate.md).
> 2. **AFTER** — write audit using [templates/audit-after-mode.md](templates/audit-after-mode.md); user picks finding numbers to fix.

## Templates

| Task | Load |
|------|------|
| Architecture read (before backend code) | [templates/architecture-read.md](templates/architecture-read.md) |
| After-mode audit file | [templates/audit-after-mode.md](templates/audit-after-mode.md) |
| First-run AGENTS.md pointer | [templates/agents-md-pointer.md](templates/agents-md-pointer.md) |

## Before coding (backend-heavy work)

Fill [templates/architecture-read.md](templates/architecture-read.md) — required at delivery for handler/API/database changes.

## Delivery gate

Run [delivery-gate.md](references/core/delivery-gate.md) every pass on executable surfaces. **Comments only:** delivery gate + `super-noslop-code` checklist.

## When invoked by glab-code-review

- **Scope:** MR review comment bodies and user-facing API/error copy flagged in the diff — not executable code inside suggestion fences.
- **Mode:** **after** — audit draft comment text before posting GitLab draft notes.
- **Inline vs summary:** reject generic rollup blocks; each finding stays on its inline draft. See [`glab-code-review`](../../delivery/glab-code-review/SKILL.md).
- **Dimensions:** cite rule IDs (R-XX) in findings; Dim column stays `noslop`. Full MR signals: [review-dimensions.md](../../delivery/glab-code-review/references/review-dimensions.md) §8.
- Pair with **polyglot-copywriter** (`glab-code-review` use case) for STE-simple phrasing after slop removal.

## When invoked by write-mr-description

- **Scope:** MR description markdown — not commit subjects or code paths.
- **Mode:** **after** render from [TEMPLATE.md](../../delivery/write-mr-description/TEMPLATE.md); strip AI filler and unjustified breaking claims before opening the draft MR.

## Old skill name

| Old | Use |
|---|---|
| `noslop` | This skill (`super-noslop`) |
| `noslop-code` | [`super-noslop-code`](skills/super-noslop-code/SKILL.md) |

## Related skills

- `super-noslop-code`: edit comments only.
- `glab-code-review`: review a diff.
- `super-refactor`: fix slop in the structure.
- `polyglot-copywriter`: rewrite prose.
