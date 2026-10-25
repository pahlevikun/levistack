# Source playbooks

`trace` sends one investigator per evidence category, and each investigator reads one playbook for the tool it owns. The playbooks are worked examples. Adapt one to a different tool in the same category.

| # | Category | Playbook | Tools it covers |
|---|---|---|---|
| 1 | Source control | `sources/code-archaeology.md` | git, `gh`, in-repo artifacts |
| 1 | Source control | `sources/git-history.md` | commit forensics: blame through moves, pickaxe, `log -L`, tags, bisect |
| 1 | Source control | `sources/github-pr.md` | GitHub PRs, reviews, line comments, issues |
| 1 | Source control | `sources/gitlab-mr.md` | GitLab MRs, discussions, versions, pipelines, issues |
| 2 | Issue or ticket tracker | `sources/jira.md` | Jira (also Jira Service Management) |
| 2 | Issue or ticket tracker | `sources/linear.md` | Linear (adapt for GitHub Issues, Plane, Shortcut) |
| 3 | Long-form documents | `sources/docs.md` | Confluence, Google Docs and Drive, SharePoint, Coda, markdown vaults, PDFs |
| 3 | Long-form documents | `sources/notion.md` | Notion |
| 3 | Long-form documents | `sources/inline-docs.md` | comments, READMEs, CHANGELOG, ADRs, contracts, tests, runbooks in the repo |
| 4 | Real-time team chat | `sources/slack.md` | Slack (adapt for Discord, Teams, Mattermost) |
| 4 | Real-time team chat | `sources/lark.md` | Lark or Feishu chat, Docs, Wiki, Sheets, Base, approvals |
| 5 | Infrastructure observability | `sources/datadog.md` | Datadog (adapt for New Relic, Honeycomb, Splunk) |
| 5 | Infrastructure observability | `sources/grafana.md` | Grafana with Prometheus, Loki, Tempo or other data sources |
| 5 | Infrastructure observability | `sources/logs.md` | Elasticsearch, OpenSearch, Kibana, Loki, cloud logging |
| 6 | Error or exception tracking | `sources/sentry.md` | Sentry (adapt for Rollbar, Bugsnag, Airbrake) |
| 7 | Product analytics warehouse | `sources/databricks.md` | Databricks SQL |
| 7 | Product analytics warehouse | `sources/data-warehouse.md` | BigQuery, Snowflake, Redshift, ClickHouse, MaxCompute, dbt |
| 8 | Deploy and CI history | `sources/ci-cd.md` | GitHub Actions, GitLab CI, Jenkins, Argo CD, release tags |
| 9 | Runtime platform | `sources/kubernetes.md` | kubectl, Lens, k9s |
| 9 | Runtime platform | `sources/config-and-flags.md` | feature-flag services, Consul, cloud config stores, config repos |
| 10 | Live data (read-only, ask first) | `sources/databases.md` | PostgreSQL, MySQL, MongoDB, Redis and similar |
| 10 | Live data (read-only, ask first) | `sources/event-streams.md` | Kafka, RabbitMQ, Pub/Sub, SQS, job queues |
| 10 | Live data (read-only, ask first) | `sources/api-probes.md` | read-only `GET` calls to running services |
| 11 | Customers and support | `sources/support-and-crm.md` | Zendesk, Freshdesk, Intercom, Salesforce, support queues in Lark Base, CSV exports |

Cross-cutting:

- `sources/incident-postmortem.md`. Add it when the target looks defensive, and always in root-cause mode.

## Rules for every source

- Read-only. No writes, posts, purges, offset resets or config changes.
- Categories 9 and 10 touch running systems: confirm the environment and ask the user before you query production.
- Mask personal data and never print secrets (`rules/core/pii-logging.md`).
- If a tool needs auth and auth fails, stop and report the gap. Never invent findings.
