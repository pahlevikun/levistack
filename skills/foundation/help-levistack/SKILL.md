---
name: help-levistack
description: "Answers questions about levistack without starting the work: setup, starting a task, which skill or playbook fits, a run that went wrong, making the catalog your own, and the glossary of how to use it, each group, and every skill. Returns one prompt and the file the answer came from. Use when the user types /help-levistack, asks how to use levistack, which skill does X, what a levistack word means, or asks for the levistack version of arena, swarm, interrogate, teach, recall, or architect. Not for doing the task (use-levistack) or for searching and installing skills (find-skills)."
disable-model-invocation: true
metadata:
  version: 1.1.0
  author: levistack
  license: MIT
  group: foundation
  category: foundation
  department: foundation
  related_skills:
    - use-levistack
    - find-skills
    - setup-levistack
  tags:
    - levistack
    - help
    - routing
    - glossary
  capabilities:
    - catalog_help_without_execution
    - stack_glossary
  languages:
    - en

---

# Help levistack

Answer the question, hand back one prompt the user can send, and link the file the answer came from. A help question does not start the work. The user asked how, and a full `use-levistack` run spends real tokens, so the user sends the prompt.

A message that asks for work, such as "use levistack to fix this bug", is not a help question. Read [`use-levistack`](../use-levistack/SKILL.md) and run it.

This file maps questions to the skills that hold the answers. Those skills own the details. Read the file you route to before you quote it, and trust it when it disagrees with this map. Give the user the public copy of the file: `https://github.com/pahlevikun/levistack/blob/main/` followed by its path from the repo root.

## Find out what they need

Infer the need from the message and the chat. A named situation, such as "which skill reviews an MR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `/use-levistack`
- Pick a skill or playbook
- Fix a run that went wrong
- Make levistack my own
- Look up a word, a group, or a skill

