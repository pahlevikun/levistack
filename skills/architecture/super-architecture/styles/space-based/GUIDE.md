# Space-based

Scale by adding identical **processing units**, each with an in-memory partitioned data grid. The database is no longer on the request path for the hot state. Used when one node cannot hold the traffic or the latency budget.

## Pick when
- Traffic or working set overwhelms a single database node.
- Latency needs memory-local data next to compute.
- You can partition work so units are self-sufficient, and you will operate a grid (replication, failover, cost).

## Avoid when
- Low traffic; a cache in front of a database is enough.
- Strong, cross-partition consistency matters more than availability.
- The team cannot yet run clustering, split-brain recovery and reconciliation.

## Core idea

Incoming work is routed to a unit that owns that partition. Units keep state in a **replicated in-memory grid**. Durability is write-through or write-behind to a store, plus a reconciliation job. Node loss is handled by replica promotion or leader election, not by "the DB will save us" on the hot path.

Eventual consistency between partitions is the default. Document freshness SLAs.

## Layout

```
processing-unit/          stateless-looking worker + local grid node
grid/                     partition scheme, replication, eviction
persistence/              write-through / write-behind, reconciliation
routing/                  partition-aware load balancing
```

## Build steps
1. Choose a partition key that keeps a business transaction inside one unit.
2. Pick grid technology, sync versus async replication, and eviction policy. Write them in the ADR with a durability SLA.
3. Implement write-through (safer, slower) or write-behind (faster, needs reconciliation and loss budget).
4. Failover: heartbeats, leader election, split-brain runbook, exercised in a non-prod environment.
5. Load and chaos test at least about twice expected peak; no acknowledged loss on a single node kill.
6. Monitor cache hit rate, replication lag, failover events, and memory cost; autoscale units from those signals.

## Testing
- Unit tests of routing and partition assignment.
- Grid tests: replica lag, eviction, concurrent writes to one key.
- Chaos: kill a unit, partition the network, assert the runbook.
- Reconciliation: compare grid to durable store after a write-behind burst.

## Pitfalls
A partition key that splits a transaction across units. Treating async replication as strong consistency. No split-brain runbook. Unbounded memory (no eviction). Cost surprise from always-hot RAM. Using this as a generic cache for a CRUD app.

## Combines with
Event-driven (units consume partitions of a log), CQRS (grid as the hot read model), microservices (a service's hotspot becomes a grid), hexagonal (grid and store behind ports).
