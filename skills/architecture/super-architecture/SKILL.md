---
name: super-architecture
description: "Detect, choose, build, evaluate, migrate and document software architecture. Use to name the architecture of an existing codebase, pick one for a new system, scaffold or write code in a given style (layered, onion, hexagonal or ports and adapters, clean, COLA, vertical slice, CQRS, event sourcing, event-driven, client-server, domain-driven, functional core, microkernel, microservices, modular monolith, pipeline, serverless, service-based, space-based), check dependency direction and layer violations, plan a strangler-fig migration, or write an ADR or C4 docs. One skill with granular job, style and stack guides; it loads only what the task needs."
when_to_use: "Use when the user asks 'what architecture is this', 'which architecture should we use', 'where does this code belong', 'structure this service', 'is the domain leaking into the framework', 'should we use CQRS or microservices', 'modular monolith or services', 'functional core', 'serverless vs always-on', 'refactor toward hexagonal', 'write an ADR' or 'draw the C4 diagram'; or when scaffolding a new service or feature that needs a structure."
metadata:
  version: "1.1.0"
---

# Super Architecture

One skill, three axes. Call it once. It works out the **job**, then loads only the **style** and **stack** guides that job needs, plus the shared **core** principles.

| Axis | Folder | Answers |
|---|---|---|
| Job | `jobs/` | What are we doing: detect, select, build, evaluate, migrate, document |
| Style | `styles/` | In-process structure, modeling, read/write flow, deployable shape, extensibility |
| Stack | `stacks/` | How it looks in this language and framework, and how to enforce it |
| Core | `core/` | The principles every style shares |

New style, stack or job: add one folder or file and one row in [styles/README.md](styles/README.md) or the matching table below. Nothing else changes.

## Step 0: detect the job and the context

Do this first and do not announce it.

1. **Is there code?** If yes, run `node scripts/arch-scan.mjs detect <dir>` and read its evidence, then open two or three files on the main request path. Never name a style from folder names alone; confirm the dependency direction from imports.
2. **Is it greenfield?** Gather only what is missing: team size and experience, business-rule complexity, stack, how often infrastructure changes, number of entry points (HTTP, CLI, queue, gRPC), test requirements, deployable shape (one process or many), traffic pattern.
3. **Pick the job** from the table, state it in one line, and load its guide.

## Jobs

| The user wants to... | Job | Guide |
|---|---|---|
| Know what architecture exists, where code belongs, find layer violations | detect | [jobs/detect.md](jobs/detect.md) |
| Choose an architecture, CQRS level or service split | select | [jobs/select.md](jobs/select.md) |
| Create a service, feature or scaffold in a style | build | [jobs/build.md](jobs/build.md) |
| Assess health, maturity or debt of an existing design | evaluate | [jobs/evaluate.md](jobs/evaluate.md) |
| Move from one structure to another, or strangle a legacy one | migrate | [jobs/migrate.md](jobs/migrate.md) |
| Write ADRs, C4 diagrams or an architecture blueprint | document | [jobs/document.md](jobs/document.md) |

Common chains: **greenfield** is select, build, document. **Legacy** is detect, evaluate, migrate, then verify. **Review** is detect, then evaluate with a short report.

## Styles

Two independent axes. Pick **one in-process structure**, add **domain-driven** only when the business has a language to model, and pick a **deployable shape** when the unit of deploy matters. Full catalog with grouping: [styles/README.md](styles/README.md).

| Style | Pick when | Avoid when | Guide |
|---|---|---|---|
| Layered (DDD four-layer or n-tier) | Simple domain, small team, moving from three-tier | Swapped infrastructure, dense rules, many entry points | [layered](styles/layered/GUIDE.md) |
| Onion | Domain-centric core, high test coverage, changing infrastructure | CRUD-heavy apps, teams new to abstraction | [onion](styles/onion/GUIDE.md) |
| Hexagonal (ports and adapters) | Several entry points, volatile integrations, complex rules, TDD | Tiny single-entry CRUD, throwaway prototypes | [hexagonal](styles/hexagonal/GUIDE.md) |
| Clean | Large teams, strict module isolation, long-lived systems | Small teams, quick MVPs | [clean](styles/clean/GUIDE.md) |
| COLA (diamond) | Java and Spring Boot enterprise teams that want scaffolding and a validator | Non-Java stacks | [cola](styles/cola/GUIDE.md) |
| Vertical slice | Feature-heavy products where change should stay in one place | A tiny script, or heavy shared domain logic across all features | [vertical-slice](styles/vertical-slice/GUIDE.md) |
| Functional core | Rules tangled with I/O; you want pure, fast tests | Measured immutability cost, no appetite for the split | [functional-core](styles/functional-core/GUIDE.md) |
| Domain-driven | Real rules a domain expert can argue about; composes with a structure | CRUD over a form; no business vocabulary | [domain-driven](styles/domain-driven/GUIDE.md) |
| CQRS | Read and write needs differ sharply | Simple CRUD where reads equal writes | [cqrs](styles/cqrs/GUIDE.md) |
| Event sourcing | Audit trail, temporal queries, replay | No audit need, first CQRS attempt | [event-sourcing](styles/event-sourcing/GUIDE.md) |
| Event-driven | Decoupled services, async workflows, streaming | A single process with simple call chains | [event-driven](styles/event-driven/GUIDE.md) |
| Pipeline | ETL, streaming analytics, isolated transform stages | Interactive request/response, shared mutable state | [pipeline](styles/pipeline/GUIDE.md) |
| Client-server | UI and logic across a network trust boundary | One process, no contract to version | [client-server](styles/client-server/GUIDE.md) |
| Modular monolith | Team autonomy without distributed operations | Tiny apps, or already independently deployed services | [modular-monolith](styles/modular-monolith/GUIDE.md) |
| Service-based | Few coarse deployables; shared DB still realistic | One team; or full data autonomy already funded | [service-based](styles/service-based/GUIDE.md) |
| Microservices | Independent deploy and scale; platform already funded | Small team, no SRE, strong cross-cut consistency | [microservices](styles/microservices/GUIDE.md) |
| Serverless | Bursty event work; pay-per-execution | Long-running, sticky state, tight cold-start SLO | [serverless](styles/serverless/GUIDE.md) |
| Space-based | One database cannot hold the traffic | Low traffic; strong cross-partition consistency | [space-based](styles/space-based/GUIDE.md) |
| Plugin and extension | Third parties or other teams extend a stable host | A closed application | [plugin](styles/plugin/GUIDE.md) |
| Microkernel | Minimal kernel, sandboxed versioned plugins | Closed app, or all features must be core | [microkernel](styles/microkernel/GUIDE.md) |
| Game and real-time | State machines, pooling, event buses, data-driven content | Ordinary request/response services | [game](styles/game/GUIDE.md) |

