# The dependency rule

The one rule every architecture style restates in its own words: **source code dependencies point toward the business rules, never away from them.** Layered, onion, hexagonal, clean and COLA differ in vocabulary and folder names, not in this rule.

## Contents
- The rule
- Who owns the abstraction
- What crosses a boundary
- Composition root
- Deciding what is inside
- Variants that are all valid

## The rule

| Ring | Contains | May depend on |
|---|---|---|
| Domain | Entities, value objects, aggregates, domain services, domain events | Nothing outside the language's standard library |
| Application | Use cases, command and query handlers, port interfaces | Domain |
| Adapters and infrastructure | Controllers, repositories, API clients, queue consumers, ORM models | Application and domain |
| Composition root | Wiring of concrete adapters to use cases | Everything |

Inner rings never import, name or reference anything from an outer ring: no class, function, annotation, exception type or data format. The compiler or an architecture test should enforce it; a code review should not have to.

## Who owns the abstraction

The side that needs a capability defines the interface; the side that provides it implements the interface. A use case needs to save orders, so the **use case's layer** defines `OrderRepository`, and a Postgres adapter implements it. If the adapter's package defines the interface, the dependency points the wrong way.

- Aggregate repositories may sit beside the aggregate in the domain; use-case ports and other outbound ports sit in the application layer. Either is fine while the dependency still points inward.
- Model capabilities, not technologies: `PaymentGateway`, not `StripeClientPort`.
- Keep ports small and cohesive. A port with ten or more methods is a sign it should split.

## What crosses a boundary

Data crossing a boundary takes the shape that is most convenient for the **inner** side, never the outer one.

- Pass plain data structures (DTOs, commands, results). Never hand an ORM entity, an HTTP request object or a database row to the inside.
- Map at the adapter: request to command, domain object to response, domain object to persistence model.
- Errors cross the same way. Adapters return transport outcomes; the domain owns the meaning of an error; exactly one place maps errors to the wire.
- Third-party types (a payment SDK's `Payment`, an identity provider's `User`) stay in adapters and are translated into domain types at the edge.

## Composition root

One place at the program's entry point builds the concrete objects and injects them. No layer constructs its own infrastructure, and no layer looks dependencies up in a global container (service locator).

- Frameworks with dependency injection (Spring, NestJS, ASP.NET) are fine; keep the container configuration in the outermost layer.
- Without a container, use a plain factory or a `main` function. This is often clearer for small services.

## Deciding what is inside

For any class or function, ask: **Does it do I/O or run out of process? What does it depend on?** If it does I/O, or depends on a framework, a database driver or an SDK, it is outside, even if its own logic is simple. The inside contains both the domain and the application layers; adapters sit outside both.

## Variants that are all valid

- Three layers or four. A separate presentation layer is optional; driving adapters may live under `infrastructure/http` if that is the project's convention.
- Repository interfaces in the domain (DDD-centered) or under `application/ports` (hexagon-centered).
- Explicit port interfaces everywhere, or the use-case handler's public method as the driving port in small codebases.

Follow the project's convention. Do not create a second home for the same thing.
