# Event-driven architecture (outbox, sagas, Kafka)

Components communicate by publishing facts that others react to, instead of calling each other directly. This guide covers the reliability patterns that make it safe and the design of a Kafka-style streaming platform.

## Pick when
- Services or modules must be decoupled in time and ownership.
- Workflows span several aggregates or services and tolerate eventual consistency.
- Streaming, fan-out to many consumers, or replay of history is valuable.
- Reads and writes scale differently (see CQRS L2).

## Avoid when
- A single process with simple call chains, or flows that need immediate consistency across steps.
- The team cannot yet operate a broker. A broker is infrastructure with its own failure modes.

## Topology
For each flow, pick **choreography** (publish and let subscribers react) or **orchestration** (a saga or process manager issues the next command). Choreography extends easily and hides the whole story; orchestration makes the story visible and concentrates failure handling. Do not mix both on the same workflow.

## Reliability patterns

| Pattern | Problem it solves | How |
|---|---|---|
| **Outbox** | Database change and event publish must succeed together | Write the event row in the same transaction as the state change; a relay publishes it and marks it sent |
| **Idempotent consumer** | At-least-once delivery redelivers messages | Processed-id table, state-machine guard, or naturally idempotent operations |
| **Saga** | A business flow across several services without a distributed transaction | A sequence of local transactions, each with a compensating action; orchestrated by a coordinator or choreographed by events |
| **Dead-letter queue** | A poison message blocks a partition | After bounded retries with backoff, park the message with context for review |
| **Process manager** | Coordinate several aggregates | A stateful handler that reacts to events and issues commands |
| **Anticorruption layer** | Foreign event shapes leak into your model | Translate at the consumer edge |

Aggregates stay consistent inside; between aggregates and services, accept eventual consistency and design for it explicitly (reads that may be stale, compensation instead of rollback).

## Event design
- Name events in the past tense (`OrderPlaced`). Carry ids and the facts needed; keep secrets and personal data out.
- Use a stable envelope: id, type, version, occurred-at, correlation id, causation id, payload.
- Version schemas and keep consumers tolerant of unknown fields. Evolve with backward compatible changes; a schema registry with compatibility checks helps.
- Distinguish **events** (facts already happened) from **commands** (requests that can be rejected). Do not publish commands as events.

## Kafka design

Work one component at a time, in this order: topics, partition strategy, consumer groups, event patterns, data modeling. Large designs go wrong when everything is decided at once.

**Cluster.** Brokers store and serve data; a controller (an elected broker) manages partition leaders and replica assignment and is re-elected on failure. Small deployments run about 3 to 10 brokers. New clusters should use KRaft mode rather than ZooKeeper. Spread replicas across racks or zones.

**Topics.** One topic per event type or per aggregate stream, named `<domain>.<entity>.<event>` or the project's convention. Choose retention by how long consumers may lag or replay. Use log compaction for "latest value per key" topics.

**Partitions and keys.** Ordering is guaranteed only within a partition, so key messages by the entity whose order matters (for example the order id). Size partitions from throughput: partitions at least the larger of (target throughput divided by what one producer partition sustains) and (target throughput divided by what one consumer sustains), with headroom. Partitions can be added later but not removed, and adding them changes key-to-partition mapping.

**Durability.** Replication factor 3, `min.insync.replicas` 2, producer `acks=all` with idempotence on, unclean leader election off. This trades a little latency for no acknowledged-write loss on a single failure.

**Consumers.** A partition is consumed by at most one consumer in a group, so consumers beyond the partition count idle. Commit offsets after processing. Make processing idempotent. Monitor lag per partition. Handle rebalances without losing in-flight work.

**Data modeling.** Decide between event streams (immutable facts), changelog topics (state by key) and command topics. Keep payloads small; reference large data by id.

## Build steps
1. State why events are needed here and which flows need eventual consistency.
2. Define the events and their ownership: one producer context per event type.
3. Add an outbox to each producer; run a relay.
4. Make every consumer idempotent and add retry with backoff and a dead-letter path.
5. Design broker resources: topics, partitions, keys, retention, replication.
6. Define schemas and compatibility rules.
7. Add observability: lag, error rate, dead-letter depth, end-to-end latency.
8. Test with the broker in a container, including duplicate delivery and out-of-order cases.

## Hidden coupling
Consumers that depend on undocumented fields couple the system through the payload. Publish an event catalog or schema registry; lint payloads; add consumer-driven contract tests. Time-box discovery workshops to the highest-value contexts first so modeling does not replace shipping.

Trace every hop with a correlation id. Dashboards: consumer lag, throughput, schema validation failures, DLQ depth. A consumer without a DLQ and a retry policy is not ready to deploy.

## Pitfalls
Dual writes, non-idempotent consumers, commands disguised as events, giant events carrying whole aggregates, no schema versioning, using one partition for everything, assuming global ordering, treating the broker as a database of record without a retention plan, choreography so implicit nobody can draw the flow.

## Combines with
CQRS L2 (projections via events), event sourcing, hexagonal (the broker client is an adapter behind a port), vertical slice (slices react to events).
