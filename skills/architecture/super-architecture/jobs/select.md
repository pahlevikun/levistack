# Job: select

Choose an architecture for a new system or a new module, with one recommendation and the reasons. The matrix and thresholds below are heuristics from common practice; present them as such and let project facts override them.

## Contents
- Procedure
- Context to collect
- Scenario router
- Two axes
- Decision matrix (in-process)
- Deployable shape
- Decision tree
- Team size
- Subdomain classification
- CQRS level
- Service boundaries
- Recommendation format

## Procedure

1. **Collect context** (next section). Ask only for what is missing.
2. **Right-size first.** Read `core/right-sizing.md`. If the honest answer is "the simple thing", say so.
3. **Rank the quality attributes** that matter (`core/quality-attributes.md`).
4. **Split the choice into axes:** in-process structure, modeling (DDD or not), deployable shape, then CQRS/events if reads or workflows demand it.
5. **Score the in-process candidates** with the matrix on at least five dimensions.
6. **Walk the decision tree** and check team size and the scenario router.
7. **Classify subdomains** and give each the lightest style that fits.
8. **Choose a CQRS level** and service boundaries if relevant.
9. **Recommend one option,** with reasons, costs, what would change the answer, and write an ADR (`templates/selection-record.md`, then `templates/adr.md`).

Domain-driven design answers "what do we call things." It **composes** with a structural style. Selecting it does not deselect hexagonal, layered or a modular monolith. Skip it when the domain is CRUD over a form.

## Context to collect

- Team size and experience with domain-driven design and abstraction.
- Business-rule complexity: simple CRUD, moderate, dense and volatile.
- Stack and framework.
- How often infrastructure changes (database, broker, third-party APIs).
- Entry points: one HTTP API, or HTTP plus CLI plus queue plus gRPC.
- Testing expectations and audit or compliance needs.
- Read versus write load, and the expected growth.
- Deployable constraints: one process, several coarse services, bursty traffic, or a single database already at its ceiling.
- Whether a network trust boundary (web/mobile client vs API) exists.

## Scenario router

| Situation | Lean toward | Then load |
|---|---|---|
| Simple CRUD, small team | Layered | `styles/layered/GUIDE.md` |
| Several entry points or volatile infra | Hexagonal | `styles/hexagonal/GUIDE.md` |
| Rules tangled with I/O; tests are slow | Functional core | `styles/functional-core/GUIDE.md` |
| Rich language, experts to talk to | Domain-driven **plus** a structure | `styles/domain-driven/GUIDE.md` |
| Feature teams, change should stay local | Vertical slice | `styles/vertical-slice/GUIDE.md` |
| Many teams, one process still fine | Modular monolith | `styles/modular-monolith/GUIDE.md` |
| Few coarse deploys, shared DB realistic | Service-based | `styles/service-based/GUIDE.md` |
| Independent deploy and scale; platform funded | Microservices | `styles/microservices/GUIDE.md` |
| Bursty event work, pay-per-execution | Serverless | `styles/serverless/GUIDE.md` |
| ETL / streaming transforms | Pipeline | `styles/pipeline/GUIDE.md` |
| Reads and writes differ sharply | CQRS (not automatically event sourcing) | `styles/cqrs/GUIDE.md` |
| Audit, temporal query, replay | Event sourcing (after CQRS L2) | `styles/event-sourcing/GUIDE.md` |
| Async fan-out, decoupled modules | Event-driven | `styles/event-driven/GUIDE.md` |
| One DB cannot hold the traffic | Space-based | `styles/space-based/GUIDE.md` |
| UI across a network trust boundary | Client-server | `styles/client-server/GUIDE.md` |
| Third parties extend a stable core | Microkernel (or plugin for a host pack) | `styles/microkernel/GUIDE.md` |
| Unsure | Layered or vertical slice, clean dependency direction | `jobs/migrate.md` |

## Two axes

| Axis | Question | Typical picks |
|---|---|---|
| In-process structure | Where does a line of code live? | Layered, onion, hexagonal, clean, COLA, vertical slice, functional-core |
| Modeling | What do we call things? | None, or domain-driven |
| Deployable shape | What ships together? | One process, modular monolith, service-based, microservices, serverless, space-based |
| Flow | How do writes, reads and reactions travel? | CRUD, CQRS L1–L3, event-driven, pipeline |

A normal recommendation names one cell from each axis that applies, not four competing "the" architectures.

## Decision matrix (in-process)

Ratings are relative (low, medium, high) and indicative.

