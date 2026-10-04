# Anti-pattern catalog

Symptom, how to confirm it, and the fix. `scripts/arch-scan.mjs check` finds candidates for the first group; confirm each by reading the code. Priorities: **P0** blocks merging or is a boundary break, **P1** fix soon, **P2** polish.

## Contents
- Boundary breaks
- Domain model smells
- Structure smells
- Over-engineering
- Event and CQRS smells
- Fix order

## Boundary breaks

| Anti-pattern | Symptom | Confirm | Fix | Pri |
|---|---|---|---|---|
| Framework in the core | ORM annotations, web types or SDK clients in domain classes | Search the domain folder for framework imports | Persistence model in the adapter; domain stays plain; map at the edge | P0 |
| Core depends on adapter | Domain or application imports infrastructure | Imports point outward | Define the interface inside; implement outside | P0 |
| Skipped use case | Controller calls the repository directly | Search controllers for repository calls | Controller, then use case, then port | P0 |
| Business logic in adapters | `if` and `switch` on business rules in controllers, repositories or consumers | Review adapter methods longer than translation | Move the rule into the domain or a use case | P0 |
| Leaky port | Port signature exposes HTTP, SQL or SDK types | Read port interfaces | Replace with domain types or DTOs | P1 |
| Adapter to adapter | One adapter calls another directly | Imports between adapters | Route through a use case and a port | P1 |
| Missing port | A use case calls an external service directly | Search use cases for client or SDK calls | Introduce a port for the capability | P1 |
| Domain scope pollution | Third-party types (`StripePayment`) appear in the domain | Search the domain for vendor type names | Keep them in the adapter; translate at the boundary | P1 |
| Cycle between modules | Import error between packages, or changes ripple everywhere | Dependency graph has a cycle | Invert one dependency or extract a shared abstraction | P1 |

## Domain model smells

| Anti-pattern | Symptom | Fix |
|---|---|---|
| Anemic domain | Entities are getters and setters; all logic in services; services over ~500 lines | Move rules into entities and value objects |
| CRUD thinking | Methods named `save`, `update`, `delete` | Rename to business actions (`place`, `confirm`, `cancel`) |
| Repository per table | A repository for every table, far more than aggregates | One repository per aggregate; inner entities have none |
| God aggregate | One aggregate with many entities, slow loads, write conflicts | Split along transactional invariants |
| Cross-aggregate transaction | One transaction updates several aggregates | Domain events and eventual consistency |
| Cross-aggregate references | Aggregates hold each other's objects | Hold ids |
| Value-object overuse | Every string wrapped in a class | Wrap only values with rules or meaning (`Money`, `Email`) |
| Premature database design | Schema designed before the model | Model first; the adapter maps to the schema |

## Structure smells

| Anti-pattern | Symptom | Fix |
|---|---|---|
| Brittle interfaces | `register(username, password)` breaks when email is required | Pass a command or request object that can grow |
| Use-case interdependency | Use cases call other use cases | Extract shared domain logic; keep each use case self-contained |
| Fat controller or endpoint | Controller does more than parse, call, format | Extract a use case |
| Slice theater | Vertical folders but logic is still central and tangled | Move behavior into the slice; remove the central service |
| Hidden shared layer | A `shared/` or `common/` folder that every feature depends on | Give each item an owner; extract only proven duplication |
| God port | A port with ten or more methods | Split by capability |
| Over-complicated adapter | Adapter does more than translate | Thin it; move logic inward |

## Over-engineering

- Interfaces with exactly one implementation and no volatility or test need.
- Mappers between identical shapes; a `Manager` per `Service`.
- Hexagonal or clean structure on a CRUD admin tool.
- Cargo-cult DDD: entities and value objects with no business language behind them; DTOs and mappers added "because DDD."
- Adapter explosion: ports for stable internals.
- Microservices adopted as an architecture rather than for a deployment need.
- Distributed monolith: many repos or processes, one lockstep release, shared tables.
- Kernel bloat: features land in a microkernel instead of a plugin.

Fix by removing the layer until a named pain justifies it. See `core/right-sizing.md`.

## Event and CQRS smells

| Anti-pattern | Symptom | Fix |
|---|---|---|
| CQRS without need | Read and write load are similar; double the code | Collapse to one model; add separation when the difference shows |
| Event sourcing without audit need | Complexity, no temporal queries | Downgrade to L1 or L2 |
| Non-idempotent handlers | Redelivery creates duplicates | Dedup table, state-machine guard or natural idempotency |
| Dual write | Writes the database and publishes in two steps | Outbox in the same transaction |
| Mutable events | Published events edited or deleted | Append a corrective event; version schemas |
| Sensitive data in events | Passwords or PII in event bodies | Carry ids and facts only |
| Query that writes | A query handler changes state | Move the write to a command |

## Deployable-shape smells

| Anti-pattern | Symptom | Fix |
|---|---|---|
| Shared-table writes | Two services update the same tables | One owner; others use API, events or a view |
| Chatty client | Many small HTTP calls per user action | BFF or façade; batch; cache |
| Thick client drift | The same rule exists in UI and API and they disagree | Server owns invariants; share shape checks only |
| Logic in the shell | Handlers contain business `if` | Move the decision into the functional core |
| Silent IO leak | A shared type crosses the wire with extra fields | Audit every serialized type; version the request DTO |
| Pipeline god-filter | One stage does three transforms | Split filters; contract-test the schemas |

## Fix order

1. **P0:** remove framework types from the core, cut outward dependencies, remove cycles, stop controllers skipping use cases.
2. **P1:** make core aggregates rich, add the value objects that carry rules, replace cross-aggregate transactions with events.
3. **P2:** naming, thin adapters, tidy shared code.

One change per commit; keep the tests green between steps.
