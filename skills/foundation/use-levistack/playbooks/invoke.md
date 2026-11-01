# Invoke the first skill

**Step 3**, after [prime.md](prime.md). Restate the goal and the problem first. When step 1 matched a situational playbook, its first skill is the pick and its table is the chain. Otherwise pick **one** first skill below before any catalog hunt, unless the user clearly asked for two things (see Chaining).

## Intent map

| The user wants to… (signals) | First skill |
|---|---|
| Know how X works, walk through a flow, find where something lives or should live | `codebase-learner` (explain mode) |
| Know why X is this way, the tradeoff, the history, whether a guard is still needed | `trace` (rationale mode) |
| Find the root cause of a bug, an incident, a flaky test or a slow pipeline; five whys | `trace` (root-cause mode). If the failure is live and its mechanism unknown, `verify` (investigate first) runs inside it |
| Understand a whole repo, onboard, write ARCHITECTURE.md or CLAUDE.md of what exists | `codebase-learner` (onboard or summarize mode) |
| Grill a plan, doc, idea or design; poke holes; brainstorm before code | `challenge-me` |
| Get a detailed spec for a backend or API change before an agent builds it | `ready-spec` |
| Get a step-by-step coding plan from a spec | `write-plan` |
| Build a feature or fix a bug | `tdd` |
| Refactor without changing behavior | `safe-refactor` |
| Tear apart a diff or branch, find blind spots before merge | `second-opinion` |
| Give independent agents different tasks, competing solutions, or one question to investigate in parallel | `rumbling` (Split, Contest, or Council) |
| Review an MR, or act on review comments | `code-review` |
| Commit, split commits, open or describe an MR or PR | `atomic-semantic-commit`, then `write-mr-description` |
| Prove something is done, run the gates, find why it fails | `verify` |
| Audit or polish a shipped product's code, UI, journeys or branding. It calls the three skills below when it reaches colors, screens or the system | `product-polish-workflow` |
| Write or rewrite text for people | `polyglot-copywriter` |
| Answer from primary sources, the web, or git-recorded facts, or draft a questionnaire for one person | `research` |
| Draw Mermaid, SVG, draw.io or Excalidraw diagrams, including animated exports | `diagram` |
| Build an editorial infographic from evidence | `infographic` |
| Learn from this session or repeated mistakes in a repo | `retrospective` |
| Retro an initiative, or reconstruct what happened on a ticket, PR, or branch | `retrospective` (initiative or artifact) |
| Repeated local or CI environment setup friction | `retrospective` (environment) |
| Build a skill, agent, rule, hook, command or AGENTS.md | the matching `create-*` skill |
| Stuck, overwhelmed, or a tangent showed up | `get-moving` or `later-list` |
| Catch me up on this chat, what is waiting on me, or what was I doing last week | `handoff` (catch up or recall mode) |
| Make this prompt better, deeper or sharper before running it | `challenge-me` (sharpen mode) |
| Is this change safe, is this speedup real | `verify` (prove it is safe, or vet a number) |
| What could this small diff break outside itself, blast radius | `blast-radius` |
| Settle types, signatures, and module shape before code, then build it | `shape-and-build` |
| A large migration or ambitious change a person reviews later, and no narrower route fits | `figure-it-out` |
| How to use levistack, which skill fits, without doing the work | `help-levistack` |
| Check which script tools this machine has | `setup-levistack` |
| Refresh a stale pull request or merge request, or decide whether to close it | `refresh-pr` |
| Stay with a request until it is clean, or get it merge-ready and stop | `code-review` (watch or prep) |
| Several lanes under one controller, and they must not merge | `lane-lead` |
| Compare one prompt on two or three models | `compare-models` |
| Export or import an agent setup, or back up or restore a Mac workstation | `dev-environment` |
| Throwaway prototype, wireframe or screen map to answer a design or behavior question | `prototype-wireframe` |
| Only colors: a palette, brand colors, dark mode, a theme, a contrast fix or a color audit | `color-kit` |
| One screen, component, interaction, gesture or motion on iOS, Android, React Native, Flutter, desktop, web, car or TV | `ui-ux-kit` |
| A whole design system, token file, DESIGN.md or governance, or extract a site's design. It calls `color-kit` and `ui-ux-kit` | `design-system-kit` |
| Audit the existing tests for weak or duplicate ones | `tdd` (audit mode) |
| Write docs for a feature, or check docs after a change | `create-documentation` |
| Write a design doc or RFC | `write-adr` (Proposal job) |
| Write, review, or supersede an ADR | `write-adr` |
| Write a changelog or release notes | `write-changelog` |
| Write a postmortem or near-miss report after stabilization | `write-postmortem` |
| Write a recovery, deployment or migration runbook | `write-runbook` |
| Frame a reusable goal prompt, run an evidence workflow, judge completed work, rewrite a report, or build a domain workflow | `evidence` (requested mode) |
| Loop until the named checks pass | `loopy` |
| Build a client API handover with complete responses and state coverage | `create-documentation` (handover; Bruno first, `create-bruno-collection` if missing or incomplete) |
| Stop or resume a session; write a standup | `handoff`; `standup` |
| A domain is named: architecture, caching, Node, protobuf, Elixir, slop, stack choice | that `super-*` domain router |
| Anything else, or two rows fit equally | still step 4: [find-skills](../../../workflow/find-skills/SKILL.md). Step 4 also runs when a row above already matched |

## Named one-shots

The user named a skill: that skill is the step 3 pick. Step 4 still runs and must keep it. Steps 5, 6, 6b, and 7 still run. Read-only skills (`codebase-learner`, `trace`, `second-opinion`, `challenge-me`) skip step 6 unless they made a claim that needs a command to prove it.

**Not invoke picks:** `output-savers` and `polyglot-copywriter` are gates in steps 2 and 7, not routes, unless the user's whole job is writing or shrinking text.

## Agents

Spawn one only for a bounded job, and keep routing in this session.

| Spawn | When |
|---|---|
| `context-harvester` | The task needs facts gathered from several places first |
| `explorer` | `codebase-learner` on a wide subsystem: one angle per agent |
| `reviewer`, `security-reviewer` | `second-opinion` reviewers |
| `planner` | A large plan before `write-plan` |
| `tdd-runner`, `implementer` | A planned task with clear acceptance |
| `bulk-reader` | A huge file or log; judgment stays here |

## Chaining

Allowed when one output feeds the next:

- `codebase-learner` or `trace` → `ready-spec` → `write-plan` → `tdd`
- `challenge-me` → `write-plan`
- `codebase-learner` → `super-architecture` or `super-tech-blueprint`
- `tdd` or `safe-refactor` → `second-opinion` → `atomic-semantic-commit` → `write-mr-description`
- Independent parallel work, a contest, or a council → `rumbling` → `evidence` Judge
- Repeat until the named checks pass → task skill inside `loopy`
- One evidence pass, plan, judge, report, or domain workflow → `evidence` in that mode
- Unfinished work or an ending session → `handoff` Write after prove, before deliver

Do not run `second-opinion` and `challenge-me` on the same artifact unless the user asked for both. Do not run `loopy` and `evidence` Run on the same edit.

## File, tool-server and art tasks

| User intent | First owner |
|---|---|
| Audit Node.js, web, mobile, or backend development caches, or perform exact approved cleanup | `dev-cache-cleanup` |
| Configure, diagnose or build MCP servers | `mcp-management` |
| Parse/create/reconstruct/convert documents, images or audio | `file-toolkit` |
| Canvas, seeded generative art or animated GIF composition | `visual-art` |
| Explicit sprint/month/date-window activity report | `standup` (period report) |