| Dimension | Layered | Onion | Hexagonal | Clean | COLA | Vertical slice | Functional core |
|---|---|---|---|---|---|---|---|
| Learning cost | Low | Medium | Medium | Medium-high | Medium | Low-medium | Medium |
| Fit for dense business rules | Low | High | High | High | High | Medium-high | High |
| CRUD efficiency | High | Low | Low | Low | Medium | High | Low |
| Infrastructure replaceability | Low | High | High | High | Medium | Medium | High (shell) |
| Test friendliness | Low | High | High | High | High | High (via entry point) | High (pure core) |
| Feature isolation | Low | Low | Medium | Medium | Medium | High | Medium |
| Module isolation by build | Low | Medium | Medium | High | High | Medium | Medium |
| Typical team size | 1 to 5 | 5 to 15 | 5 to 15 | 15 to 50 | 5 to 50 | any | any |
| Best for | Simple CRUD, small teams | Domain-centric apps with changing infrastructure | Multi-entry systems, complex rules | Large enterprise isolation | Java and Spring teams | Feature-heavy products | Rules currently stuck in I/O |

COLA is Java-specific; do not recommend it outside Java and Spring.

## Deployable shape

| Shape | Cost to operate | Autonomy | Pick when | Avoid when |
|---|---|---|---|---|
| One process (layered / hexagonal / …) | Lowest | Shared release | Default | Teams or scale already collide |
| Modular monolith | Low | Code ownership, one deploy | Several teams, one ops story | Tiny app; or you already ship N services |
| Service-based | Medium | Independent deploys, shared DB possible | Coarse cuts; full data autonomy not ready | One team; hop-sensitive path |
| Microservices | High | Independent deploy and scale | Contexts, data and platform are real | No SRE; strong cross-service transactions |
| Serverless | Medium (bills + IAM) | Per-function scale-to-zero | Bursty, short, event-triggered work | Long jobs, sticky state, harsh cold-start SLO |
| Space-based | Highest | Linear scale of units | One database is the ceiling | Low traffic; strong cross-partition consistency |

Do not recommend microservices as a structure for a five-person team. Do not recommend space-based as a cache for CRUD.

## Decision tree

1. **Business complexity.** Mostly CRUD: layered or vertical slice. Moderate: layered DDD, onion or vertical slice. Dense and volatile: hexagonal, clean, onion or functional-core with a rich domain.
2. **Entry points.** Several (HTTP, CLI, queue, gRPC) pushes to hexagonal.
3. **Infrastructure volatility.** High volatility pushes to hexagonal, onion or functional-core.
4. **Feature velocity with many parallel changes.** Pushes to vertical slice.
5. **Team and stack.** Java with Spring and an enterprise standard: consider COLA. Strict module isolation across a large organization: clean. Several teams, one process: modular monolith.
6. **Deploy and scale.** Cadence or scale diverge and data can be owned: services. Bursty and short: serverless. Database is the bottleneck and partitions are natural: space-based.
7. **Network boundary.** Web or mobile client: client-server contracts and version skew on top of the server style.
8. **Unsure.** Start with a layered or vertical-slice shape and a clean dependency direction, and evolve (see `jobs/migrate.md`).

## Team size

| Team | Lean toward | Why |
|---|---|---|
| 1 to 5 | Layered, simple vertical slice, functional-core if tests hurt | Lowest ceremony, fastest delivery |
| 5 to 15 | Hexagonal, onion, vertical slice, modular monolith, single-module COLA | Balance abstraction and speed |
| 15 to 50 | Clean, multi-module COLA, modular monolith or service-based | Physical isolation, parallel work |
| 50 and up | Independent services (or space-based where the data grid is the product), each with its own fitting style | Autonomous teams and deploys |

Architecture can grow with the team: layered, then hexagonal, then modular, then coarse services, then independently deployed contexts.

## Subdomain classification

Core domain: rich model with hexagonal, clean or functional-core, and domain-driven language. Supporting: layered or CRUD. Generic: buy, reuse or wrap in an adapter. Do not give generic or supporting subdomains the heavy style (`core/domain-modeling.md`).

## CQRS level

| Level | What | Cost | Use when |
|---|---|---|---|
| L0 | One model, one store | None | Reads and writes look alike |
| L1 | Separate command and query services, shared store | Low | One service mixes reads and writes and is hard to reason about |
| L2 | Separate read store, synced by events | Medium | High read volume or complex query shapes |
| L3 | Event sourcing with projections | High | Audit trail, temporal queries, replay |

Start at L0 and prove the need for each step. Never recommend event sourcing as a default. See `styles/cqrs/GUIDE.md` and `styles/event-sourcing/GUIDE.md` as two guides, not one.

## Service boundaries

- Default: one bounded context, one deployable. Start with fewer services and split when a real need appears.
- Split when deploy cadence, scaling profile or team ownership differ **and** data can be owned.
- Merge when strong transactional consistency is needed, the context is small, or one team owns both.
- Use events for eventual consistency between services; synchronous calls only where strong consistency is required, and rarely.
- Service-based (shared DB, explicit schema owners) is a valid stop between modular monolith and microservices. Do not skip it by renaming modules "services."

## Recommendation format

```
Recommendation: <in-process style, plus modeling, deployable shape, CQRS level>
Because: <3 to 5 reasons tied to the collected context>
Costs: <what we give up>
Would change if: <the facts that would flip the choice>
First step: <the first slice to build>
Record: <ADR path>
```
