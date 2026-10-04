# Clean architecture

Use-case-centric structure with a strict dependency rule: source dependencies point only inward, from frameworks to interface adapters to use cases to entities.

## Pick when
- Large teams (about 15 to 50) and long-lived systems that need strict module isolation.
- You want use cases as the first-class unit and delivery mechanisms as plugins.
- Several components that must be built and deployed independently.

## Avoid when
- Small teams (under about 5), rapid MVPs, simple CRUD.
- You have not yet felt the pain that the extra ceremony prevents.

## Core idea

Four rings, innermost first: **Entities** (enterprise rules), **Use cases** (application rules), **Interface adapters** (controllers, presenters, gateways), **Frameworks and drivers**. Inner rings never name anything from an outer ring. The inner ring defines the input and output boundaries; outer rings implement them.

## Layout

```
entities/               enterprise business rules; aggregates, value objects, events
usecases/               one interactor per use case, with input and output ports
adapters/               controllers, presenters, repository and gateway implementations
frameworks/ (or main)   web, database and UI wiring; the composition root
```

## Dependency rules

| Ring | May depend on |
|---|---|
| Entities | Nothing |
| Use cases | Entities |
| Interface adapters | Use cases and entities |
| Frameworks | Everything, as the outermost ring |

The number of rings is not fixed; the rule is.

## Build steps

1. **Confirm the basics:** the team shares an understanding of entities, value objects and aggregates.
2. **Entities:** identify aggregate roots, design entities and value objects, implement rules, define domain events.
3. **Use-case ports:** for each use case, an input port, an output port and plain request and response data.
4. **Interactors:** orchestrate entities and call output ports and gateways; publish events.
5. **Adapters:** controller (parse and call the input port), presenter (format the output port's result), repository and gateway implementations.
6. **Frameworks and wiring:** dependency injection configuration at the edge.
7. **Verify:** entity unit tests, use-case tests with fakes, adapter integration tests, and an architecture test for the dependency rule.

## Rules
- Data crossing a boundary is plain data in the form the inner ring wants. Never pass an ORM entity or a request object inward.
- One focused interactor per use case. Avoid a giant orchestrator per feature.
- Controllers and presenters are humble objects: no business logic.
- The framework is a detail, confined to the outermost ring.
- Components follow the cohesion and coupling principles in `core/components-and-boundaries.md`.

## Checklist
- [ ] Use cases run with no database, no web server and no framework.
- [ ] All imports point inward.
- [ ] The database can be swapped without touching entities or use cases.
- [ ] The component graph has no cycles.
- [ ] Construction of concrete classes happens only in the composition root.

## Pitfalls
ORM models used as entities, business rules in controllers, framework-first structure, circular components, one huge use case per feature, skipping boundaries "because it is simple", treating microservices as an automatic cure.

## Combines with
DDD tactical patterns inside entities; CQRS with separate command and query interactors; hexagonal vocabulary for gateways. For a .NET project, prefer a thin database-context abstraction over a repository for every entity (`stacks/dotnet.md`).
