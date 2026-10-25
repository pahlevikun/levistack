# Review machine and runtime friction

Use this mode when friction comes from **where** work runs: laptop, container, remote dev box, CI runner, or cloud sandbox. Symptoms include "works on my machine", missing tools, wrong versions, flaky local services, permission errors, and reproduce steps that differ from CI.

This is not live debugging of a single failing command. For "why does checkout fail right now", use `trace` or `verify`. Environment retro looks for **repeatable setup gaps** and proposes durable fixes.

## Bound the environment

State:

- Host type (local OS, container image, CI label, remote host).
- Repository and commands the user cares about.
- What already failed or wasted time, with log excerpts or error text the user supplies.

Collect read-only facts before proposing changes:

| Source | Examples |
|---|---|
| Toolchain | Language runtime, package manager, compiler versions |
| Container | Image tag, compose services, volume mounts |
| CI | Job image, env vars (names only; never echo secrets), cache keys |
| Repo docs | README, CONTRIBUTING, devcontainer, Nix, mise, asdf pins |
| Lockfiles | Package lock, toolchain file, Dockerfile pins |

Redact secrets and tokens from excerpts. If a value might be sensitive, refer to it by name only.

## Inspect eight environment categories

| Category | Look for | Stronger fixes |
|---|---|---|
| Version drift | Local vs CI mismatch | Pin in lockfile, matrix, or devcontainer |
| Missing prerequisite | Undocumented binary or service | Doc plus optional bootstrap script |
| Path and shell | Wrong cwd, profile, or env not loaded | Documented entry command or direnv |
| Permissions | FS, network, or registry access | Documented setup or CI secret pattern |
| Resources | OOM, disk, slow IO | Document limits or slimmer default |
| Networking | Proxy, VPN, localhost ports | Compose profile or documented tunnel |
| Data dependencies | Seed DB, fixtures, API sandboxes | Scripted seed or documented snapshot |
| Reproducibility | Non-deterministic installs | Frozen lockfile and image digest |

A one-off outage or typo is not a lesson. Two independent failures with the same enabling condition qualify for supported proposals.

## Relate to tooling lens

Apply the tooling lens from `SKILL.md` with environment evidence. Read existing bootstrap scripts and CI before inventing a second installer.

Prefer, in order:

1. Single source of truth for versions (lockfile, image, or toolchain file).
2. CI job that exercises the same install path developers use.
3. Documented one-liner or `make`/`npm` target that wraps the real commands.
4. Prose-only README steps only when automation cannot be justified.

## Proof for environment checks

Each proposed check or doc change needs:

- A **past failure** this team actually hit (log line or command output cited).
- The **exact command** a newcomer or CI would run after the fix.
- Expected success signal and what a failure should tell the next agent.

Replay is optional and scope-bound like repo mode. Missing dependencies during replay is inconclusive, not proven.

## Return

Rank proposals by how many people or pipelines would hit the same gap. Separate supported proposals, open leads, and rejected ideas via synthesis.

Do not change global machine config, install packages, or modify CI without explicit approval outside this retro.
