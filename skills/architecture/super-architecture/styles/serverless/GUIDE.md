# Serverless (functions)

Work runs as short, stateless handlers triggered by events (HTTP, queues, timers). The platform scales to zero and bills per execution. You own code, IAM, and the surrounding managed services, not servers.

## Pick when
- Traffic is bursty or idle most of the time; pay-per-execution beats a always-on fleet.
- Units of work finish inside the platform timeout and need no local sticky state.
- Cold-start latency is acceptable, or you will pay for provisioned concurrency on the hot paths.

## Avoid when
- Long-running jobs, persistent connections (games, WebSockets at volume) or in-process state.
- A tight latency SLO that cold starts would miss and warming would erase the cost win.
- You need many chatty intra-app calls; function-to-function hop tax adds up. Prefer one function plus a modular core, or a small always-on service.

## Core idea

Handlers are **idempotent** and hold **no durable state**. Databases, queues and object stores sit outside. Wiring, permissions and budgets are declared as infrastructure-as-code. Least-privilege IAM is per function, not a shared god role.

## Layout

```
functions/<name>/         handler, its tests, its IAM snippet
packages/core/            shared pure logic (keep the bundle small)
infra/                    IaC: triggers, queues, tables, budgets
```

A hexagonal or functional-core package behind a thin handler keeps vendor APIs out of the rules.

## Build steps
1. Cut workloads into event-triggered handlers. If two always deploy together and call each other synchronously, keep them as one.
2. Externalize state. Design for at-least-once delivery: idempotency keys, conditional writes.
3. Keep dependencies small on latency-sensitive paths; add provisioned concurrency only where measured.
4. Trace, structure logs, set per-function memory, timeout and cost alarms.
5. Deploy from IaC (SAM, CDK, Terraform or equivalent) so an empty account can recreate the system.
6. Watch provider quotas (concurrency, payload size) and design shards before you hit them.

## Testing
- Handler tests with replayed events: twice yields one effect.
- Core tests without the cloud SDK.
- Contract tests against the trigger payload schema.
- A smoke deploy per environment; measure cold-start and duration on the hot function.

## Pitfalls
Vendor types in the domain. God functions. Hidden coupling through a shared table. No idempotency. Debugging across hops without trace ids. Ignoring cost until the bill. Cold-start surprise in the user-facing path.

## Combines with
Functional-core (handler is the shell), hexagonal (SDK behind a port), event-driven (queue and bus triggers), pipeline (each stage a function), client-server (API Gateway as the server edge).
