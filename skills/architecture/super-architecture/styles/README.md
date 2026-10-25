# Style catalog

Load only the guides the job named. Styles stack: pick an **in-process structure**, add **domain-driven** only when the business has a language to model, pick a **deployable shape** when the unit of deploy matters, and add CQRS or events where reads, writes or workflow demand it.

## In-process structure

| Style | Pick when | Guide |
|---|---|---|
| Layered (DDD four-layer or n-tier) | Simple domain, small team, moving from three-tier | [layered](layered/GUIDE.md) |
| Onion | Domain-centric core, high test coverage, changing infrastructure | [onion](onion/GUIDE.md) |
| Hexagonal (ports and adapters) | Several entry points, volatile integrations, complex rules, TDD | [hexagonal](hexagonal/GUIDE.md) |
| Clean | Large teams, strict module isolation, long-lived systems | [clean](clean/GUIDE.md) |
| COLA (diamond) | Java and Spring Boot enterprise teams that want scaffolding and a validator | [cola](cola/GUIDE.md) |
| Vertical slice | Feature-heavy products where change should stay in one place | [vertical-slice](vertical-slice/GUIDE.md) |
| Functional core, imperative shell | Business rules entangled with I/O; you want pure, fast tests | [functional-core](functional-core/GUIDE.md) |

## Modeling

Domain-driven design answers "what are the concepts and what do we call them." It composes with a structural style; selecting it does not deselect hexagonal, layered or a modular monolith.

| Style | Pick when | Guide |
|---|---|---|
| Domain-driven | Real business rules a domain expert could argue about; the team can talk to the people who do the work | [domain-driven](domain-driven/GUIDE.md) |

Tactical building blocks live in `core/domain-modeling.md`.

## Read, write and async flow

| Style | Pick when | Guide |
|---|---|---|
| CQRS | Read and write needs differ sharply | [cqrs](cqrs/GUIDE.md) |
| Event sourcing | Audit trail, temporal queries, replay; already running CQRS L2 | [event-sourcing](event-sourcing/GUIDE.md) |
| Event-driven | Decoupled modules or services, async workflows, streaming | [event-driven](event-driven/GUIDE.md) |
| Pipeline (pipes and filters) | ETL, streaming analytics or CI stages with isolated transformations | [pipeline](pipeline/GUIDE.md) |

CQRS and event sourcing are distinct. Most systems stop at CQRS L1. Do not adopt event sourcing as the default.

## Deployable shape

| Style | Pick when | Guide |
|---|---|---|
| Client-server | UI and logic sit across a network trust boundary (web, mobile, API) | [client-server](client-server/GUIDE.md) |
| Modular monolith | Team autonomy and enforced module boundaries without distributed operations | [modular-monolith](modular-monolith/GUIDE.md) |
| Service-based | A few coarse deployables; shared database still realistic | [service-based](service-based/GUIDE.md) |
| Microservices | Independent deploy and scale per bounded context; platform and SRE are already funded | [microservices](microservices/GUIDE.md) |
| Serverless | Bursty, event-triggered work; pay-per-execution; cold starts are acceptable | [serverless](serverless/GUIDE.md) |
| Space-based | A single database cannot hold the traffic; in-memory partitioned units | [space-based](space-based/GUIDE.md) |

Default deployable is one process. Move along this line only when team, scale or cadence force it.

## Extensibility and specialized

| Style | Pick when | Guide |
|---|---|---|
| Plugin and extension | Third parties or other teams extend a stable host (including Claude Code plugins) | [plugin](plugin/GUIDE.md) |
| Microkernel | A minimal stable kernel with sandboxed, versioned plugins (IDEs, platforms, marketplaces) | [microkernel](microkernel/GUIDE.md) |
| Game and real-time | State machines, pooling, event buses, data-driven content | [game](game/GUIDE.md) |

Plugin is the host-extension shape. Microkernel is the general platform architecture those hosts implement.
