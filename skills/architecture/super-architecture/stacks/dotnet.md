# Stack: .NET

## Layout (solution)

```
src/
  MyApp.Domain/           entities with behavior, enums, domain exceptions, Result type; no project references
  MyApp.Application/      use-case handlers (commands and queries), interfaces, validators; references Domain only
  MyApp.Infrastructure/   EF Core, external clients, email, storage; references Application and Domain
  MyApp.Api/              endpoints, DI composition; references the others, depends on abstractions
```

Project references are the first line of enforcement: Domain has none, Application references only Domain, Infrastructure implements Application's interfaces.

## Rules
- **Domain owns the rules** as entity methods, domain services or specifications. Pure C# and base types only.
- **A use case is one class** per command or query in the Application layer. Avoid service classes with twenty methods.
- **Prefer a thin database-context abstraction** (an `IAppDbContext` exposing the `DbSet`s you need) in Application over a generic repository for every entity. Add a repository only for complex, reusable query logic.
- **Thin endpoints.** Map HTTP to a use case and the result to a response. A convention such as endpoint groups discovered at startup keeps `Program.cs` unchanged as features are added.
- **Mediator pipeline behaviors** are a good home for validation, logging and transactions around handlers. Plain handlers are fine when the pipeline is not needed.
- **Result pattern** for expected failures; exceptions for bugs and truly exceptional cases.
- **Domain events** when side effects (notifications, audit) should be decoupled from the main flow.
- Register Infrastructure services in one extension method called from the composition root.

## Clean architecture or vertical slices
Prefer clean layers for medium to large domains, long-lived systems and teams that know layering. Prefer vertical slices (a folder per feature with request, handler and validator) for feature-heavy products and quick evolution. Move from slices to layers when handlers need shared domain logic that does not belong in a common folder.

## Enforce the boundaries
Project references; plus `NetArchTest` or `ArchUnitNET` tests asserting that Domain does not depend on `Microsoft.EntityFrameworkCore` or `Microsoft.AspNetCore`, and Application does not depend on Infrastructure.

## Tests
Domain and handler unit tests without the host; integration tests with `WebApplicationFactory` and a containerized database for the full pipeline.

## Pitfalls
`DbContext` used in the Domain project, anemic entities with logic in handlers, fat endpoints, a repository per entity, EF entities exposed as API models.
