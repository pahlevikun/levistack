# Job: migrate

Move a system from one structure to another without a rewrite. The method is the strangler fig: new behavior goes into the target structure, old behavior is replaced one slice at a time, and the old path stays until the new one is proven.

## Contents
- Principles
- Before you start
- The slice loop
- Evolution ladder
- From three-tier to domain-centric
- Toward hexagonal or clean
- Toward vertical slices
- Risk and rollback
- Done

## Principles

1. **No big-bang rewrites.** Migrate per slice and keep behavior identical.
2. **Characterize first.** Add tests around legacy behavior before touching it; keep them until the new boundary is proven equivalent.
3. **Facade before replacement.** Wrap a legacy service behind a port so its internals can change later.
4. **Centralize wiring early,** so new dependencies stop leaking into the core.
5. **High churn, low blast radius first.** Pick slices that hurt often and break little.
6. **One reversible switch per slice** (a flag or route toggle) until production behavior is verified.

## Before you start

- [ ] Current architecture detected and documented (`jobs/detect.md`, `jobs/document.md`)
- [ ] A reason for migrating that is measurable (cycle time, defects, blocked features)
- [ ] Target style chosen and agreed (`jobs/select.md`), with an ADR
- [ ] Scope: incremental by slice, not the whole system
- [ ] Rollback plan, ideally executable within hours
- [ ] The baseline test and build commands recorded, and green

## The slice loop

1. Pick one slice (one endpoint, job or workflow).
2. Add characterization tests for its current behavior.
3. Extract a use-case boundary with explicit input and output types.
4. Introduce outbound ports around the infrastructure calls it makes.
5. Move orchestration out of controllers and services into the use case.
6. Keep the old entry point, but make it delegate to the new use case.
7. Switch traffic behind the toggle; compare behavior.
8. Remove the old path once stable. Repeat.

## Evolution ladder

```
Traditional three-tier
  -> DDD four-layer (extract domain and infrastructure)
  -> Rich domain or functional core (behavior, or pure decisions, leave the I/O)
  -> Domain events and CQRS L1
  -> Hexagonal, clean or COLA where the need is proven
  -> Modular monolith (enforced module façades)
  -> Service-based (coarse deployables, schema owners)
  -> Independent services per bounded context
```

Stop at the rung that solves the measured pain. Most systems do not need the last two. Serverless and space-based are not rungs on this ladder; they are deployable shapes chosen from traffic, not from "more architecture."

## From three-tier to domain-centric

1. Characterization tests on the slice.
2. Extract domain: move rules from the service into entities and value objects; the persistence model stays in the adapter.
3. Introduce use cases: one class or function per business action; controllers call them.
4. Invert persistence: the use-case layer defines the repository interface; infrastructure implements it.
5. Move wiring to a composition root.
6. Retire the old service methods.

## Toward hexagonal or clean

Start from the slice loop. Define outbound ports first (persistence, external calls, clock), then the inbound use-case interface, then adapters. Keep old adapters delegating to the new use case during the transition.

## Toward vertical slices

Move one feature at a time into `features/<capability>/<operation>/`, with its handler, types, validation and tests together. Leave shared technical code in a `platform` folder and move domain code into a slice or a small shared kernel only once two slices prove identical meaning. New features start as slices from day one.

## Toward a modular monolith

Carve modules from bounded contexts, not from technical layers. Give each a façade, hide internals, assign schema ownership, then add a CI import rule. Do not extract a service until change-coupling and deploy cadence say the module is already independent.

## Toward functional core

Inventory side effects first. Extract one high-churn module into pure functions that return commands; leave I/O in the shell. Architecture tests must fail if the new core imports a framework. Do not rewrite the whole app in one pass.

## Toward services

From a modular monolith, extract the module whose cadence, scale or ownership already diverges. Give it its own store (microservices) or keep schema ownership on a shared database (service-based). Stand up tracing, contract tests and a rollback **before** the second independent deploy. Never big-bang a rewrite into "microservices."

## Domain by domain (strangler)

When the goal is a language and context map, do not migrate every layer at once. Per domain: split data access, then the business module, then redirect callers, then the view. Repeat. See `styles/domain-driven/GUIDE.md`.

## Risk and rollback

| Blast radius | Rollout |
|---|---|
| High: core business logic, money, data | Canary release, automatic rollback, parallel comparison |
| Medium: non-core features | Parallel run with mirrored traffic |
| Low: read-only queries | Direct switch with performance checks |

Keep each slice reversible with one switch. Do not remove the old path until the new one has run in production without regressions for an agreed period.

## Done

- The slice runs through the new structure, the old path is removed or frozen, and the characterization tests pass against the new path.
- The architecture check shows no new violations.
- Behavior, not only tests, was compared (`super-verify` gate), and the result was read.
- The ADR records what moved, what remains, and the next slice.