Styles combine. A typical modern service is hexagonal or vertical-slice at the top level, with CQRS inside the slices that need it, inside a modular monolith or a single process. Each guide has a "Combines with" section.

## Stacks

| Stack | Guide |
|---|---|
| TypeScript and Node | [stacks/typescript.md](stacks/typescript.md) |
| Java and Kotlin (Spring) | [stacks/java-kotlin.md](stacks/java-kotlin.md) |
| Go | [stacks/go.md](stacks/go.md) |
| PHP (Symfony) | [stacks/php.md](stacks/php.md) |
| .NET | [stacks/dotnet.md](stacks/dotnet.md) |
| Python | [stacks/python.md](stacks/python.md) |
| Dart and Flutter | [stacks/dart-flutter.md](stacks/dart-flutter.md) |

## Core principles

Load the matching file when a job needs more than the summary here.

| Topic | File |
|---|---|
| Dependency direction, ports, composition root, crossing boundaries | [core/dependency-rule.md](core/dependency-rule.md) |
| Right-sizing: simple by default, thresholds to upgrade | [core/right-sizing.md](core/right-sizing.md) |
| Entities, value objects, aggregates, bounded contexts | [core/domain-modeling.md](core/domain-modeling.md) |
| Components, cohesion and coupling, humble objects | [core/components-and-boundaries.md](core/components-and-boundaries.md) |
| Naming, folder layout, screaming structure | [core/naming-and-layout.md](core/naming-and-layout.md) |
| Testing per layer and architecture tests | [core/testing-architecture.md](core/testing-architecture.md) |
| Quality attributes, trade-offs, system design | [core/quality-attributes.md](core/quality-attributes.md) |
| Anti-pattern catalog with symptoms and fixes | [core/anti-patterns.md](core/anti-patterns.md) |

## Rules that hold in every style

1. **Follow the project first.** Detect before prescribing. Do not rewrite a working structure to match a favorite pattern; move one slice at a time.
2. **Right-size.** Use the simplest structure that keeps the rules intact. Upgrade when a measurable pain appears, not in anticipation.
3. **Dependencies point inward.** The inside defines the abstractions it needs; the outside implements them.
4. **The core knows no framework.** Domain and use-case code import no web, ORM, queue or SDK types. Adapters stay thin. One composition root wires everything.
5. **Name business intent.** `PlaceOrder`, not `updateOrder`. Folders should show what the system does before they show what it is built with.
6. **One aggregate per transaction.** Inside an aggregate, consistency is immediate. Between aggregates, use IDs and events.
7. **Abstract only where it pays.** A port needs volatility, a test seam or a team boundary. Share code only after two real consumers prove identical meaning.
8. **Make claims checkable.** Back structure with scan output, architecture tests and diagrams derived from the code, each with file paths.
9. **Record the decision with its trade-off,** using [templates/adr.md](templates/adr.md).
10. **Verify before claiming.** Use the `super-verify` gate: run the scan and tests, read the output, then say what holds.

## Output by job

Detect returns a style, a confidence, evidence with paths, deviations and violation candidates. Select returns one recommendation, its reasons, what would change it, and an ADR. Build returns the structure and code plus the check that proves the boundaries hold. Evaluate returns a scored report and a prioritized roadmap. Migrate returns phases, a rollback path and the first slice. Document returns diagrams and records grounded in paths.

## Done when

- The job, style and stack were named, and only the guides they need were opened.
- Recommendations fit the detected project, or state why they deviate.
- Dependency direction was checked with `scripts/arch-scan.mjs check` or an architecture test, and the result was read.
- Any decision is recorded with its trade-off, and any claim names the file it came from.
