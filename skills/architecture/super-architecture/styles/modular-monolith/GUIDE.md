# Modular monolith

One deployable, many enforced modules. Teams get service-like boundaries (facades, no table sharing, independent code ownership) without a distributed runtime.

## Pick when
- You want team autonomy and clear seams but not Kafka, service discovery and on-call per module.
- Release velocity is hurt by tangled internal dependencies.
- You may extract a service later; module boundaries are the rehearsal.

## Avoid when
- The app is tiny and a module graph would be ceremony.
- You are already independently deploying services; do not wrap them back into one process without a reason.
- Boundaries exist only as folders, with no visibility rules or CI check (that is a monolith with extra directories).

## Core idea

Modules align with **business capabilities** (often bounded contexts). Each module hides its internals and exposes a façade, API object or events. Other modules never import implementation packages and never touch another module's tables. Shared code is an explicit, tiny kernel or a published contract, not a junk drawer.

The process is one: one database instance is allowed, but **schema ownership** is not shared. Views or published events are how others read.

## Layout

```
modules/
  ordering/               public façade, domain, persistence for this module
  billing/
  identity/
  platform/               truly shared kernel (auth primitive, clock), kept small
composition/              process entry, module wiring
```

Language tools: `internal` / package visibility, .NET `InternalsVisibleTo` only for tests, Java modules, ESLint `no-restricted-imports`, ArchUnit.

## Build steps
1. Name modules from capabilities, not from technical layers.
2. Give each a public façade. Move leftover cross-imports behind it.
3. Assign schema or table ownership. Ban cross-module SQL.
4. Add a CI check that fails on forbidden imports; keep one documented violation test so the rule cannot rot.
5. Track change coupling (modules that always change together). A pair over about half the time is a boundary to redraw or a future extract.
6. Record in the ADR the conditions that would extract a module to a service.

## Testing
- Module tests through the façade, with other modules faked at the façade.
- Architecture tests for import rules.
- A few process-level journeys.
- Schema ownership review in CI or a scheduled check.

## Pitfalls
Folder-only modules that import each other's internals. Shared database hotspots with no owner. A growing `platform` or `common` that becomes the real system. Extracting services before coupling metrics say so. Treating any cross-module call as a REST call "for future microservices."

## Combines with
Hexagonal or layered **inside** a module, domain-driven (one module per context), vertical slice inside a module, event-driven in-process between modules, microservices when a module's cadence or scale actually diverges.
