# Microservices

Independently deployable services, each owning a bounded context and its data. Autonomy is the point; the network and operational platform are the cost.

## Pick when
- Teams need independent release cycles, and capabilities have different scale, stack or risk profiles.
- Bounded contexts are already clear and each can own its data without shared tables.
- The organization will fund a platform: discovery, tracing, CI templates, contract tests, on-call.

## Avoid when
- Small team, early product, or requirements still changing shape every week.
- Strong transactional consistency is required across the would-be service cuts.
- DevOps and observability are not yet a practice. Distribution without a platform is a distributed monolith.
- Regulatory constraints make split data harder than the autonomy is worth.

Default is fewer services. Prefer a modular monolith until a real split trigger appears (`core/right-sizing.md`).

## Core idea

One service, one business capability, one data store. Other services see **APIs or events**, never tables. Communication is either synchronous (with timeouts, retries, circuit breakers, bulkheads) or asynchronous (with idempotency and an outbox). Consistency across services is eventual; sagas coordinate with compensation, not distributed transactions.

## Layout

```
services/<context>/       one deployable: code, its database, its CI
  src/                    often hexagonal or vertical-slice inside
platform/                 golden-path templates, telemetry, CI, catalog
contracts/                OpenAPI / AsyncAPI / event schemas
```

## Build steps
1. Map services to bounded contexts and write data ownership down. No shared tables.
2. Stand up the platform **before** the second independent deploy: discovery, tracing, logs, CI template, contract tests.
3. Pick sync versus events per flow. Document SLIs and SLOs.
4. Put timeouts, retries (bounded), circuit breakers and bulkheads on every outbound call.
5. Automate security scanning, dependency policy and versioning across services.
6. Add a saga or process manager only where a business flow spans services.

## Testing
- Unit tests inside each service.
- Consumer-driven contract tests on every published API or event; they gate merges.
- A few cross-service journeys in a composed environment.
- Resilience tests: timeout, retry storm, downstream down.

## Granularity
A service that is too small pays in hops and coordination. Track **change coupling**: services that always ship together are merge candidates. A service that owns a thin CRUD table and must join three others to answer one question was split too early.

## Pitfalls
Shared database. Distributed monolith (many repos, one lockstep release). Chatty sync chains. Missing platform. Over-splitting. Sagas without compensation. No idempotency. Treating "microservices" as a folder layout instead of a deploy and ownership model.

## Combines with
Domain-driven (context map first), hexagonal or vertical slice **inside** each service, event-driven between services, CQRS per service that needs it, modular monolith as the step before the first split, client-server at the edge (BFF or gateway).
