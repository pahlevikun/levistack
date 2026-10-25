---
description: "Ecto and PostgreSQL in Elixir: sandboxed tests, bound raw SQL, transaction retries, reversible migrations."
globs: "**/*.{ex,exs},**/migrations/**"
alwaysApply: false
---

# Ecto and PostgreSQL

Builds on `queries-and-indexes` and `migrations-and-soft-delete`.

- **The database is authoritative.** Tests run against a real database through the SQL sandbox, on the same engine and version as production. Do not mock the Repo.
- **Constraints agree in both layers.** Review the migration and the schema or changeset together. A new field, index or constraint is incomplete until both match.
- **Raw SQL**, where used (`Ecto.Adapters.SQL.query/4`): bind every request-derived value; take dynamic identifiers and assignment columns only from finite source-code allowlists; add explicit casts for nullable or ambiguous placeholders; return domain values, not `%Postgrex.Result{}`; keep it inside the data app; disable parameter logging.
- **Data accepts validated structs or atom-keyed attributes**, never arbitrary request maps.
- **Transactions.** Aggregate writes use serializable isolation; multi-query aggregate reads use a read-only repeatable-read snapshot. Retry the **whole** transaction on SQLSTATE `40001`, `40P01` and bounded `55P03`. Carry optimistic lock versions through update commands. Keep retryable callbacks free of non-transactional external effects unless an outbox or an independently idempotent boundary exists.
- **Expected database failures** (unique, foreign key, check) become tagged domain errors, not exceptions at the edge.
- **Migrations** are reversible, use the default migration lock, and are validated against the pinned database image. Staging and production require verified TLS.
- **Engine-specific notes** (for example CockroachDB: no DDL in a transaction, so `@disable_ddl_transaction true`; no enum types, use CHECK constraints; computed columns through raw SQL) belong in the project's own database guide. Follow it rather than assuming PostgreSQL behavior.
- **IDs:** prefer UUID primary keys unless a library dictates otherwise. Do not add a serial key without a specific reason.
