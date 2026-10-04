# Onion architecture

Concentric rings with the domain model at the center. Every dependency points to the center; inner rings define interfaces, outer rings implement them.

## Pick when
- A domain-centric core, high test coverage goals, and infrastructure that may change (database, broker).
- A team of roughly 5 to 15 that is comfortable with abstraction.
- You want the domain model to be the stable thing and everything else replaceable.

## Avoid when
- CRUD-heavy apps with little business logic.
- Teams with no experience with interfaces and inversion; start layered.

## Core idea

Four principles: the application core is independent of infrastructure; the core defines interfaces and outer rings implement them; all coupling points inward; the domain model sits at the center and owns the rules.

## Layout (modules)

```
core/domain/            aggregates, value objects, repository interfaces, events
core/application/       use-case interfaces and services; orchestration only
infrastructure/         repository, messaging and client implementations
api/                    controllers, DTOs, assemblers, global error handling
composition/            the one place that wires everything
```

## Dependency rules

| Module | May depend on | Must not depend on |
|---|---|---|
| `core/domain` | Nothing (language only) | Any framework, ORM or other module |
| `core/application` | `core/domain` | `infrastructure`, `api` |
| `infrastructure` | `core` | `api` |
| `api` | `core`, `infrastructure` (through composition) | |
| `composition` | All modules | |

## Build steps

1. Create the five modules; enforce the table with the build tool or an architecture test.
2. Write the domain: aggregates, value objects, repository interfaces, domain events. Zero framework imports.
3. Write the application interfaces and services: pure orchestration, no business branching.
4. Implement infrastructure: repositories, message publishers, external clients, with persistence models mapped at the edge.
5. Write the API adapters: controllers, DTOs, assemblers, error mapping.
6. Assemble dependencies in `composition`.
7. Test in order: domain unit tests, application tests with mocks, infrastructure integration tests.

## Checklist
- [ ] Domain has no framework imports.
- [ ] Repository interfaces are in the core, implementations outside.
- [ ] Application layer is thin; no business `if` in it.
- [ ] Value objects are immutable; aggregates are small; cross-aggregate references use ids.
- [ ] DTOs stay in `api`; controllers hold no business logic.
- [ ] Wiring lives only in `composition`.

## Pitfalls
Framework leakage into the domain, interface placed in the wrong ring, a thick application layer, over-abstraction, wiring scattered across modules, mutable value objects, oversized aggregates, DTOs reaching the domain.

## Onion, hexagonal and clean
They share the dependency rule. Onion emphasizes **layers around a domain model**. Hexagonal emphasizes **ports and adapters** and the symmetry of driving and driven sides. Clean emphasizes **use cases and the entity/use-case split** plus component principles. Pick the vocabulary your team will keep using; the structure converges.

## Combines with
CQRS (command and query interfaces in the application ring), vertical slice (slices over the core), event-driven (outbox in infrastructure).
