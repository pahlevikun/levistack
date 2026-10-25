---
description: "Bound queries, keyset pagination, bulk child reads instead of N+1, and indexes justified by a named query."
alwaysApply: false
---

# Queries and indexes

## Queries
- **Bind every value.** Dynamic identifiers and column names come only from finite source-code allowlists. Never concatenate request input into SQL.
- **Collections return summary projections** with **keyset pagination.** Reject unbounded reads and offset pagination on growing collections.
- **Query count is bounded by operation type, not result count.** Reject query-per-row loops. For several roots, bulk-load each child family with a bound array and group by parent in the data layer.
- Reject one big multi-child join that creates a cartesian fan-out, and root projections with several correlated child aggregates.
- Hydrate children only for rows actually returned, excluding a `limit + 1` probe.
- Compose optional predicates from a closed allowlist. Prefer sargable "present-only" predicates over nullable `OR` forms.
- Aggregate writes use serializable isolation; multi-query aggregate reads use a read-only snapshot. Retry the **whole** transaction on serialization failure, deadlock and bounded lock-timeout errors.
- Keep retryable transaction bodies free of non-transactional external effects unless there is an outbox or an independently idempotent boundary.

## Indexes
Every index proposal names: the exact query, equality columns, any stable partial predicate, range or order columns, the uniqueness invariant, cardinality, overlap with existing indexes, and the write and storage cost.

- Equality columns before range and order columns, with a unique keyset tie-breaker last.
- No index per field. No redundant prefix indexes.

## Evidence
Validate with `EXPLAIN (ANALYZE, BUFFERS)` against representative data in a non-production environment. Do not publish a performance claim without the dataset, query, plan, environment and method.
