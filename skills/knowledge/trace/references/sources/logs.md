# Logs

Logs say what the system did at each moment. They are the best evidence for Why 1 in a root-cause chain.

## Where they live

| Store | Reach it with |
|---|---|
| Elasticsearch, OpenSearch, Kibana | their MCP server, the Kibana UI, or the `_search` API with a read-only query |
| Grafana Loki | `grafana.md`, or `logcli` |
| Cloud logging (Google Cloud Logging, AWS CloudWatch, Azure Monitor, Tencent CLS) | the provider CLI (`gcloud logging read`, `aws logs filter-log-events`) or its MCP server |
| Datadog, New Relic | `datadog.md`, or their MCP server |
| Kubernetes pods | `kubernetes.md` (`kubectl logs`) for recent logs only |

## How to search it

1. **Bound the time** around the first-seen time. Start narrow, then widen.
2. **Search by the most specific key first**: a trace id or request id, then an entity id, then the exact error string, then the service and level.
3. **Follow one request end to end** with its trace or request id across services.
4. **Count before you read.** Group by error message or by host to see if it is one bad node or everywhere.
5. **Find the first occurrence.** The first error after a quiet period often names the real cause. Later errors are often its side effects.

## What good evidence looks like

- The first error line, with its time, host, and the request id
- A log line that shows the bad input or the bad state right before the failure
- A count that jumps at a deploy time

## Pitfalls

- **Retention.** Old logs are gone. Note the retention cliff when the window is older.
- **Sampling.** Some systems keep only a sample. A missing line is not proof it did not happen.
- **Personal data.** Logs can hold ids, emails or tokens. Quote only what the question needs, and mask the rest (`rules/core/pii-logging.md`).
- **Cost.** Wide queries on big stores are slow and can cost money. Bound the time and the index first.

## What to return

The store, the exact query, the time window in UTC, the first relevant line quoted (masked), counts that matter, and the trace or request ids you followed.