A question about a word, a group, or what a skill does goes to [Glossary](#glossary). Answer the entries they named. Give the whole glossary only when they ask for the glossary, the map, or every skill.

Check the state that changes the answer, and mention it only when it does:

- No `~/.levistack/setup.md` means `/setup-levistack` has not run, so nobody has checked which script tools are on this machine. Mention it when the question is about a skill that runs a script, such as a diagram export or an MR context fetch.
- A note that lists a tool as missing means the skill that needs it reports a named gap instead of running that step.

## Get set up

1. Install with `claude plugin marketplace add pahlevikun/levistack`, then `claude plugin install levistack@levistack`. The [README](../../../README.md) has Codex, Cursor, Antigravity, and the skills CLI.
2. Run [`/setup-levistack`](../setup-levistack/SKILL.md). It checks `node`, `python3`, and the optional tools some scripts need, then writes `~/.levistack/setup.md`. It installs nothing without a yes.
3. Start a real task with `/use-levistack`, a goal, and a check that can pass or fail.

Installing changes nothing until a skill runs. Most skills load from the user's words when the description matches. `help-levistack` and `setup-levistack` load only when typed.

## Start a task with `/use-levistack`

`/use-levistack` checks this machine first. If `node` or `python3` is missing, it runs `setup-levistack` and waits until that check is no longer blocked. Then it matches a playbook and runs seven steps: route, prime, invoke, hunt, apply, prove, deliver. The playbook decides which skills the apply step chains. A good prompt states the goal and how to tell it is done. It does not list skills, because a hand-written chain tends to drop the hunt or the proof.

Name a playbook to skip the match: "use-levistack, investigate playbook: how does checkout retry". The playbooks live in [`use-levistack/playbooks/`](../use-levistack/playbooks/).

## Pick a skill or playbook

The default answer is `/use-levistack`. Name a skill directly when the user wants more or less than the playbook gives. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill or playbook |
|---|---|
| Do any non-trivial task with the full route | `use-levistack` |
| Check the agent understood the goal before it edits | Any `use-levistack` playbook. Its first step restates the goal and the problem |
| Rewrite a prompt deeper before sending it, without doing the task | `challenge-me` sharpen mode |
| Know how code works now, or where new code should live | `codebase-learner` |
| Know why code is shaped this way, or where a number came from | `trace` |
| Understand a change or subsystem, explained plainly | `use-levistack` playbook `investigate` |
| Rebuild context on recent work, or ask where they left off | `handoff` Recall |
| Pick up a paused session from a note | `handoff` Resume |
| Know what a small diff could break outside itself | `blast-radius` |
| Settle types and module shape before code that crosses a function boundary | `shape-and-build` |
| Choose an architecture style for a system | `super-architecture` |
| Record an architecture decision | `write-adr` |
| Get several attempts at one brief and keep the best | `rumbling` Contest, then `evidence` Judge |
| Run independent slices in parallel and merge one report | `rumbling` Split, then `evidence` Judge |
| Have a reviewer try to break a diff | `second-opinion` |
| Fix a bug or build a feature test-first | `tdd` |
| Repeat a fix until named checks pass | `loopy` |
| Strip slop and narrating comments from code | `noslop` |
| Clean AI tells out of prose for people | `polyglot-copywriter` |
| Hear the last reply again in plain words | `polyglot-copywriter` |
| Write docs, an ADR, an MR description, a changelog, a runbook, or a postmortem | `create-documentation`, `write-adr`, `write-mr-description`, `write-changelog`, `write-runbook`, `write-postmortem`, by document type |
| Vet a performance number before reporting it | `verify` (vet a number) |
| Run a large or cross-cutting change a person reviews after stepping away | `figure-it-out` |
| Keep a decision log during a long run | `handoff` Write, with a decision row per choice |
| Turn what a finished task taught into skill edits | `retrospective` session mode |
| Stop agents repeating the same mistake in this repo | `retrospective` repo mode |
| Apply a working principle by name, such as "attack the premise" | `principles` |
| Check which script tools this machine has | `setup-levistack` |
| Find their way around levistack | `help-levistack` |

A skill missing from this table: read [`find-skills/references/routing.md`](../../workflow/find-skills/references/routing.md), which lists every skill by job.

Close calls:

- `codebase-learner` explains what the code does. `trace` explains the reasons. The `investigate` playbook runs one or both and explains the result plainly.
- `rumbling` Contest gives every worker the same brief and keeps the best. Split gives each worker a different slice. Both end in `evidence` Judge.
- `second-opinion` reviews the diff. `blast-radius` looks for breakage outside the diff and proves the one fact the change is safe because of.
- `shape-and-build` settles types and signatures, then implements. `super-architecture` picks the style. `write-adr` records the decision.
- `figure-it-out` designs one auditable run. `write-plan` writes an accepted spec for someone else to build.
- `loopy` repeats until named checks pass. `evidence` runs one evidence-led pass. `verify` runs the check once.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The router stopped after recommending a skill | It must run all seven steps. Start the message with `/use-levistack` |
| A question was treated as the next step of the last task | Say "new task" |
| A skill did not load on its own | Its description did not match the words. Name it, or run `/use-levistack` |
| A script step said a tool is missing | Run `/setup-levistack` to see the gap and the install command it suggests |
| The reply claims success from a green build | Ask for the real command and its output. That is `verify` |
| A loop ran forever or claimed a pass on a failure | `loopy` needs an observable pass condition. Give one |
| Parallel agents overwrote each other | `rumbling` isolates each writer: its own files or output folder, or its own worktree where the project allows one |

## Make levistack my own

- `retrospective` after a session names the skill edit a lesson calls for. It applies the edit only when asked.
- `create-skill` writes a new skill. `convert-as-skill` turns a rule, command, or document into one.
- Fix a misbehaving skill in its own change, not inside the feature work where it went wrong.

## Glossary

Index only. The linked file owns the detail. Read that file before you quote anything this line does not say. The picture of this same glossary is [docs/assets/levistack-glossary.png](../../../docs/assets/levistack-glossary.png).

For one skill, the prompt is `/use-levistack` plus the job that row names. `help-levistack` does not start work, so its prompt is the question itself. For a how-to-start question, the prompt is `/use-levistack` and the task.

<!-- glossary-body:start -->
### How to use

Three ways to start. On the full route and on a one-shot, the machine check runs first. If `node` or `python3` is missing, `setup-levistack` runs before the steps. A bare skill does not run that check.

| Way | What you type | What runs |
|---|---|---|
| Full route | `/use-levistack` or `/start`, and the task | A machine check, then a playbook and all seven steps. |
| One-shot | A skill name inside that command | Prime, that skill, hunt to confirm, prove, deliver. |
| Bare skill | `/skill` alone | That skill only. Prime, hunt, and deliver stay off. |

Prime, hunt, and deliver always run on the full route and on a one-shot.

| Step | Word | What it does |
|---|---|---|
| 1 | Route | Match a playbook, or mark a named skill as a one-shot. |
| 2 | Prime | output-savers reads your prompt for the job, the safety needs, and the reply length. It does not rewrite your words. |
| 3 | Invoke | Restate the goal, then pick the first skill. |
| 4 | Hunt | find-skills searches this catalog. This step runs every time. |
| 5 | Apply | The chain runs, one skill at a time. At most four skills. |
| 6 | Prove | verify shows fresh proof. A push, MR, comment, install, or publish waits for your yes. |
| 7 | Deliver | polyglot-copywriter shapes prose for people. output-savers is the last gate on the reply. |

| Word | Means |
|---|---|
| Playbook | A named route for one kind of task: investigate, feature, bug-fix, refactor, design-shape, parallel, prove-outside-diff, open-ended. It fills invoke and apply. The seven steps still run. |
| Chain | The skills for this task, at most four. Each one prepares, does the work, or verifies. |
| Your yes | A push, MR, comment, install, or publish waits until you agree. |
| Loaded | This host can start the skill by name. |
| File-only | The skill is a file on disk. Read its SKILL.md and follow it. |
| skills.sh | The only outside catalog find-skills may browse, and only after this catalog has no fit. |
| Upstream | A skill in its own repo. The levistack plugin installs it. Edit it in that repo. |
| Group | A folder of skills. It also ships as the plugin `levistack-<group>`. |
| Catalog | The skills, agents, rules, commands, and hooks this repo publishes. |
| Agent | A helper for one bounded job. The session keeps the seven steps. |
| Rule | A standard that holds even when nobody invoked a skill. |
| Command | A saved prompt you run as /name. /start runs use-levistack. |
| Hook | An opt-in check on a tool event. It runs only after you create `~/.levistack/<name>.on`. |

### Groups

Order follows the path: front door, machinery, the work, the session, the catalog, then upstream.

| Group | What it is | Skills |
|---|---|---|
| [`foundation`](../../foundation/DESCRIPTION.md) | The front door. Start a task, check the machine, or ask how. | 3 |
| [`workflow`](../../workflow/DESCRIPTION.md) | The machinery around a result: hunt, evidence, loops, lanes, handoff. | 9 |
| [`knowledge`](../../knowledge/DESCRIPTION.md) | How code works, why it is shaped that way, and whether a plan holds. | 5 |
| [`engineering`](../../engineering/DESCRIPTION.md) | Test first, prove the claim, keep behavior, and cut slop. | 7 |
| [`architecture`](../../architecture/DESCRIPTION.md) | Pick a shape, a stack, or a boundary, then build against it. | 7 |
| [`delivery`](../../delivery/DESCRIPTION.md) | Spec, plan, review, and the writing that ships with the change. | 14 |
| [`product`](../../product/DESCRIPTION.md) | Color, screens, diagrams, explainers, prototypes, and polish. | 8 |
| [`focus`](../../focus/DESCRIPTION.md) | The session itself. One next step, a later list, today's standup. | 3 |
| [`agent-authoring`](../../agent-authoring/DESCRIPTION.md) | Skills, agents, rules, commands, hooks, and whole setups. | 10 |
| [`upstream`](../../../upstream.json) | Their own repos. The levistack plugin installs them. Edit them there. | 2 |

### Every skill

66 catalog skills, plus 2 upstream. concise, concise-light, concise-heavy, and principles live inside output-savers. noslop-code lives inside noslop. Those are modes, not extra catalog skills.

#### foundation

| Skill | Does |
|---|---|
| [`use-levistack`](../../foundation/use-levistack/SKILL.md) | Check the machine, match a playbook, then run the seven steps. |
| [`setup-levistack`](../../foundation/setup-levistack/SKILL.md) | Check the tools scripts call. Install nothing without a yes. |
| [`help-levistack`](../../foundation/help-levistack/SKILL.md) | Say which skill fits and hand back a prompt. Do not start the work. |

#### workflow

| Skill | Does |
|---|---|
| [`find-skills`](../../workflow/find-skills/SKILL.md) | Search this catalog. On a miss, browse skills.sh, install, and run. |
| [`evidence`](../../workflow/evidence/SKILL.md) | Frame a goal, run one evidence-led pass, or judge finished work. |
| [`loopy`](../../workflow/loopy/SKILL.md) | Repeat one change until the named checks pass or a stop state hits. |
| [`rumbling`](../../workflow/rumbling/SKILL.md) | Split, Contest, or Council. Then evidence judges the result. |
| [`handoff`](../../workflow/handoff/SKILL.md) | Resume, catch up, recall, or write the note for the next session. |
| [`figure-it-out`](../../workflow/figure-it-out/SKILL.md) | Design one auditable run when no narrower playbook fits. |
| [`lane-lead`](../../workflow/lane-lead/SKILL.md) | Several lanes, one controller. Lanes do not merge or push. |
| [`compare-models`](../../workflow/compare-models/SKILL.md) | One prompt on two or three models this host can spawn. |
| [`retrospective`](../../workflow/retrospective/SKILL.md) | Name repeated friction and the strongest useful fix. |

#### knowledge

| Skill | Does |
|---|---|
| [`codebase-learner`](../../knowledge/codebase-learner/SKILL.md) | Explain how the code works today. Read-only. |
| [`trace`](../../knowledge/trace/SKILL.md) | Explain why it is shaped this way, evidence on every step. |
| [`challenge-me`](../../knowledge/challenge-me/SKILL.md) | Grill a plan. Numbered questions, each with a recommended answer. |
| [`research`](../../knowledge/research/SKILL.md) | Answer from primary sources, or write questions for one person. |
| [`second-opinion`](../../knowledge/second-opinion/SKILL.md) | Read-only review that drives each open decision to a commitment. |

#### engineering

| Skill | Does |
|---|---|
| [`tdd`](../../engineering/tdd/SKILL.md) | One failing test, the smallest pass, then refactor while green. |
| [`verify`](../../engineering/verify/SKILL.md) | Fresh proof before any claim of done. Diagnose before editing. |
| [`safe-refactor`](../../engineering/safe-refactor/SKILL.md) | Keep behavior the same while the structure changes. |
| [`noslop`](../../engineering/noslop/SKILL.md) | Filter slop in handlers, UI, queries, config, tests, and comments. |
| [`output-savers`](../../engineering/output-savers/SKILL.md) | The smallest change, named principles, and plain replies. |
| [`blast-radius`](../../engineering/blast-radius/SKILL.md) | What a small diff can break outside itself, and why it is safe. |
| [`dev-cache-cleanup`](../../engineering/dev-cache-cleanup/SKILL.md) | Audit dev caches. Delete only paths you approved. |

#### architecture

| Skill | Does |
|---|---|
| [`shape-and-build`](../../architecture/shape-and-build/SKILL.md) | Settle types and module shape, compare two, then build one. |
| [`super-architecture`](../../architecture/super-architecture/SKILL.md) | Detect, choose, build, evaluate, migrate, or document one. |
| [`super-caching`](../../architecture/super-caching/SKILL.md) | Cache design for web and mobile, including offline. |
| [`super-nodejs`](../../architecture/super-nodejs/SKILL.md) | Node.js services, APIs, middleware, and auth. |
| [`super-elixir`](../../architecture/super-elixir/SKILL.md) | Elixir, Phoenix, Ecto, and OTP. |
| [`super-protobuf`](../../architecture/super-protobuf/SKILL.md) | proto3, buf, gRPC or Connect, and schema breaks. |
| [`super-tech-blueprint`](../../architecture/super-tech-blueprint/SKILL.md) | Compare stacks, cost a migration, or write a blueprint. |

#### delivery

| Skill | Does |
|---|---|
| [`write-plan`](../../delivery/write-plan/SKILL.md) | A plan a stranger can follow: files, tasks, tests, and commits. |
| [`ready-spec`](../../delivery/ready-spec/SKILL.md) | An execution-ready spec for a backend or API change. |
| [`write-adr`](../../delivery/write-adr/SKILL.md) | An ADR, design doc, or RFC from the code and real alternatives. |
| [`code-review`](../../delivery/code-review/SKILL.md) | Review a diff or MR. Watch stays until clean. Prep stops before merge. |
| [`refresh-pr`](../../delivery/refresh-pr/SKILL.md) | Refresh, rework, or close a stale PR or MR, then code-review. |
| [`atomic-semantic-commit`](../../delivery/atomic-semantic-commit/SKILL.md) | Split a messy tree into small commits with clean messages. |
| [`write-mr-description`](../../delivery/write-mr-description/SKILL.md) | Draft the MR or PR description from the commits. |
| [`create-tickets`](../../delivery/create-tickets/SKILL.md) | Slice a plan into end-to-end tickets, then draft them. |
| [`create-documentation`](../../delivery/create-documentation/SKILL.md) | Docs and API handovers checked against the source. |
| [`create-bruno-collection`](../../delivery/create-bruno-collection/SKILL.md) | A Bruno API collection, with auth and error examples. |
| [`file-toolkit`](../../delivery/file-toolkit/SKILL.md) | Parse, create, or convert documents, images, and audio. |
| [`write-changelog`](../../delivery/write-changelog/SKILL.md) | Changelog and release notes from the commits and the diff. |
| [`write-postmortem`](../../delivery/write-postmortem/SKILL.md) | A blameless postmortem or near-miss, from evidence. |
| [`write-runbook`](../../delivery/write-runbook/SKILL.md) | A recovery, deploy, or migration runbook with a rollback. |

#### product

| Skill | Does |
|---|---|
| [`color-kit`](../../product/color-kit/SKILL.md) | Pick colors and prove contrast. |
| [`design-system-kit`](../../product/design-system-kit/SKILL.md) | Build a design system, then critique with it. |
| [`ui-ux-kit`](../../product/ui-ux-kit/SKILL.md) | One screen or one component, including motion. |
| [`diagram`](../../product/diagram/SKILL.md) | A technical diagram with an editable source and a checked export. |
| [`infographic`](../../product/infographic/SKILL.md) | An evidence-based explainer, chart, timeline, or poster. |
| [`prototype-wireframe`](../../product/prototype-wireframe/SKILL.md) | A throwaway prototype or wireframe for one design question. |
| [`product-polish-workflow`](../../product/product-polish-workflow/SKILL.md) | Audit a shipped product: code, journeys, branding, motion. |
| [`visual-art`](../../product/visual-art/SKILL.md) | Static canvas art, seeded generative art, or a short GIF. |

#### focus

| Skill | Does |
|---|---|
| [`get-moving`](../../focus/get-moving/SKILL.md) | Shrink a stuck task to one next action and a 25-minute round. |
| [`later-list`](../../focus/later-list/SKILL.md) | Park a tangent in LATER.md and return to the task. |
| [`standup`](../../focus/standup/SKILL.md) | Today's standup from what you actually did. |

#### agent-authoring

| Skill | Does |
|---|---|
| [`create-skill`](../../agent-authoring/create-skill/SKILL.md) | Write or fix a skill. |
| [`convert-as-skill`](../../agent-authoring/convert-as-skill/SKILL.md) | Turn existing material into a skill, or merge skills. |
| [`create-agent`](../../agent-authoring/create-agent/SKILL.md) | Write a subagent. |
| [`create-command`](../../agent-authoring/create-command/SKILL.md) | Write a slash command. |
| [`create-rule`](../../agent-authoring/create-rule/SKILL.md) | Write a rule or coding standard. |
| [`create-hook`](../../agent-authoring/create-hook/SKILL.md) | Automate something on an agent event. |
| [`create-agents-md`](../../agent-authoring/create-agents-md/SKILL.md) | Write or refresh AGENTS.md or CLAUDE.md. |
| [`mcp-management`](../../agent-authoring/mcp-management/SKILL.md) | Connect, diagnose, or build an MCP server. |
| [`dev-environment`](../../agent-authoring/dev-environment/SKILL.md) | Move an agent setup and a Mac in or out. Secrets are stripped. Waits for a yes before writing. |

#### upstream

| Skill | Does |
|---|---|
| [`polyglot-copywriter`](https://github.com/pahlevikun/polyglot-copywriter) | Plain prose for people, in 97 languages, facts unchanged. |
| [`logo-kit-svg`](https://github.com/pahlevikun/logo-kit-svg) | An SVG brand kit: icon, banner, static, and animated. |
<!-- glossary-body:end -->

## Reply

Lead with the answer. Give at most one example prompt in a code block, then the public link to the file it came from. Keep it short unless the user asked for the whole map. Do not edit files, run checks, or start `use-levistack` from a help question.

## Related skills

- `use-levistack`: runs the work this skill only describes.
- `find-skills`: searches and installs skills beyond this map.
- `setup-levistack`: checks the machine before a script step needs a tool.

## Done when

- The reply answers the question and gives at most one prompt and one link.
- No file was edited and no task was started.
- [evals/evals.json](evals/evals.json) covers a help question, a work request, an outside word that maps to an existing skill, and a glossary question.
