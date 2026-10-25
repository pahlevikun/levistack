# Components and boundaries

Beyond layers: how to group code into deployable or replaceable units, and where to draw the lines that matter. This is the part of clean architecture that applies to any style.

## Contents
- Component cohesion
- Component coupling
- Boundaries
- Humble object
- Partial boundaries
- Frameworks are details
- SOLID where it matters

## Component cohesion

A component is a unit you release, replace or own as a team (a package, module, library, service). Three principles pull in different directions; balance them for the project's stage:

| Principle | Statement | Pushes toward |
|---|---|---|
| Reuse/release equivalence | Things reused together are released together | Fewer, coherent components |
| Common closure | Things that change together live together | Components grouped by business capability |
| Common reuse | Do not force users to depend on what they do not use | Smaller components |

Early in a product, favor common closure (group by capability so one change stays local). Later, as reuse grows, split.

## Component coupling

| Principle | Statement | Check |
|---|---|---|
| Acyclic dependencies | The component dependency graph has no cycles | Break a cycle by inverting one dependency or extracting a shared abstraction |
| Stable dependencies | Depend in the direction of stability | Volatile components depend on stable ones, not the reverse |
| Stable abstractions | Stable components should be abstract | A stable, concrete component is hard to change; put an interface in front of it |

A cycle is always worth fixing: it makes every change in the cycle a change to all of it.

## Boundaries

A boundary separates things that matter (business policy) from details (database, web framework, message broker). Draw it at points of likely volatility and make it with polymorphism: the inside defines an interface, the outside implements it.

- Cheapest boundary: a package or module boundary with an enforced dependency rule.
- Costlier: separate deployable components, then separate services. A service is a deployment boundary, not automatically an architectural one; a distributed ball of mud is worse than a tidy monolith.
- Defer decisions about details (which database, which broker) behind a boundary so you can decide late with real information.

## Humble object

Split hard-to-test behavior from easy-to-test behavior. The humble part is so thin that it needs almost no tests (a view, a controller, a repository implementation); the logic it delegates to is plain and tested directly. Presenters, controllers and gateways are all humble objects.

## Partial boundaries

When a full boundary is too costly now, keep the option open cheaply:
- Build the interface and the implementation in one component, but keep the dependency direction clean.
- Use a facade that hides a legacy service, so it can be replaced later.
- One-dimensional boundary: the interface exists, but only one side is separated.

Do this when you can name the future change that the boundary is for. Otherwise it is speculative abstraction.

## Frameworks are details

A framework is a tool you use, not the structure of your system. Keep it in the outermost ring, wrap what you must, and keep business logic free of its types. The test: could the use cases run, and be tested, with no web server and no database? If not, the framework has become the architecture.

## SOLID where it matters

Use the principles as design checks, not as ceremony:
- **Single responsibility:** a module has one reason to change (one actor).
- **Open-closed:** add behavior by adding code (a new adapter, a new handler), not by editing stable code.
- **Dependency inversion:** the mechanism behind the dependency rule.
- **Interface segregation:** small ports, shaped by their consumer.
- **Liskov:** every adapter must honor its port's contract; contract tests prove it.
