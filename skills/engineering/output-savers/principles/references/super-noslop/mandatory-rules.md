# Part 2: Mandatory rules (R-01 to R-38)

Scope: everything in the diff that is backend/API/config/message surface. Rule numbers are stable for audits and [`super-noslop-code`](comments.md) cross-refs.

## Group 1: Hard Gate (absolute)

### R-02 — Messages and copy

- **FORBIDDEN**: em dash (`—`) in user-facing API or CLI text
- **FORBIDDEN**: generic errors without stable code or field
- Use comma, period, colon, or parentheses; name the failure domain
- Carve-out: skill headings, pattern examples, `super-noslop-code` docs

### R-03 — Trust boundaries

- Validate untrusted input at the boundary that owns the outcome
- Size/time limits on reads, uploads, fan-out; no unbounded loops or N+1 without intent
- Fail closed on ambiguous auth or validation

### R-17 — Data and numbers

- **FORBIDDEN**: metrics, benchmarks, SLA figures without a real source

### R-18 — Example and seed data

- **FORBIDDEN**: realistic fabricated rows/IDs presented as production samples
- Fixtures labeled synthetic or obviously placeholder

### R-23 — Config and integrations

- Label placeholders before inventing hostnames, keys, queues, flags, external IDs
- Never commit plausible secrets or endpoints as if real

### R-24 — Routes and handlers

- **FORBIDDEN**: registered routes that noop or return success with no work
- Not implemented → `501` / typed error / flag off — not silent `200`

### R-25 — Fail closed

- Auth, authorization, validation ambiguity must reject
- **FORBIDDEN**: catch-and-return-empty-success

### R-26 — Stubs and placeholders

- No prod-path handler with empty `200`, enabled `TODO`, or default mock client
- Stubs behind flags, test packages, or dev-only wiring

### R-27 — Operational states

- Handle empty results, validation errors, timeouts, rate limits, partial failure

### R-28 — API descriptions

- No template OpenAPI strings; state behavior, constraints, error semantics — or stay minimal

### R-32 — Retries and writes

- Retried mutations idempotent or deduplicated
- **FORBIDDEN**: blind retry on non-idempotent writes without key/outbox

### R-33 — No patch scripts

- **FORBIDDEN**: sed/regex fix on deployed config/SQL outside normal source edit path

### R-34 — Feature flags and modes

- Shipped flag: both paths work, or defaults off with explicit guard

### R-35 — Verify before you deliver

- Run repo test/type/lint/build for this change **this turn**; report command + exit status

### R-36 — No fabricated claims

- No invented SOC 2, ISO, "10x faster", fake uptime in code/docs

### R-37 — Architecture direction required

- Read `AGENTS.md`, project docs and siblings before inventing layers
- Diverge only with *draft without repo pattern* label; name collisions with existing convention

### R-38 — Honest placeholders

- `[NOT IMPLEMENTED]`, `501`, typed errors, obvious fixture IDs — not production-shaped fakes

## Group 2: Purpose-Gate

Allowed with a **written reason**. FAIL as default without one.

### R-01 — Layers and abstractions

No default controller→service→repo for one query; no `BaseService` for one handler; no bus for one listener.

### R-04 — Names

No default `Manager` / `Helper` / `Util` / `Processor` / `DataService`. Use product vocabulary.

### R-06 — Types and DTOs

No `Data` / `Info` / `RequestDTO` for everything. Types name the contract.

### R-07 — Middleware stack

No copied auth+log+metrics+trace+cache chain on every route without need.

### R-08 — Pass-through wrappers

Delegate-only functions need a boundary job (auth, metrics, transaction).

### R-09 — Decorative annotations

No `@Transactional` / `@Retry` / `@Cacheable` / decorators on every method without a failure mode.

### R-10 — Interface with one implementation

Need second consumer, test double, or swap target — not cleanliness alone.

### R-12 — Logging

Meaningful transitions once at owning boundary — not every line, not duplicate per layer.

### R-13 — Resilience patterns

Retry/circuit/bulkhead need written trigger (upstream, latency, cost).

### R-14 — Handler shape

Not identical copy-paste CRUD everywhere; shared helpers OK when reason written.

### R-19 — Background work

Named trigger, idempotency story, failure visibility — not "add a cron" default.

### R-22 — Mocks in production path

No test doubles or in-memory stores in default DI.

## Group 3: Quality locks

### R-05 — Package layout

No tutorial tree when repo uses another layout; no god-service; no utils dump.

### R-11 — Error contract

Consistent typed/coded errors on the same surface — not string soup + `{ error: true }` mix.

### R-15 — Response messages

No default `Success` / `OK` / `Failed` / `Error`. Name outcome or field.

### R-16 — Buzzwords

No seamless, robust, enterprise-grade, cutting-edge, intelligent, next-generation in logs/docs.

### R-20 — Domain identity

Models, events, endpoints use this product's language — swap-company test.

### R-21 — Config profiles

Referenced dev/staging/prod paths exist or fail fast at startup.

### R-29 — Dependency budget

No new library for one function when repo already has a standard.

### R-30 — Do not clone

No wholesale tutorial/blog architecture unless repo already uses that shape.

### R-31 — Write the reason

One line per major decision (layer, type, retry, dependency, error shape). Keystone rule.
