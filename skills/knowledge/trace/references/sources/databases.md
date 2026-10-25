# Databases (read-only)

The actual state of the data: what a record looks like now, when it changed, how many records are in a bad state.

**Ask the user before any query against a production database.** Read-only queries only, on a read replica when there is one.

## Where it lives

PostgreSQL, MySQL, MongoDB, Redis, DynamoDB, Cassandra, and their managed versions. Reach them with the client the user already uses (`psql`, `mysql`, `mongosh`, `redis-cli`) or an MCP server, with read-only credentials.

## How to search it

1. **Confirm the target**: host, database, replica or primary, and that the user is fine with the query.
2. **Count first.** `SELECT COUNT(*) … WHERE <bad state>`, or `db.<coll>.countDocuments({…})`, before pulling rows.
3. **Always limit.** `LIMIT 20`, `.limit(20)`. Select only the columns you need.
4. **Look for history columns**: `created_at`, `updated_at`, `deleted_at`, version fields, audit tables. They give the timeline.
5. **Check the plan** for slow-query questions: `EXPLAIN` (or `EXPLAIN ANALYZE` only on a replica, since it runs the query).

Never run `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, a migration, or a Redis write command (`SET`, `DEL`, `FLUSH*`). If the fix needs a write, hand it to the user as text.

## What good evidence looks like

- A count of records in the bad state, grouped by the day they were created
- An `updated_at` that matches a deploy or a job run
- An `EXPLAIN` with a full scan on a large table

## Pitfalls

- **Personal data.** Return counts and masked ids. Never paste names, emails, phone numbers or tokens.
- **Load.** A heavy query on the primary can hurt production. Use the replica, and limit everything.
- **Replication lag.** A replica can be seconds or minutes behind. Say so.

## What to return

Target (host, database, replica or primary), the exact query, the row counts, masked sample ids, and the timestamps that matter.
