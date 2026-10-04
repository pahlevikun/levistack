# Domain: backend

Handlers, application services, repositories, outbound clients, background workers, and package-level wiring.

## Checklist (add to core delivery gate)

- [ ] Layer count matches sibling modules — no Controller→Service→Repo for one query without reason (R-01, R-31).
- [ ] No `Manager` / `Helper` / `Util` catch-alls; names state the job (R-04).
- [ ] Interfaces have a second consumer or a documented seam — not single-impl cleanliness (R-10).
- [ ] Pass-through wrappers and decorative middleware removed or justified (R-07, R-08).
- [ ] Retry/circuit breaker names a trigger and idempotency story (R-13, R-19, R-32).
- [ ] Jobs and workers: bounded concurrency, shutdown, cancellation propagated (R-27).
- [ ] No mock/in-memory client on production path unless behind a flag (R-22).
- [ ] Errors use repo envelope/types — not raw strings or `err.Error()` matching (R-02, patterns in [slop-patterns.md](../core/slop-patterns.md)).

## MR review signals

Tutorial layering, god service, utils dump, dead registered handlers, silent stubs — see [glab-code-review §8](../../../../delivery/glab-code-review/references/review-dimensions.md).
