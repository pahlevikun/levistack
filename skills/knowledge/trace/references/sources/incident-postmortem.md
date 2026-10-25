# Incident and postmortem context

Add this to every investigator's prompt when the target looks defensive (null checks, retries, timeouts, rate limits, feature flags, egress guards, OOM handlers), and always in root-cause mode. Each investigator runs the incident-flavored search inside its own source.

| Source | Incident search |
|---|---|
| Git | Commit messages like "fix for incident", "hotfix", "add defensive check", "revert", then "re-apply with…" |
| GitHub, GitLab | PRs or MRs labeled `incident`, `hotfix`, `sev*`, merged within a day of the incident |
| Jira, Linear | Issues labeled `incident`, `sev-*`, `postmortem`, `postmortem-action-item`, `reliability`, or linked as "caused by" |
| Slack, Lark | Incident and on-call channels or groups (`#sev-*`, `#incident-*`) around the dates the target code was added |
| Docs | Postmortem docs: their timeline, root cause and action items. An action item often names the exact guard |
| Paging (PagerDuty, Opsgenie, incident.io, FireHydrant) | Incidents and alerts in the window, their responders and their timeline |
| Status pages | Public incidents in the window, for customer-facing impact |
| Observability, logs, error tracking | The first error and the metric change in the incident window |
