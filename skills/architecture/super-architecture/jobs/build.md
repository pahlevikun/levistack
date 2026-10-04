# Job: build

Create code in a chosen architecture: a new service skeleton, a new feature, or a new adapter. Work inside out, keep the project's own conventions, and prove the boundaries hold.

## Contents
- Before writing
- Scaffold a new service
- Add a feature
- Add an adapter
- Per-style notes
- Checks
- Do not

## Before writing

1. **Confirm the style.** If the project has code, run `node scripts/arch-scan.mjs detect <dir>` and follow what it finds. If greenfield, run the select job first, or confirm the user's choice.
2. **Load the style guide** (`styles/<style>/GUIDE.md`) and the stack guide (`stacks/<stack>.md`). Open `core/naming-and-layout.md` for names.
3. **Read the nearest existing feature** and copy its shape. Match the project's naming, error handling, test style and dependency injection.
4. **Decide the size.** Apply `core/right-sizing.md`: no port for a stable internal, no domain layer for pure CRUD.

## Scaffold a new service

Order of work, innermost first. Each step compiles and tests before the next.

1. **Folder skeleton** for the chosen style (layout is in its guide). Add only the folders you will use now.
2. **Dependency rule as a test** before any code: an architecture test or script that fails when the domain imports an outer ring (`core/testing-architecture.md`).
3. **Domain:** the first aggregate or a few value objects and their rules, with unit tests. No framework imports.
4. **Application:** the first use case with a command and result type, calling outbound ports.
5. **Ports:** define the interfaces the use case needs, in the layer that needs them.
6. **In-memory adapters** for those ports, then the use-case tests using them.
7. **Real adapters:** persistence first, then the inbound adapter (HTTP, CLI, consumer), each thin, with integration tests.
8. **Composition root:** wire concrete adapters to use cases in one place.
9. **One end-to-end journey** through the inbound adapter.
10. **Run the checks** below and read the output.

## Add a feature

1. Name the business intent as a verb phrase (`PlaceOrder`).
2. Write the failing use-case test first, with fakes for ports.
3. Add or extend domain rules, with unit tests.
4. Implement the use case: validate application-level preconditions, load aggregates, call domain behavior, save, publish events.
5. Add port methods only if an existing port cannot express the need.
6. Implement adapter changes (persistence mapping, endpoint, consumer).
7. Wire it in the composition root or the feature's entry point.
8. Run the feature's integration test and the architecture check.

In feature-first projects, all of this happens inside the feature's folder; in layer-first projects it spans the layer folders in the same inside-out order.

## Add an adapter

1. Find the port it implements. If there is none, ask whether a port is warranted (`core/right-sizing.md`).
2. Implement the port with no business logic: translate, call, translate back.
3. Map vendor types to domain types inside the adapter.
4. Run the port's contract test suite against it. Add one if missing.
5. Register it in the composition root; configuration comes from one typed place.

## Per-style notes

| Style | Where the extra care goes |
|---|---|
| Layered | Keep controllers thin; one repository per aggregate, not per table |
| Onion | Core, infrastructure, api and composition modules; composition wires everything |
| Hexagonal | Driving and driven ports; port ownership; in-memory adapters |
| Clean | Input and output boundaries; interactors; presenters as humble objects |
| COLA | Command and query executors, gateways, extension points; run the validator |
| Vertical slice | One entry point per feature; shared code only after proven reuse |
| CQRS | Commands return no domain data; queries never write; handlers per use case |
| Event-driven | Outbox in the same transaction; idempotent consumers |
| Event sourcing | Given-events / when-command / then-events; replay tool exists before production |
| Functional core | Side-effect inventory first; core returns commands; no I/O imports in core |
| Domain-driven | Glossary terms in types; no DTO until shapes diverge |
| Modular monolith | Public façade only; architecture test on module imports |
| Service-based | Contract and schema owner before the second deployable |
| Microservices | Platform (trace, CI template, contract tests) before the second service |
| Serverless | Idempotent handler; IaC; vendor SDK stays out of core |
| Pipeline | One schema per filter; back-pressure and replay named |
| Client-server | Contract and version-skew strategy before client code |
| Microkernel | Kernel stays minimal; plugin contract and sandbox first |
| Space-based | Partition key keeps a transaction in one unit; failover runbook |

## Checks

1. `node scripts/arch-scan.mjs check <dir>`; confirm or dismiss each candidate.
2. The project's test, lint and type-check commands.
3. Domain and use-case tests pass with no database and no network.
4. Use the `super-verify` gate before saying it is done: fresh run, read the output, state what was and was not checked.

## Do not

- Generate every layer for a one-endpoint CRUD feature.
- Import a framework type into the domain or a use case.
- Put business rules in controllers, repositories or consumers.
- Add an interface with a single stable implementation "for flexibility".
- Create a second folder tree beside the existing one.
