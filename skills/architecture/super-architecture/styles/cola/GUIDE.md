# COLA (diamond architecture)

An open-source Java architecture framework from Alibaba (v5 at the time of writing) built on the diamond shape: the domain sits in the middle, with the adapter and application layers on the entry side and the infrastructure on the other.

## Pick when
- Java and Spring Boot enterprise projects, with MyBatis or JPA.
- You want engineering standards, project scaffolding and an automated architecture validator.
- Teams of roughly 5 to 50 working in multi-module Maven builds.

## Avoid when
- Non-Java stacks: use clean or hexagonal instead.
- Small or short-lived projects where the multi-module structure is overhead.

## Core idea

Four layers as Maven modules, with the domain depending on nothing:

```
adapter  ->  app  ->  domain  <-  infrastructure
```

| Layer | Module | Holds |
|---|---|---|
| Adapter | `{project}-adapter` | REST, RPC and MQ entry points, DTO conversion, input validation |
| Application | `{project}-app` | Command and query executors, transaction orchestration, extension-point routing |
| Domain | `{project}-domain` | Aggregates, entities, value objects, domain events, repository and gateway interfaces, domain abilities |
| Infrastructure | `{project}-infrastructure` | Repository and gateway implementations, persistence-object conversion, config, technical components |

An optional `{project}-client` module holds the public DTOs and service interfaces for consumers.

## v5 features
- **Extension points:** an interface marked as an extension point, with implementations selected per business identity. Use it for per-tenant or per-business variation without `if` chains.
- **Ability:** a domain capability abstraction shared across aggregates.
- **Componentized infrastructure:** distributed lock, rate limiting, circuit breaking.
- **Strict CQRS in the application layer:** separate command and query executors.

## The four P0 constraints
1. The domain has zero framework dependencies (no Spring, JPA, MyBatis, Hibernate).
2. The application layer contains no business `if` and `else`; it orchestrates.
3. The adapter layer contains no SQL and no business decisions.
4. No cycles between modules.

## Build steps
1. **Scaffold** with the project's archetype (the framework's Maven archetype for a web project) or by hand as a multi-module build.
2. **Model the domain** with aggregates and value objects; define repository and gateway interfaces here.
3. **Infrastructure:** repository and gateway implementations, with persistence objects separate from domain objects.
4. **Application:** command executors and query executors; add extension points where business variation exists.
5. **Adapter:** controllers or consumers that convert and delegate.
6. **Validate** with an ArchUnit compliance test (run through the build) or a lightweight script.

## Validation scoring (suggested)
Start at 100 and subtract 10 per P0 finding, 5 per P1 and 2 per P2. Grades: 90 and above A, 70 to 89 B, 50 to 69 C, below 50 D. P1 examples: package naming, module cycles, aggregates over five entities, cross-aggregate object references, mutable value objects.

## Naming
Aggregate root `Order` (not `OrderEntity`), value objects `Money` and `Email`, repository interface `OrderRepository` in the domain, implementation `JpaOrderRepository` in infrastructure, events in past tense (`OrderPlaced`).

## Pitfalls
Controllers in the domain module, annotations from the framework in domain classes, persistence objects used as domain objects, SQL in the application layer, business branching in executors.

## Combines with
CQRS (executors are already split), hexagonal vocabulary inside the domain (gateways as ports).
