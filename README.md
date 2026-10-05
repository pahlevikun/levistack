<p align="center">
  <img src="docs/assets/levi.svg" alt="Levi, the levistack mascot: a floating mug built from a stack of three muted layers, leaning as if tired, with a handle shaped like a fish hook, inside a soft dusky fog" width="220">
</p>

<h1 align="center">levistack</h1>

<p align="center"><em>Meet Levi, the mug. Overskilled, underslept, and one cron job away from a nap.</em></p>

The agent skills I use every day, in one repo. 35 skills, 11 subagents, 41 rules and 5 hooks for Claude Code, Cursor, Codex and the skills CLI.

Your agent is fast. It also says "done" before it ran anything, writes like a press release, and forgets your rules by turn ten. I got tired of fixing the same things by hand, so I wrote them down once. This is that.

## Install

Pick one method. Installing through both the skills CLI and the Claude plugin gives you every skill twice.

```bash
# Any agent (skills CLI). Pick skills or whole groups.
npx skills@latest add pahlevikun/levistack

# Claude Code: the whole stack, or just one group
claude plugin marketplace add pahlevikun/levistack
claude plugin install levistack@levistack
claude plugin install levistack-engineering@levistack
```

Then turn on the hooks you want (next section). Cursor and Codex have manifests too, but I have not load-tested them yet. See [Status](#status).

## What it fixes

### It says "done" and nothing was run

`super-verify` makes it show fresh proof that matches the claim. If it could not check something, it says so.

### It writes like a chatbot

`polyglot-copywriter` is the default writing skill. It removes 26 AI tells and uses short, plain sentences. It never adds a fact that was not in your text. This README went through it.

### It ships tutorial code

`super-noslop` stops generic errors, N+1 queries, filler comments and fake a11y. `output-savers` pushes for the smallest change that works.

### It forgets everything between sessions

`handoff` writes a note a fresh session can pick up cold. `parking-lot` catches tangents so they do not eat the current task. `one-next-action` shrinks a foggy goal to one step.

### It runs scary commands

That one is a hook. Read on.

## Hooks

Hooks are the part that works even when the agent forgets the rules. They run on events, so the rule is enforced and not just suggested. All of them are opt-in. Nothing runs until you create a flag file.

| Hook | What it does |
|---|---|
| `careful-guard` | Asks before `rm -rf /`, force-push, `reset --hard`, `git clean -f` and `DROP TABLE` |
| `generated-file-guard` | Asks before the agent edits a file marked "do not edit" or `@generated` |
| `large-read-guard` | Blocks full reads of files over 350 lines and points the agent to `bulk-reader` |
| `session-start` | Injects a short digest of the always-on rules at the start of every session |
| `notify-done` | Pings you when the agent finishes, so you can leave the tab |

```bash
mkdir -p ~/.levistack
touch ~/.levistack/careful-guard.on ~/.levistack/session-start.on
```

Delete the `.on` file to turn one off. Hooks fail open, so a bug in a hook never locks you out. Details and how to write your own: [`hooks/README.md`](hooks/README.md). Claude Code only for now.

## Where to start

You do not need all 35. These are the ones I would try first.

| Skill | What you get |
|---|---|
| [`super-verify`](skills/engineering/super-verify/SKILL.md) | No "it works" without proof. Diagnoses a failure before it edits anything |
| [`super-tdd`](skills/engineering/super-tdd/SKILL.md) | One failing test, then the smallest pass, then refactor. Never all tests first |
| [`super-challenge-me`](skills/knowledge/super-challenge-me/SKILL.md) | Grills your plan like a critical manager. Numbered questions, each with a recommended answer |
| [`super-codebase-learner`](skills/knowledge/super-codebase-learner/SKILL.md) | Reads a repo and writes down what it actually does today |
| [`atomic-semantic-commit`](skills/delivery/atomic-semantic-commit/SKILL.md) | Splits a messy working tree into small commits with clean messages |
| [`write-mr-description`](skills/delivery/write-mr-description/SKILL.md) | Drafts the MR or PR description from your commits, then reviews it |
| [`glab-code-review`](skills/delivery/glab-code-review/SKILL.md) | Reviews your diff before you open the PR, or reviews a GitLab MR with draft inline notes |
| [`standup`](skills/workflow/standup/SKILL.md) | Builds today's standup from what you really did yesterday |
| [`polyglot-copywriter`](skills/engineering/polyglot-copywriter/SKILL.md) | Plain, human prose in 97 languages, from emails to incident updates |
| [`find-skills`](skills/workflow/find-skills/SKILL.md) | Not sure which skill fits? It picks the chain for you |

Want to build your own? The `agent-authoring` group has a skill for each piece: skills, subagents, rules, hooks, commands and `AGENTS.md`.

## Groups

<!-- groups:start -->
| Group | About | Skills |
|---|---|---|
| `agent-authoring` | Creating agents, skills, rules, hooks, commands and AGENTS.md files for coding assistants. | `convert-as-skill`, `create-agent`, `create-agents-md`, `create-command`, `create-hook`, `create-rule`, `create-skill` |
| `architecture` | System design and stack choices: super-architecture (detect, select, build, evaluate, migrate and document architecture), super-caching, Node backends, super-protobuf, target-stack evaluation and blueprints. | `super-architecture`, `super-caching`, `super-nodejs`, `super-protobuf`, `super-tech-blueprint` |
| `delivery` | Shipping work: atomic commits, merge request descriptions, code review (local diff, request, receive, GitLab glab drafts), tickets, API collections. | `atomic-semantic-commit`, `create-bruno-collection`, `create-jira-story`, `glab-code-review`, `write-mr-description` |
| `engineering` | Engineering habits: review, super-tdd (test-first red-green-refactor across stacks), super-refactor (multi-language behavior-preserving refactors), super-verify (evidence before claims: gate completion, verify-only, investigate first), super-noslop (domain no-slop filter for backend, API, frontend, database, config, and comments), polyglot-copywriter (plain human prose and anti-AI-tell edits), super-design (UI critique, design tokens, component libraries, DESIGN.md), clean-code principles (DRY, SOLID, YAGNI), output-savers, and Elixir with its specialities (OTP, Ecto, Phoenix, security and performance review). | `output-savers`, `polyglot-copywriter`, `super-design`, `super-elixir`, `super-noslop`, `super-refactor`, `super-tdd`, `super-verify` |
| `focus` | ADHD-friendly focus tools: shrink tasks, park tangents, keep momentum. | `one-next-action`, `parking-lot` |
| `knowledge` | Understanding code and domains: current-state codebase learning, architecture docs, site IA, grilling and challenging plans, brainstorming design, planning docs. | `super-challenge-me`, `super-codebase-learner`, `writing-plans` |
| `workflow` | How a session runs: planning, brainstorming, handoffs, standups and reviews of your own work. | `find-skills`, `handoff`, `standup` |
<!-- groups:end -->

## Subagents

Eleven generic ones in `agents/`. They carry no project names. Your project's own `AGENTS.md` supplies the specifics.

The usual flow: `context-harvester` first, then `planner`, `coordinator`, `explorer` or `scaffolder`, then `implementer` or `tdd-runner`, and `reviewer` at the end (plus `security-reviewer` when you touch a trust boundary). Two of them, `bulk-reader` and `template-writer`, run on a small model on purpose, so keep judgment work away from them. Full roster: [`docs/agents/README.md`](docs/agents/README.md).

## Rules

42 rules in `rules/`, by topic: `core`, `architecture`, `elixir`, `go`, `python` and `design`. The core ones cover things like commit messages, comments, testing, failure visibility and PII in logs. Cursor `.mdc` copies are generated into `generated/cursor/rules/`.

## Also in the box

- `commands/`: slash commands. `/handoff` is the one I use most.
- `statusline/`: a one-line status for Claude Code, Cursor CLI and Codex. It shows the branch, model, your 5-hour and weekly limits, and context use. `node scripts/install-statusline.mjs --dry-run` first. See [`statusline/README.md`](statusline/README.md).

## Status

| Install path | State |
|---|---|
| `npx skills add` (nested `skills/<group>/<skill>`) | Not yet verified against the published repo |
| Claude Code marketplace and per-group plugins | Check with `claude plugin validate . --strict` |
| Cursor plugin | Manifest generated, not load-tested |
| Codex plugin | Manifest generated, not load-tested |
| Hooks | Claude Code only |

## Develop

```bash
npm run sync               # regenerate manifests and the group table above
npm run check              # sync --check, validate, tests
./scripts/link-skills.sh   # symlink skills into ~/.claude/skills and ~/.agents/skills
```

Needs Node 20 or newer. To add a skill, create `skills/<group>/<name>/SKILL.md`, run `npm run sync`, then `npm run check`. Conventions are in [`AGENTS.md`](AGENTS.md).

PRs and issues are welcome. If a skill never triggers or gets in your way, tell me. That is how these got better.
