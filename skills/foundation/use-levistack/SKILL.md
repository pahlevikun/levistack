---
name: use-levistack
description: "Start here. Checks this machine first. If node or python3 is missing, setup-levistack runs before the task. Then matches a situational playbook (investigate, feature, bug-fix, refactor, design-shape, parallel, prove-outside-diff, open-ended), restates the goal before edits, and runs route, prime, invoke, hunt, apply, prove, deliver. Always hunts with find-skills, even when a first skill is already clear. Combines rumbling then evidence Judge for parallel work, loopy when named checks must be repeated until they pass, and evidence for one evidence-led pass or a read-only judge. Writes a handoff note before deliver when the task is unfinished or the session is ending. Use when the user does not know which skill fits, says 'where do I start', 'help me with', 'what should I use', 'just handle it', gives a goal with no skill named, or types /use-levistack with a task. A named skill inside it still runs, after the hunt confirms it."
metadata:
  version: 1.3.0
  author: levistack
  license: MIT
  group: foundation
  category: foundation
  department: foundation
  related_skills:
    - setup-levistack
    - find-skills
    - handoff
    - rumbling
    - loopy
    - evidence
    - help-levistack
    - shape-and-build
    - blast-radius
    - figure-it-out
  invokes:
    - skill: setup-levistack
      when: Before step 1, when the machine check is blocked or node cannot run the check
    - skill: find-skills
      when: Every use-levistack run, after the first skill is picked, to confirm the chain
    - skill: handoff
      when: Resume at the start, or Write before deliver when the task is unfinished or the session is ending
    - skill: rumbling
      when: Independent parallel tasks, competing solutions, or a council on one question
    - skill: loopy
      when: Named checks must be repeated until they pass
    - skill: evidence
      when: One evidence-led pass, a plan, a read-only judge, a report rewrite, a domain workflow, or the judge after rumbling
    - skill: shape-and-build
      when: The design-shape, feature, or bug-fix playbook needs types and signatures settled before code
    - skill: blast-radius
      when: The prove-outside-diff, bug-fix, or refactor playbook needs what a change breaks outside its diff
    - skill: figure-it-out
      when: The open-ended playbook matched a large run no narrower playbook fits
  tags:
    - levistack
    - routing
    - playbooks
    - handoff
    - rumbling
    - loopy
    - evidence
  capabilities:
    - catalog_routing
    - situational_playbooks
    - workflow_combinations
    - machine_check_before_route
  languages:
    - en

---

# Use levistack

Do not stop at a recommendation. Check the machine, then run the steps below in order, top to bottom, for every prompt.

## Machine check (before step 1)

Every run, including a one-shot. A bare `/skill` call does not come through this router, so it skips this check.

1. Run the live check. An old `~/.levistack/setup.md` is not enough on its own.

   ```bash
   node <setup-levistack>/scripts/check.mjs
   ```

   The script lives in the `setup-levistack` skill folder, next to this skill at `../setup-levistack/scripts/check.mjs` in the catalog. It writes nothing and installs nothing. Read the `Status:` line. Exit 0 means `node` 20+ and `python3` are present. Exit 1 means blocked.
2. Status `ready`, or `ready with N named gap(s)`: this machine can run. If `~/.levistack/setup.md` is missing, or its status line differs from the live check, refresh the note with `--write`. That writes the note only. Then go to step 1. A named gap (an optional tool such as `ffmpeg` or `glab`) does not stop the route and is not an install. When a later skill needs that tool, name the gap and its install line from the note, and offer `setup-levistack` for that tool.
3. Status `blocked`, or `node` cannot run the script: do not start the seven steps. Read [`setup-levistack`](../setup-levistack/SKILL.md) and follow it. It has `disable-model-invocation: true`, so load it by reading the file. It asks before any install. When a recheck is no longer blocked, return to step 1. If the user declines a required install, say what is blocked and stop.

## Orchestration (run in order)

