---
name: dev-environment
description: "Moves a developer environment in or out. By default one run exports or imports the agent setup and backs up or applies the Mac workstation. An agent setup is skills, rules, agents, commands, hooks, and MCP entries, written as files plus PACK.md. A workstation snapshot is Homebrew, the shell, languages, and editor plugins, applied as an upsert that keeps existing files. Strips secret values and waits for a yes before writing, committing, or pushing. Use when the user says move my dev environment, export my setup, import this setup, backup my Mac, restore a workstation, pack this directory, or import from a git URL. If they say only the agent setup or only the Mac, do that job alone. Not for authoring one skill (create-skill) or checking which CLIs are installed (setup-levistack)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: agent-authoring
  category: agent-authoring
  department: agent-authoring
  related_skills:
    - setup-levistack
    - create-skill
    - find-skills
  tags:
    - environment
    - export
    - import
    - backup
    - workstation
  capabilities:
    - environment_export
    - environment_import
    - workstation_backup
    - workstation_apply
    - secret_redaction
  languages:
    - en

---

# Dev environment

Move a developer environment in or out. By default, one run does both jobs, in this order: the agent setup, then the Mac workstation. Do one job only when the user explicitly limits the request.

An agent setup is skills, rules, agents, commands, hooks, and MCP server entries, written as files plus `PACK.md`. A workstation snapshot is lists and config for Homebrew, the shell, languages, and editor plugins. It is not app binaries and not the contents of git repos. This skill ships that snapshot as `seed/`, plus `scripts/init-repo.sh`, `scripts/snapshot`, and `scripts/apply`. The layout is in [references/structure.md](references/structure.md).

## Scope

Default scope is both.

| The user says | Scope |
|---|---|
| only the agent setup, just the skills, pack only, don't touch the workstation | Agent setup |
| only the Mac, just the workstation, don't touch the agent setup | Workstation |
| move, export, import, backup, or restore the environment, with no limit | Both |

## Direction

| Words | Direction |
|---|---|
| export, backup, snapshot, pack | Out |
| import, apply, restore, set up this Mac | In |

When they name no direction, ask once. Recommend out: export the agent setup and back up the workstation. That writes a pack and a snapshot and does not change the machine.

When both jobs run, they share one direction. When the user gives each job its own direction, follow that.

## Shared rules

1. Show what would be written, including files that would be overwritten. Wait for a yes before copying, applying, committing, pushing, or creating a remote.
2. Keep the name of a token, key, or password. Delete the value. Write `<redacted>` in its place.
3. Agent import may overwrite only the files you listed. Workstation apply is an upsert: keep what exists, add what is missing. Never replace `.zshrc`, an SSH key, or a JSON config wholesale.
4. Do not install packages, run hooks, or push unless that step is the one they asked for.
5. Do not copy private keys, tokens, or session files into the snapshot. `private/` stays out of `seed/`.

## Default run

Out:

1. [Export the agent setup](references/agent-setup.md#export).
2. [Back up the workstation](references/workstation.md#backup).

In:

1. [Import the agent setup](references/agent-setup.md#import).
2. [Apply the workstation](references/workstation.md#apply).

## One job

| Scope | Go to |
|---|---|
| Agent setup | [references/agent-setup.md](references/agent-setup.md) |
| Workstation | [references/workstation.md](references/workstation.md) |

Skip the other job. Say that you skipped it.

## Output

Name the scope, the direction, the paths written, the secret fields redacted, and any job you skipped.

## Related skills

- `setup-levistack`: check whether script tools are installed. It does not move an environment.
- `create-skill`: write one skill. It does not pack a setup or a workstation.
- `find-skills`: discover a skill inside a catalog. It does not export config.

## Done when

- Scope was both unless the user explicitly named one job.
- The agent setup and the workstation each followed their own write rule.
- Secret values were removed.
- Nothing was copied, applied, committed, or pushed before a yes.
- [evals/evals.json](evals/evals.json) covers a default export, a default import, an agent-only request, and a workstation-only request.
