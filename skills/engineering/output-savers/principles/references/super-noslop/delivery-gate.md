# Delivery gate (mandatory)

PASS/FAIL report with evidence. Any FAIL: fix, re-run, ship only when green.

**Comments only:** this gate plus [`super-noslop-code`](comments.md) checklist.

Pair with fresh command evidence from this turn and your end-of-work checklist's super-noslop item.

## Block 1: Hard Gate (all must be **no**)

- [ ] Em dash or generic user-facing error without code/field? *(R-02)*
- [ ] Missing validation, limits, or fail-open auth/validation? *(R-03, R-25)*
- [ ] Metrics/benchmarks without source? *(R-17)*
- [ ] Fabricated fixtures as production? *(R-18)*
- [ ] Invented config/secrets/endpoints unlabeled? *(R-23)*
- [ ] Dead routes, noop handlers, silent stubs? *(R-24, R-26)*
- [ ] Missing empty/error/timeout/rate-limit handling? *(R-27)*
- [ ] Template OpenAPI/doc strings? *(R-28)*
- [ ] Non-idempotent retries on writes? *(R-32)*
- [ ] Patch-script fix instead of source? *(R-33)*
- [ ] Shipped flag with broken path? *(R-34)*
- [ ] No fresh verify command this turn? *(R-35)*
- [ ] Fabricated compliance/performance claims? *(R-36)*
- [ ] Ignored repo architecture unlabeled? *(R-37)*
- [ ] Production-shaped fake placeholders? *(R-38)*

## Block 2: Purpose-Gate (FAIL if default, no reason)

- [ ] Extra layers/abstractions by default? *(R-01)*
- [ ] Generic Manager/Helper/Util names? *(R-04)*
- [ ] Generic Data/Info/DTO types? *(R-06)*
- [ ] Middleware stack copied without need? *(R-07)*
- [ ] Pass-through wrappers? *(R-08)*
- [ ] Decorative annotations everywhere? *(R-09)*
- [ ] Interface, single impl only? *(R-10)*
- [ ] Line-by-line or duplicate-layer logging? *(R-12)*
- [ ] Retry/circuit without written trigger? *(R-13)*
- [ ] Copy-paste handlers, no reason? *(R-14)*
- [ ] Background job without idempotency story? *(R-19)*
- [ ] Mock/in-memory on prod path? *(R-22)*

## Block 3: Craftsmanship

- [ ] C-1: AI-default-only justification?
- [ ] C-2: Fake success or unlabeled stub in prod path?
- [ ] C-3: Module exists only for template?
- [ ] C-4: Happy-path-only?
- [ ] C-5: Fabricated metrics/compliance/samples?
- [ ] Architecture read declared? — **yes required** ([architecture-read.md](../templates/architecture-read.md))

## Block 4: Quality locks (all must be **no**)

- [ ] R-05 tutorial layout or god-service?
- [ ] R-11 inconsistent error contract?
- [ ] R-15 generic Success/Error messages?
- [ ] R-16 buzzwords in logs/docs?
- [ ] R-20 swap-company fails?
- [ ] R-21 lazy/missing config profile in prod?
- [ ] R-29 unnecessary dependency?
- [ ] R-30 cloned tutorial architecture?
- [ ] R-31 major decision without one-line reason?

If any Hard/Quality item is **yes**, Purpose-Gate fails, or craftsmanship fails: **do not deliver**.
