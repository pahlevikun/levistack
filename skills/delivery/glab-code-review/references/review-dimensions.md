# MR review dimensions

Use every section below during Phase 1 preview. Load project playbook checklists when they exist — they **extend** this list, not replace it.

Delegate heavy passes to subagents when available; the calling agent still owns the merged report.

| Dimension | Load | Subagent (optional) |
|-----------|------|---------------------|
| Security, auth, PII, secrets | `rules/core/pii-logging.md`, `agents/security-reviewer.md` | `security-reviewer` |
| Tests and coverage gaps | `agents/tdd-runner.md`, project TDD rules | `tdd-runner` |
| Silent failures, wiring, principles | `rules/core/engineering-principles.md`, `agents/reviewer.md` | `reviewer` |
| Backend/API slop | `rules/core/noslop.md`, `skills/engineering/super-noslop/SKILL.md` (+ `super-noslop-code` for comments) | noslop audit (after mode) |
| Review comment prose | `skills/engineering/polyglot-copywriter` use case `glab-code-review`, [simple-prose.md](../../../engineering/polyglot-copywriter/references/simple-prose.md) | STE-simple inline text |

## 1. Knowledge and context

- Run `context-harvester` (or search the project docs) for ADRs, incidents, runbooks and past review learnings for this repo and feature area.
- Read open MR discussions and CI — do not duplicate or contradict resolved threads without checking current code.
- Read **surrounding source**, not only the diff hunks.

## 2. Compatibility with existing code

This pass is mandatory. The MR must fit the repo as it exists today.

- **Callers and callees:** use `codebase-memory` (`search_graph`, `trace_path`) or repository search to find who calls changed symbols and what they assume.
- **Pattern match:** compare new code to sibling files in the same package (error handling, logging, DI, naming, test style).
- **Registration / wiring:** new routes, handlers, jobs, CLI commands, hooks, or providers must be registered where siblings are — flag compile-only additions that never run.
- **Contract consistency:** request/response shapes, status codes, error codes, pagination, and idempotency must match sibling endpoints.
- **Config and feature flags:** new keys follow existing config layout; flags default safely and both paths work when shipped.
- **Breaking changes:** explicit in MR description, versioned, or guarded — never silent semantic changes on stable identifiers.
- **Data migrations:** reversible when the repo requires it; indexes and locks follow production patterns documented in the project.

## 3. Security (`security-reviewer`)

- Trust boundaries: identity from validated session/token — not spoofable client headers alone.
- PII and secrets never in logs, errors, tests, or fixtures (`pii-logging`).
- Injection: parameterized queries, no shell concatenation, path traversal rejected, SSRF allowlists on server-side fetch.
- Authz on every mutating path; webhooks and async payloads validated before acting.
- Outbound clients: timeouts, TLS where expected, no stack traces to untrusted callers.
- Concurrency: bounded parallelism; cancellation propagated.

## 4. Correctness and API contracts

- Logic bugs, nil derefs, race conditions, off-by-one, wrong defaults.
- **Error envelope:** platform APIs return the repo's standard JSON envelope (success and error) — flag raw strings, bare `message: "Success"`, or missing `error.code` when siblings use typed errors.
- **Status codes:** match domain conventions; no `200` with empty body or noop handler.
- **Validation:** at the trust boundary; inner layers may assume invariants already enforced.
- **Idempotency:** retried writes safe (keys, upsert, outbox).
- **Fail closed:** ambiguous auth/validation rejects — never proceed on ambiguity.

## 5. Tests and coverage (`tdd-runner`)

- Every behaviour change has a test update or a documented reason why not.
- New branches, error paths, and edge cases have table-driven or focused tests — not only happy path.
- No weakened assertions, added skips, or fixture changes to make broken code pass.
- Run scoped tests when the branch is available; report command + exit status.
- Flag missing tests for: new public API, status/error code changes, concurrency, registration wiring.

## 6. Performance and operations

- N+1 queries, unbounded reads, missing pagination, hot-path allocations.
- Missing timeouts on I/O; fire-and-forget goroutines/workers without shutdown.
- Duplicate logging of the same failure at every layer.

## 7. Engineering principles (`engineering-principles`)

- KISS / YAGNI / DRY / SOLID — flag premature abstraction, god modules, utils dump, duplicated business rules.
- Deletion test: would removing this layer put behaviour in one obvious place?
- Comments explain *why*; names reveal intent.
- Dead code, commented experiments, and unused flags removed in the same change.

## 8. noslop (backend/API/message surface)

Run an **after** audit on the diff. Cite rule IDs (R-XX) for findings.

Priority slop signals for MR review:

| Signal | What to flag |
|--------|----------------|
| Generic errors | `An error occurred`, string-matched `err.Error()` |
| No envelope / fake success | `200` + empty body, success with no contract |
| Dead routes | Registered handler that noops |
| Tutorial layering | Extra service/repo layer for one query |
| Template OpenAPI | "Returns data", "Handles the request" |
| Fabricated metrics | SLA/uptime claims without source |
| Non-idempotent retry | Retry on charge/create without dedupe |

See `skills/engineering/super-noslop/references/core/slop-patterns.md` and `mandatory-rules.md` for the full R-01–R-38 list.

## 9. Documentation and MR hygiene

- User-facing behaviour changes reflected in README, CHANGELOG, OpenAPI, or curl examples when the repo requires it.
- MR description matches the diff (no 💥 without proof).
- Stale fixtures, test data, or comments referencing old error codes.

## 10. Output format (preview)

Present findings in a table:

```markdown
## MR review findings

| # | Sev | Dim | File:Line | Finding | Suggestion |
|---|-----|-----|-----------|---------|------------|
| 1 | 🔴 | security | handler/foo.go:42 | ... | ... |
```

**Severity:**

- 🔴 **Critical** — must fix before merge (security, broken contract, silent failure)
- 🟠 **High** — likely bug or serious convention break
- 🟡 **Medium** — should fix; reviewer would comment
- 🟢 **Low** — nitpick or optional improvement

**Dimensions** (Dim column): `compat`, `security`, `correctness`, `api`, `tests`, `perf`, `principles`, `noslop`, `docs`.

End preview with:

- Open threads summary (existing discussions)
- Verdict if submitted now: **approve** / **request changes** / **comment only**
- Draft-ready count: how many findings map to **inline** draft comments (with suggestions when possible)

Do **not** plan a long summary note for GitLab — carry detail in per-line drafts ([comment-body-format.md](comment-body-format.md)).

Then **stop and wait** for user selection.