| Step | Do | Playbook | Skip when |
|---|---|---|---|
| 0 Machine | Live check from `setup-levistack`. Ready, including named gaps: step 1. Blocked: follow `setup-levistack`, then come back | [Machine check](#machine-check-before-step-1) | Never |
| 1 Route | Accept the prompt. Match one situational playbook from the table below. If the user named a skill, mark it a one-shot | [Situational playbooks](#situational-playbooks) | Never |
| 2 Prime | `output-savers` Step 0 on the **user's** prompt: safety override, job, reply level. Never rewrite their words | [prime.md](playbooks/prime.md) | Never |
| 3 Invoke | Restate the goal and the problem before any edit. Then take the first skill from the matched playbook, the intent map, or the named one-shot. No clear intent: go to step 4 | [invoke.md](playbooks/invoke.md) | Never |
| 4 Hunt | `find-skills` on every run. Keep the step 3 pick. Confirm it in the catalog and add only the missing companions below. At most four skills in the chain | [find-skills](../../workflow/find-skills/SKILL.md) | Never |
| 5 Apply | Run the chain. Load each skill when its step starts. Pass each result to the next in one sentence | the chosen `SKILL.md` files | Never |
| 6 Prove | `verify` before any "done", "fixed" or "passing". Every outward-facing action stops at the user | [prove.md](playbooks/prove.md) | Nothing was changed and nothing is claimed |
| 6b Close | `handoff` Write before deliver when the task is unfinished, paused, or the session is ending. Resume, catch up, or recall when the user is continuing or returning | [handoff](../../workflow/handoff/SKILL.md) | The reply finishes the task and nothing remains for a later session |
| 7 Deliver | `polyglot-copywriter` on prose a person will read, then `output-savers` last on **your** reply | [deliver.md](playbooks/deliver.md) | Never |

Never reorder. A claim without fresh proof does not enter the reply. An outward action without a yes does not run.

## Situational playbooks

A playbook fills steps 3 and 5 for one kind of task: the first skill, the chain, and the reply shape. The seven steps still run around it. Match one in step 1. The user can name one directly ("investigate playbook: ..."). No match: use the intent map in step 3.

| The task is | Playbook |
|---|---|
| Understand how or why code works, or learn a change plainly. Read-only | [investigate](playbooks/investigate.md) |
| Add or build new behavior | [feature](playbooks/feature.md) |
| Fix a bug, a regression, or a failing test | [bug-fix](playbooks/bug-fix.md) |
| Restructure without changing behavior | [refactor](playbooks/refactor.md) |
| Settle types, signatures, module shape, or an architecture choice | [design-shape](playbooks/design-shape.md) |
| Fan out slices, attempts, or judgments to several agents | [parallel](playbooks/parallel.md) |
| Find what a change breaks outside its diff, or whether it is safe | [prove-outside-diff](playbooks/prove-outside-diff.md) |
| A large or ambitious run no narrower playbook fits | [open-ended](playbooks/open-ended.md) |

Every playbook starts by restating the goal and the problem in a few sentences, before any edit, so the user can correct the aim early. A task that changes kind mid-run ("now fix it") switches playbook at that point.

## Around the steps

| Layer | What | Role |
|---|---|---|
| Rules | `rules/core/` (always on) and topic rules by glob | Apply to the whole session, not one step |
| Hooks | `careful-guard`, `generated-file-guard`, `large-read-guard`, `session-start`, `notify-done` (opt-in) | Enforce at tool-call time, even when a step forgets |
| Agents | `context-harvester`, `explorer`, `planner`, `tdd-runner`, `implementer`, `reviewer`, `security-reviewer`, `bulk-reader` | Optional spawn in steps 3 to 6 for one bounded job. Results go back to this session, which keeps the steps |
| Focus | `get-moving`, `later-list` | Any step. A tangent goes on the later list, not into the work |

## Workflow combinations

Pick these in step 4. They are companions, not a replacement for the task skill.

| Condition | Chain |
|---|---|
| Independent tasks at once, competing solutions, or several judgments of one question | `rumbling` (Split, Contest, or Council), then `evidence` Judge on the combined result |
| Named checks must stay green across rounds, or the user said to loop until it passes | `loopy` around the task skill. Each round still uses that skill for the edit and `verify` for the check |
| One evidence-led pass, a plan with no edits, a read-only judge, a report rewrite, or a domain workflow | `evidence` in that mode. Not when the user asked to repeat until green (`loopy`) or only wants the check command (`verify`) |
| The user says continue or pick up | `handoff` Resume before step 3 |
| The user is back in a long chat, or no note exists and they ask what they were doing | `handoff` Catch up or Recall before step 3 |
| The task is unfinished, paused, or this session is ending | `handoff` Write after prove and before deliver |

Do not stack `loopy` and `evidence` Run on the same edit. `rumbling` already ends in `evidence` Judge. A single routine task does not start `rumbling`.

## One-shots

The user named a skill inside `/use-levistack` (for example "use-levistack: second-opinion on my branch"): run the machine check, then steps 1, 2, and 3 with that skill, then step 4 to confirm it and add a companion only when the table above matches. Then 5, 6, 6b, and 7. A bare `/skill` call without this router runs that skill alone. Prime, hunt, deliver, and the machine check do not run.

## Hard rules

1. Steps run in order. The machine check is first. Prime before invoke. Hunt on every run. Handoff Write, when it applies, comes after prove and before deliver. Deliver is last. Prime and deliver are two `output-savers` touches on two different targets. A blocked machine check does not continue into the task.
2. Closed catalog first. Go to skills.sh only through `find-skills` Upstream, and never install without a yes.
3. At most one round of questions in the whole run, at most three questions, each with a recommended answer. Read the workspace before asking.
4. Read-only skills (`codebase-learner`, `trace`, `second-opinion`, `challenge-me`) never edit code.
5. Push, open or update an MR or PR, post a comment, publish, install, or anything destructive: show exactly what will happen and wait for a yes.

## When the route gets stuck

| Symptom | Do |
|---|---|
| Two skills tie | Read both descriptions' "Not for" lines; the one that does not exclude the job wins |
| The opened skill does not fit | Say so, go back to step 3 or 4. Do not force it |
| The user is overwhelmed, not confused about skills | `get-moving` |
| Nothing fits | Say so plainly. Offer to do it directly, or `create-skill` if the job will repeat |

Example chains: [references/worked-chains.md](references/worked-chains.md).

## Related skills

- `setup-levistack`: the machine check before step 1. Follow it in full when the check is blocked.
- `find-skills`: step 4 on every run. It confirms the first skill and adds companions. It does not replace a named skill.
- `handoff`: resume at the start, or write the note before deliver when work remains.
- `rumbling`: parallel seats, then `evidence` Judge.
- `loopy`: repeat until the named checks pass.
- `evidence`: one pass, a plan, a judge, a report rewrite, or a domain workflow.
- `output-savers`: step 2 prime and step 7 last gate.
- `verify`: step 6 proof.
- `polyglot-copywriter`: step 7 prose for people.
- `codebase-learner`, `trace`, `second-opinion`, `challenge-me`, `ready-spec`: step 3 first picks.
- `get-moving`: the user is stuck on the work, not on the skill.
- `shape-and-build`, `blast-radius`, `figure-it-out`: picks inside the design-shape, prove-outside-diff, and open-ended playbooks.
- `help-levistack`: answers how to use the catalog without starting the work.
