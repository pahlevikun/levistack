# Event sourcing

Store what happened, not just what is. The sequence of immutable events is the source of truth; current state is derived by replaying them.

## Pick when
- A complete audit trail or compliance history is required.
- You need temporal queries ("what was the state at time T").
- You want several projections from the same history, or the ability to replay and rebuild.
- You are already running CQRS at L2 successfully.

## Avoid when
- There is no audit or temporal need. It adds real operational cost.
- It would be the team's first CQRS step. Never adopt event sourcing as the default.
- Simple CRUD.

## Core idea

| Traditional | Event sourcing |
|---|---|
| Store what IS (`UPDATE users SET email = ...`) | Store what HAPPENED (`UserEmailChanged` appended) |
| History is lost or approximated by audit tables | History is the data |

Pieces: **aggregate** (decides, emits events), **event store** (append-only, per-aggregate streams, optimistic concurrency by version), **projections** (read models built by consuming events), **snapshots** (a cached state at a version to avoid replaying long streams).

## Rules
1. **Events are immutable facts,** named in the past tense (`OrderPlaced`). Never edit or delete a published event; append a corrective event.
2. **Aggregates are the consistency boundary.** Changes inside one are immediately consistent; across aggregates use process managers or sagas with eventual consistency.
3. **Validate commands before emitting events.** The aggregate checks its invariants against current state, then appends.
4. **Version event schemas.** Plan upcasting from the first release.
5. **Handlers and projections are idempotent;** a rebuild must produce the same result.
6. **No sensitive data in events** (secrets, personal data); carry ids and facts.
7. **Aggregates reference each other by id,** never by object.

## Build steps
1. Decide that you need it (audit, temporal, replay). Record the reason in an ADR.
2. Model aggregates and the events that describe their state changes.
3. Implement the event store: stream per aggregate, expected-version append, a global ordering or checkpoint for projections.
4. Implement `apply` for each event so state can be rebuilt by replay.
5. Build projections, each shaped for one query need; make them rebuildable.
6. Add snapshots when stream length makes replay slow, not before.
7. Add process managers or sagas for cross-aggregate workflows, with compensation for failures.
8. Test aggregates as given-events, when-command, then-events; test projections by replaying fixture streams.

## Temporal queries
Reconstruct state at a point in time by replaying events up to that point (from the nearest snapshot). Keep a timestamp and a causation or correlation id on every event.

## Technology
Dedicated stores (for example EventStoreDB) and frameworks (for example Axon) exist; a relational table with `(stream_id, version, type, payload, metadata, created_at)` and a unique constraint on `(stream_id, version)` is a workable start.

## Operations before production
Identify, not merely mention: replay of a stream, rebuild of a projection, snapshot take/restore, and a schema registry (or version policy) that CI uses to block unregistered event versions. Practice a replay in a non-prod environment. Projection lag, sequence gaps and dead-letter depth are dashboard rows, not afterthoughts.

## Pitfalls
Using it for simple CRUD, aggregates that span several consistency boundaries, editing published events, no schema versioning, non-idempotent projections, tight coupling between aggregates, missing validation before emitting events, declaring the write side done with no replay tool.

## Combines with
CQRS L3, event-driven delivery (publish from the store through an outbox or log), hexagonal (the event store is a driven port).
