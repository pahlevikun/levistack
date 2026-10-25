# Grafana

Grafana shows data from other systems. Find out which data source each panel uses (Prometheus, Loki, Tempo, Elasticsearch, a SQL database, a cloud monitor), because the evidence is the query, not the picture.

## What this source holds

- Dashboards and panels with metrics over time: latency, error rate, saturation, queue depth
- **Annotations**: deploys, incidents and manual notes on the timeline
- Alert rules, their thresholds, and their firing history
- Explore: ad-hoc queries on the same data sources
- Dashboard version history: who changed a panel or a threshold, and when

## How to search it

Use the Grafana MCP server if one is connected, or the HTTP API with the user's token (read-only calls).

1. **Find the dashboard** for the service: search by service name or tag (`GET /api/search?query=<service>`).
2. **Set the window** around the first-seen time, with room before it (for example 2 hours before to 1 hour after).
3. **Read the annotations** in that window. A deploy marker right before a change in a graph is a strong lead for the timeline check.
4. **Get the query behind each panel**, and re-run it in Explore for the exact numbers. Cite the query, not "the graph went up".
5. **Check the alert rule history** (`GET /api/v1/provisioning/alert-rules`, the alert state history). A threshold changed by hand can explain "why didn't it page".
6. **Check the dashboard version history** when a number "changed" but the system did not.

## What good evidence looks like

- A step change in a metric that starts within minutes of a deploy annotation
- An alert that fired, with its threshold and the time
- A saturation metric (CPU, connections, queue depth) hitting a limit right before errors rise

## Pitfalls

- **Rate and resolution.** A wide time range averages spikes away. Narrow the window, or use a max or a percentile.
- **Missing data looks like zero.** Check for gaps, not only values.
- **Time zones.** Grafana shows the browser's zone. Write every time in UTC with the zone named.
- **Correlation is not cause.** Two lines moving together is a lead. The cause chain still needs the mechanism.

## What to return

Dashboard and panel name, the data source and the exact query, the time window in UTC, the key numbers, and any annotations or alert firings in the window.
