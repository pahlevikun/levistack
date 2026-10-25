# Layered architecture (DDD four-layer)

The simplest entry into domain-centric design. It turns the traditional three tiers (controller, service, data access) into four layers and inverts the persistence dependency so the domain becomes the center.

## Pick when
- Simple to moderate business rules, small team (about 1 to 5), CRUD-leaning product.
- Moving from a three-tier or MVC codebase and wanting the gentlest learning curve.
- A prototype that will probably grow, and should have a clear upgrade path.
- Compliance or operations need a familiar, documented split (UI, rules, persistence) and the deployable stays one process.

## Avoid when
- Dense, volatile business rules, or infrastructure that changes often: use hexagonal, onion or clean.
- Many entry points (HTTP plus CLI plus queue plus gRPC): hexagonal handles this more naturally.
- Independent scale or deploy per capability: modular monolith or services, not more layers.
- Real-time fan-out where every hop through a layer is wasted: event-driven or a pipeline.

## Core idea

Name the stack you are actually using. They are not the same rule.

| Stack | Layers | Dependency |
|---|---|---|
| Traditional 3-tier | Presentation → business → data access | Each layer may depend only on the one below; data access does not know the UI |
| DDD four-layer (this guide's default) | Interface → application → domain ← infrastructure | `Infrastructure` depends on `Domain` (inverted persistence) |
| 5-layer | UI → controller → application → domain → persistence | Extra hop; only when UI and controller teams are truly separate |

Three tiers become four layers: **Interface** (controllers, consumers), **Application** (use cases, orchestration, transactions), **Domain** (entities, value objects, repository interfaces, domain events), **Infrastructure** (repository implementations, clients, persistence models). The key move in the four-layer form is that `Infrastructure` depends on `Domain`, not the reverse.

Cross-cutting work (auth, logging, validation of shape) lives once as middleware or policy, not copied into every layer.

## Layout

```
interface/        controllers, request and response DTOs, assemblers
application/      use-case services, commands, queries, transaction handling
domain/           aggregates, value objects, domain services, repository interfaces, events
infrastructure/   repository implementations, persistence models, gateways, config
```

## Dependency rules

| Layer | May depend on | Must not depend on |
|---|---|---|
| Interface | Application | Domain internals, Infrastructure |
| Application | Domain | Interface, Infrastructure |
| Domain | Language standard library | Every other layer and every framework |
| Infrastructure | Domain | Interface, Application |

Direction: `Interface -> Application -> Domain <- Infrastructure`.

## Build steps

1. Create the four folders and an architecture test that enforces the table.
2. Model the first aggregate in the domain with behavior, not just fields. Define its repository interface there.
3. Add an application service per business action; it loads the aggregate, calls it, saves it, owns the transaction.
4. Implement the repository in infrastructure with a separate persistence model; map at that edge.
5. Add the controller: parse, call the application service, format the response. No business `if`.
6. Wire in one composition root.

## Checklist
- [ ] Domain imports no framework, ORM or other layer.
- [ ] Controllers contain no business rules and do not call repositories.
- [ ] Application services contain orchestration, not SQL and not business branching.
- [ ] One repository per aggregate, not per table.
- [ ] Value objects are immutable; aggregates reference each other by id.

## Pitfalls
- Anemic entities with all logic in application services.
- DTOs leaking into the domain, or ORM entities used as domain objects.
- Treating the application layer as "the old service layer" and keeping SQL there.
- Repository interfaces placed in infrastructure.
- Shortcut imports that skip a layer; treat them as build failures (`scripts/arch-scan.mjs check`).
- Pass-through methods on every layer for one feature. If a change only forwards a DTO, collapse the hop or add a façade rather than more layers.

## Evolution

Three-tier, then four-layer, then rich domain, then domain events and CQRS L1, then hexagonal, clean or COLA when a measured need appears. See `jobs/migrate.md`.

## Combines with
Vertical slice (a small layered shape inside each feature), CQRS L1 (split command and query services in the application layer).
