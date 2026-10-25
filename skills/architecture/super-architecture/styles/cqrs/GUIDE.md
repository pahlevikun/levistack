# CQRS (command query responsibility segregation)

Use different models for changing state and for reading it. CQRS is a pattern you adopt in steps, not a switch.

## Pick when
- Reads and writes differ sharply in shape, load or scaling (reports versus transactions).
- One application service is wide and hard to reason about because it mixes reads and writes.
- You need several read models for different consumers.

## Avoid when
- Simple CRUD where reads equal writes. It doubles the code for no benefit.
- The team has not yet felt the pain; start at L0.

## Core idea

| | Command side | Query side |
|---|---|---|
| Purpose | Express intent and change state | Return data |
| Model | Normalized, focused on invariants | Shaped for the screen or API |
| Result | Success or failure, not domain data | Data, never changes state |
| Rules | Authorize first; validate; one aggregate per transaction | Can be cached and optimized freely |

## Adoption levels

| Level | Design | Cost | Move up when |
|---|---|---|---|
| L0 | One model, one store | None | Default |
| L1 | Separate command and query services, shared store | Low | One service mixes reads and writes |
| L2 | Separate read store synced by events | Medium | High read volume or special query shapes |
| L3 | Event sourcing with projections | High | Audit, temporal queries, replay (`styles/event-sourcing/GUIDE.md`) |

Prove the value at each level before moving up. Most systems stop at L1. L2 and above fit best with hexagonal or clean structures that already isolate ports. Event sourcing is L3 only; this guide stays on the split of models. For the event store, snapshots and replay, open `styles/event-sourcing/GUIDE.md`.

## Rules
1. A command handler authorizes the caller before acting.
2. A query handler never writes.
3. Strong consistency inside an aggregate; eventual consistency between aggregates and between write and read stores.
4. Write business data and the outbox record in one transaction (no dual write).
5. Event bodies carry ids and facts, never passwords or personal data.
6. Handlers are idempotent.

## Where it lives in each style

| Style | Command side | Query side |
|---|---|---|
| Layered | `application/service/command/` | `application/service/query/` |
| Onion | `core/application/command/` | `core/application/query/` |
| Hexagonal | Command ports | Query ports |
| Clean | Command interactors | Query interactors |
| COLA | `app/command` executors | `app/query` executors |
| Vertical slice | The slice's command handler | The slice's query handler |

## Build steps
1. Split use cases into writes and reads.
2. Give each command and query its own handler, named for intent.
3. L1: keep one store; separate the services and the types they use.
4. L2: publish domain events through an outbox; build projections that update the read store; accept and expose the staleness.
5. Make handlers idempotent (below).
6. Test the command side with domain unit tests, the query side with projection tests against the read store.

## Event delivery and idempotency

| Delivery | Latency | Complexity | Fits |
|---|---|---|---|
| Poll the outbox table | About 1 to 5 s | Low | Small to medium traffic |
| Change data capture on the log | Under about 100 ms | Medium | High traffic and low latency |
| After-commit callback (in process) | Under about 10 ms | Low | In-process handlers only; can lose events on a crash |

| Idempotency strategy | Reliability | Fits |
|---|---|---|
| Processed-event table | High | Money and critical events |
| State-machine guard | High | State-driven events |
| Natural idempotency in the operation | High | Simple operations |
| Cache key with expiry | Medium | Non-critical notifications |

## Read freshness
At L2 and L3, name a **staleness SLA** per read model (for example "under 2 s for checkout, under 30 s for reports"). The command side returns success or failure immediately; the UI does not wait for the projection unless that SLA is "sync." Users who refresh and see old data were not told the rule.

## Pitfalls
Adopting L2 or L3 too early, using CQRS for CRUD, queries that mutate, commands that return rich read data, non-idempotent projections, no versioning of event schemas, no CI gate on an event schema registry, projections without lag metrics.

## Combines with
Any base style, event sourcing (L3), event-driven delivery, vertical slice.
