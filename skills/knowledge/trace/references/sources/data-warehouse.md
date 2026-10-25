# Data warehouse

For "where did this number come from", "how many users were hit", and the data behind flags and experiments. Use with `databricks.md`, which has a worked Databricks playbook.

## Where it lives

BigQuery, Snowflake, Redshift, Databricks, ClickHouse, Alibaba MaxCompute (ODPS), Athena, Trino or Presto, and dbt models on top of them. Reach each one with its MCP server or its CLI (`bq`, `snowsql`, `odpscmd`, `clickhouse-client`).

## How to search it

1. **Find the table first.** Search the catalog or the dbt models for the entity or event name. Read the model's SQL and docs: they say how a metric is defined.
2. **Filter by partition and time.** Always put the date partition in the `WHERE` clause. A full scan is slow and can cost real money.
3. **Count, then sample.** Start with `COUNT(*)` and `GROUP BY` the dimension that matters (day, version, region). Pull a few rows only when you need an example.
4. **Find first and last seen.** `MIN(event_time)` and `MAX(event_time)` for the bad state give the timeline check its dates.
5. **Compare before and after** a deploy or a flag change with the same query on both windows.

## What good evidence looks like

- A count of affected records per day that starts on the deploy date
- A metric definition in a dbt model that explains an odd threshold
- An experiment table that shows the variant a flag was set from

## Pitfalls

- **Cost.** Estimate first where the tool allows it (`bq query --dry_run`). Ask the user before a large scan.
- **Late data.** Warehouses lag hours or a day behind production. Say the freshness.
- **Definitions drift.** The same metric name can mean different things in two models. Cite the model.
- **Personal data.** Return counts and masked ids, not raw rows with names or contacts.

## What to return

The table or model, the exact SQL, the time window, the freshness, and the numbers that bear on the question.
