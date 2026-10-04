# Right-sizing

Architecture is a cost. The goal is the smallest structure that keeps the business rules safe and the next change cheap. These are defaults, not laws: depart from them with a written reason.

## Contents
- The default
- Over- and under-engineering
- Upgrade triggers
- Justified complexity
- Questions to ask first
- What size does not decide

## The default

Start simple. Add structure when pain is **measurable**, not when it is imaginable. A CRUD admin screen does not need ports and adapters; a payment engine with five integrations does.

| Dimension | Default | Upgrade when |
|---|---|---|
| Structure | Feature folders, or plain layers | Business rules are dense, or infrastructure changes often |
| Persistence access | The ORM or a thin gateway | The same query logic is duplicated across features, or tests need a seam |
| Ports and interfaces | None for stable internals | An external integration is volatile, costly to test, or has several implementations |
| Domain model | Data plus functions | Invariants span several entities |
| CQRS | One model (L0) | Reads and writes need different shapes or scaling |
| Event sourcing | State in tables | The business needs history, audit or replay |
| Services | One deployable | Teams, deploy cadence or scaling genuinely diverge |
| Module boundaries | Feature folders or layers | Several teams collide in one tree; add a modular monolith before services |
| Functional core | Domain plus adapters | Rules cannot be tested without I/O; extract pure decisions first |
| Serverless | Always-on process | Traffic is bursty and units are short; not for sticky state |
| Pipeline | One function or job | Independent stages must scale, fail or reuse separately |
| Space-based | Database plus cache | A single node cannot hold the working set; partitions are natural |

## Over- and under-engineering

| Context | Over-engineered | About right | Under-engineered |
|---|---|---|---|
| Simple CRUD | Hexagonal or clean | Layered or feature folders | none |
| Medium complexity | Microservices | Layered DDD, onion or modular monolith | Controllers talking to the database |
| Complex domain | none | Hexagonal or clean | Layered with anemic entities |
| High scale or heavy audit | none | Event-driven with CQRS | A single shared model |

Signs of **too much**: interfaces with one implementation that never changes, a `Manager` for every `Service`, mappers between identical shapes, a new feature touching seven files for one field. Signs of **too little**: business rules in controllers, tests that need a database to check a rule, one change rippling through unrelated modules.

## Upgrade triggers

Move up one step only when you can point to the trigger:

- **Add a port** when a second implementation exists or is planned, a test cannot run without the real dependency, or the dependency has bitten you twice.
- **Add a domain layer** when a rule involves several entities or states and keeps being re-implemented.
- **Add CQRS L1** when one service class mixes reads and writes and has become hard to reason about. **L2** when read load or query shape needs its own store. **L3** (event sourcing) only for audit, temporal queries or replay, and only after L2 worked.
- **Split a service** when deploy cadence, scaling profile or team ownership differ, or when a bounded context is already isolated. Merge when consistency needs are strong and the context is small. Prefer modular monolith, then service-based (shared DB, named owners), then microservices.
- **Go serverless** when the work is event-triggered, short and idle most of the time. Do not use it to avoid designing modules.
- **Add a pipeline** when stages have their own scale, failure or reuse story. Do not pipe a simple request/response flow.

## Justified complexity

Complexity is acceptable when a regulation demands an audit trail, an integration is known to change, a core domain is where the business competes, or several teams must work in parallel without stepping on each other. Say which one applies.

## Questions to ask first

1. What problem is this structure solving today?
2. What breaks, and what does it cost, if we do the simpler thing?
3. Is the pain measured (cycle time, defects, merge conflicts) or only expected?
4. Is the team able to maintain it? An architecture the team does not understand decays quickly.

## What size does not decide

Team size, entity count and file length do not by themselves decide whether domain modeling is warranted. Domain density and change frequency do. Apply the heavier patterns to the **core** domain only; generic and supporting domains (authentication, notifications, reports) stay simple.
