# Deploy and CI history

The timeline check needs to know when code actually shipped, not only when it merged. This source answers that.

## Where it lives

GitHub Actions, GitLab CI, Jenkins, CircleCI, Buildkite, Argo CD and Flux (GitOps), Spinnaker, a cloud deploy service, release tags, and deploy messages posted to chat.

## How to search it

```bash
# GitHub Actions: runs on the main branch around a date
gh run list --branch main --limit 50 --json databaseId,headSha,createdAt,conclusion,name

# GitLab CI: pipelines and deploy jobs
glab ci list --status success
glab api "projects/:id/deployments?environment=production&order_by=created_at&sort=desc"

# Release tags and their dates
git for-each-ref --sort=-creatordate --format='%(refname:short) %(creatordate:iso)' refs/tags | head -20

# Argo CD: what was synced, and when
argocd app history <app>
```

1. **Find the deploy** that first contained the blamed commit (`git tag --contains <sha>`, or the deployment list).
2. **Compare its time** with the first-seen time of the symptom.
3. **Read failed or retried jobs** right before the incident: flaky checks, skipped tests, manual overrides.
4. **Check what else shipped** in the same deploy. Another change in the same release is a competing chain.

## What good evidence looks like

- A production deploy minutes before the first error
- A pipeline where a check was skipped or allowed to fail
- A rollback deploy that matches the symptom stopping

## Pitfalls

- **Merged is not deployed.** A commit can wait days for a release.
- **Several environments.** Name the environment for every time you cite.
- **Feature flags** can turn code on long after it deployed. Check `config-and-flags.md`.

## What to return

Pipeline or deploy id, environment, the commits it contained, start and end time in UTC, the result, and any skipped or failed step.
