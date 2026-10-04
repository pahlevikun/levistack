# Vertical slice architecture

Organize code by feature, not by technical layer. One business capability is one slice that holds everything it needs end to end, so a product change stays in one place.

## Pick when
- Feature-heavy products, medium to large lifetime, several developers changing different features at once.
- You want small review diffs, clear ownership, and incremental migration of legacy code.
- AI-assisted development, where deterministic boundaries per use case help.

## Avoid when
- A tiny, short-lived script or mostly generic CRUD where plain structure is enough.
- Heavy shared domain logic across every feature; consider a domain-centric style with slices on top.

## The five rules
1. **One feature, one directory** with handler, request and response types, validation and tests.
2. **One entry point per feature:** a single setup or registration function that wires the slice to the framework. The name varies by convention; the role is the invariant.
3. **Low coupling between slices, high cohesion inside a slice.**
4. **No premature shared layers.** No global repository or service layer until duplication is real across slices.
5. **Test through the entry point,** asserting outcomes (stored state, external calls, the response).

## Layout

```
features/
  orders/
    place_order/        handler, request, response, validator, tests
    cancel_order/
  billing/
platform/               auth, error handling, logging, db pool, middleware, observability
app/ (main)             composition root; registers each feature
```

## Roles for the boundary map
Classify every responsibility: **entry point**, **composition** (bootstrap, lifecycle), **feature slice**, **shared kernel** (stable concepts with identical meaning across slices), **shared capability** (a cohesive subsystem with its own facade and proven consumers), **infrastructure**. Give every piece of mutable state and every shared abstraction one owner.

## Add a feature
1. Name the business intent (`PlaceOrder`).
2. Create `features/<domain>/<operation>/`.
3. Define the handler with a single exported setup function.
4. Add request and response types (inline for simple cases) and validation.
5. Register it in the composition root.
6. Write an integration test that calls the setup function, sends a request and checks outcomes.

## Cross-cutting concerns
Put them in `platform/`, not inside a feature: authentication middleware, error handling, request logging, database pooling, circuit breakers, idempotency, event notification, tracing and metrics.

## Sharing code
Move code to shared ownership only when **all** hold: (1) at least two current slices need it, (2) they use the same semantics and invariants, not just a similar shape, (3) the abstraction stays feature-neutral, (4) likely changes belong to all consumers together. Share only canonical identity, stable domain vocabulary, query or ordering semantics, and stateless presentation. A modest shared kernel plus slightly duplicated slice code beats a premature abstraction that couples unrelated features. `shared/` is not a parking place for code with no owner.

## Mixing with other styles
Keep ownership vertical; use the other patterns as local tools inside the slice.
- **With DDD:** ubiquitous language in slice and command names; aggregate invariants near the slice's domain behavior; share domain primitives only with proven identical meaning.
- **With hexagonal:** define ports from the slice's needs and put adapters next to the slice or in a narrow infrastructure module mapped to it, not in one global adapter folder.
- **With layering:** small local layers inside a slice (endpoint, application, domain, infrastructure); never one global bucket of handlers, services and repositories.

## Anti-patterns
Slice theater (vertical folders, central tangled logic), cargo-cult DDD (entities with no domain language), adapter explosion (ports for stable internals), a hidden monolith layer in an overgrown `shared`, one slice calling another slice's internals.

## Adopt incrementally
Start new features as slices; move one high-change legacy flow at a time; add guardrails in review and automated checks (`core/testing-architecture.md`); measure cycle time, defects and coupling trend. Do not rewrite everything at once.

## Judgment
VSA does not require a universal folder tree, one file per use case, CQRS, DDD, dependency injection or microservices. Add each only if it pays independently. Handlers per slice may be as thin as a single function.

## Combines with
CQRS inside slices that need it, hexagonal for volatile integrations, event-driven for cross-slice reactions.
