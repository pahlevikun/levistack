# super-noslop (principles bridge)

Canonical router and domain checklists: [super-noslop/SKILL.md](../../../super-noslop/SKILL.md).

Apply when generating or editing handlers, services, clients, jobs, migrations, config, API messages, OpenAPI, or code comments. Code must **fit this repo's boundaries and vocabulary**, not a tutorial paste.

Ask the user (in their chat language) when super-noslop applies: **during** the work or **after**. **Auto mode:** during.

Rule: [`noslop.md`](../../../../../../rules/core/noslop.md). Gate order: [workflow-gates.md](workflow-gates.md).

## Intake — load by surface

| Task | Load |
|------|------|
| Backend / API / services | [surfaces.md](surfaces.md) + [slop-patterns.md](slop-patterns.md) + [mandatory-rules.md](mandatory-rules.md) + [delivery-gate.md](delivery-gate.md) |
| Code comments | Above **and** [`super-noslop-code`](comments.md) — comments only |
| Frontend / database / tests / infra | Canonical [domains index](../../../super-noslop/references/domains/README.md) + core pack files in this folder |
| User-facing CLI / API copy | [principles-and-cli-copy.md](principles-and-cli-copy.md) |
| After-mode audit file | [templates/audit-after-mode.md](templates/audit-after-mode.md) |
| First-run AGENTS.md pointer | [templates/agents-md-pointer.md](templates/agents-md-pointer.md) |

## What this is (and is not)

**Filter**, not a framework mandate. Does not require DDD or microservices unless the repo already uses them. Does not ban interfaces or retries — rejects **patterns without purpose**.

Every layer, type, and error shape must pass the purpose test (R-31). Details: [mandatory-rules.md](mandatory-rules.md).

## Two usage modes

1. **DURING** — apply [mandatory-rules.md](mandatory-rules.md) while coding; finish with [delivery-gate.md](delivery-gate.md).
2. **AFTER** — audit using [templates/audit-after-mode.md](templates/audit-after-mode.md).

## When invoked by glab-code-review

- **Scope:** MR review comment bodies and user-facing API/error copy in the diff — not executable code inside suggestion fences.
- **Mode:** **after** — audit draft comment text before posting GitLab draft notes.
- Pair with **polyglot-copywriter** (`glab-code-review` use case).

## Old skill name

| Old | Use |
|---|---|
| `noslop` | [super-noslop/SKILL.md](../../../super-noslop/SKILL.md) |
| `noslop-code` | [comments.md](comments.md) / `super-noslop-code` subskill |
