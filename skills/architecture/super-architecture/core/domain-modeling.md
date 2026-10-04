# Domain modeling

The tactical and strategic building blocks that the domain-centric styles (onion, hexagonal, clean, COLA, functional-core) rely on. Domain-driven design as a paradigm — language first, ceremony later, divergence protocol — is `styles/domain-driven/GUIDE.md`. Use only as much as the domain's density justifies.

## Contents
- Tactical building blocks
- Aggregate rules
- Strategic design
- Subdomains
- Domain events
- Choosing how much

## Tactical building blocks

| Block | Identity | Rule |
|---|---|---|
| Entity | By id, stable over time | Carries behavior that enforces its own rules, not just getters and setters |
| Value object | By value | Immutable, validated on construction, so an invalid one cannot exist (`Money`, `Email`) |
| Aggregate | One root entity | The consistency boundary: all rules inside hold after every operation |
| Domain service | None | Logic that fits no single entity; stateless |
| Repository | Per aggregate | Loads and saves whole aggregates; interface in the domain or application layer |
| Domain event | Past-tense fact | `OrderPlaced`, immutable, carries ids and facts, never secrets or PII |
| Factory | None | Builds an aggregate that is complicated to construct validly |

Name methods after business actions: `place`, `confirm`, `cancel`, `ship`. A method called `update` or `save` on an entity usually means the rule lives somewhere else.

## Aggregate rules

1. **Boundary from invariants.** Put in one aggregate what must be consistent in one transaction. Do not group by table or by "belongs to".
2. **Small.** Roughly more than five to ten entities is a smell. Large aggregates load slowly and cause write contention.
3. **One aggregate per transaction.** Cross-aggregate effects use domain events and eventual consistency. If a requirement truly needs atomicity across two, say so as an explicit trade-off.
4. **Reference by id.** Aggregates hold other aggregates' ids, not object references.
5. **Only the root is addressable** from outside. Callers never reach into inner entities.
6. **Enforce, do not trust.** Validation of invariants lives in the domain even if the API layer also validates input shape.

## Strategic design

- **Ubiquitous language.** One vocabulary per bounded context, used in code, tests, tickets and conversation. If the code says `Customer` and the business says `Account holder`, fix the code.
- **Bounded context.** A boundary inside which a model and its language are consistent. The same word may mean different things in two contexts, and that is fine.
- **Context map.** How contexts relate: shared kernel (a small model both teams own), customer/supplier, conformist (adopt the upstream model), and anticorruption layer (translate an upstream or legacy model so it cannot leak in).
- **Anticorruption layer.** An adapter that translates a foreign model into yours. Use it whenever another context's types would otherwise appear in your domain.

## Subdomains

| Type | Meaning | Investment | Typical structure |
|---|---|---|---|
| Core | Where the business competes | Highest, build in-house | Rich domain model, hexagonal or clean |
| Supporting | Needed, not differentiating | Moderate | Simple layered or CRUD |
| Generic | Solved elsewhere (auth, email, billing) | Buy or reuse | Off-the-shelf or thin adapter |

Do not apply heavy architecture to generic and supporting subdomains. Reserve it for the core.

## Domain events

Raise events from aggregates when something the business cares about happens. Publish them after the transaction commits for in-process handlers. When another service depends on the event, write it to an **outbox** in the same transaction and publish from there, so a crash between commit and publish cannot lose it. Handlers must be idempotent. See `styles/event-driven/GUIDE.md`.

## Choosing how much

- CRUD with no rules: no domain layer.
- A few rules: value objects and entity methods inside a simple layer.
- Dense, volatile rules: aggregates, events, repositories, ports.
- If a business invariant is unknown, name the missing rule and continue with work that does not depend on it. Do not invent business behavior.

DDD does not require a DTO, a mapper or Clean Architecture. Those land at the moment of **divergence** (the API contract must hold still while the model changes) or at an **IO boundary** (do not share a type across the wire without auditing its fields). A mapper whose fields are all 1:1 copies has no job. See `styles/domain-driven/GUIDE.md`.
