# Config and feature flags

Code can be the same while behavior changes, because a config value or a flag changed. Check this source whenever the timeline shows no deploy near the first-seen time.

## Where it lives

Feature-flag services (LaunchDarkly, Unleash, Flagsmith, Split, ConfigCat, GrowthBook), config stores (Consul KV, etcd, AWS AppConfig or Parameter Store, Spring Cloud Config), Kubernetes ConfigMaps, environment files, and config repos (GitOps).

## How to search it

1. **Find the flag or key** the code reads: search the code for the flag name or config key.
2. **Read its change history** (audit log): who changed the value, targeting or rollout percentage, and when. Flag services and most config stores keep one.
3. **Config in git:** `git log -p -- <config path>` in the config repo.
4. **Compare values** between environments when only one environment fails.
5. **Check the default** in the code: what happens when the key is missing.

```bash
consul kv get -recurse <prefix>          # current values (read-only)
git log -p --since='7 days ago' -- config/   # changes in a config repo
```

## What good evidence looks like

- A flag rollout raised from 10% to 100% minutes before the errors
- A config value changed by hand, with no matching ticket
- A missing key that makes the code fall back to an unsafe default

## Pitfalls

- **Secrets.** Never print secret values. Say "the key changed at <time>", not the value.
- **Per-user targeting.** A flag can be on for some users only. Check the targeting rules.
- **Caching.** Services can cache config for minutes. The effect can lag the change.

## What to return

The flag or key, the environment, each change with its time, author and old and new value (secrets masked), and the code path that reads it.
