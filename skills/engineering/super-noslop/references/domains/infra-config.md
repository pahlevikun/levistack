# Domain: infra and config

Environment variables, feature flags, deployment config, and infrastructure snippets when they appear in the application diff.

## Checklist

- [ ] Placeholder hostnames, keys, queues, and external IDs labeled before merge (R-23).
- [ ] No plausible secrets or endpoints committed as if production (R-23).
- [ ] Feature flags default safely; both on/off paths work when shipped (R-34).
- [ ] New config keys follow existing layout and naming in sibling files (compat dimension).
- [ ] No invented SLA/uptime/compliance claims in config comments or docs strings (R-17, R-36).

## Out of scope

Full Terraform/module refactors — use **super-refactor** infra track; still run R-23/R-37 when config values are invented.
