# Domain: database

SQL, ORM queries, migrations, indexes, transactions, and data access in application code.

## Checklist

- [ ] No unbounded reads or N+1 without explicit pagination/batching intent (R-03).
- [ ] Migrations reversible when the repo requires it; locks and indexes follow production patterns.
- [ ] Fixtures and seed data labeled synthetic — not plausible production IDs (R-18).
- [ ] Transactions scope real units of work — not ceremony around a single row.
- [ ] Query layers exist for this product's access patterns — not a generic repository per table by default (R-01, R-31).
- [ ] Timeouts and connection limits on hot paths where siblings use them (R-27).

## MR review signals

N+1, missing pagination, migration risk — dimension `perf` plus noslop tutorial layering on data access.
