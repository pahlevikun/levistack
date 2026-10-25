---
name: use-levistack
description: "Start here. The entry point that routes any prompt through levistack in seven fixed steps: route, prime, invoke, hunt, apply, prove, deliver. Picks the first skill (codebase-learner, trace, second-opinion, challenge-me, execution-ready-spec-plan, or a named one), hunts the catalog with find-skills when nothing obvious fits, runs the chain, proves every claim, and shapes the reply. Use when the user does not know which skill fits, says 'where do I start', 'help me with', 'what should I use', 'just handle it', gives a goal with no skill named, or types /use-levistack with a task. A named skill inside it runs as a one-shot."
---

# Use levistack

Do not stop at a recommendation. Run the steps below in order, top to bottom, for every prompt.

## Orchestration (run in order)

| Step | Do | Playbook | Skip when |
|---|---|---|---|
| 1 Route | Accept the prompt. If the user named a skill, mark it a one-shot | — | Never |
| 2 Prime | `output-savers` Step 0 on the **user's** prompt: safety override, job, reply level. Never rewrite their words | [prime.md](playbooks/prime.md) | Never |
| 3 Invoke | Pick the first skill from the intent map, or the named one-shot. No clear intent: go to step 4 | [invoke.md](playbooks/invoke.md) | Never |
| 4 Hunt | `find-skills`: gather what is missing, search the catalog, compose a chain of at most four skills, go upstream only for a real gap | [find-skills](../find-skills/SKILL.md) | Step 3 found the skill, or the user named it |
| 5 Apply | Run the chain. Load each skill when its step starts. Pass each result to the next in one sentence | the chosen `SKILL.md` files | Never |
| 6 Prove | `verify` before any "done", "fixed" or "passing". Every outward-facing action stops at the user | [prove.md](playbooks/prove.md) | Nothing was changed and nothing is claimed |
| 7 Deliver | `polyglot-copywriter` on prose a person will read, then `output-savers` last on **your** reply | [deliver.md](playbooks/deliver.md) | Never |

Never reorder. A claim without fresh proof does not enter the reply. An outward action without a yes does not run.

## Around the steps

| Layer | What | Role |
|---|---|---|
| Rules | `rules/core/` (always on) and topic rules by glob | Apply to the whole session, not one step |
| Hooks | `careful-guard`, `generated-file-guard`, `large-read-guard`, `session-start`, `notify-done` (opt-in) | Enforce at tool-call time, even when a step forgets |
| Agents | `context-harvester`, `explorer`, `planner`, `tdd-runner`, `implementer`, `reviewer`, `security-reviewer`, `bulk-reader` | Optional spawn in steps 3 to 6 for one bounded job. Results go back to this session, which keeps the steps |
| Focus | `get-moving`, `later-list` | Any step. A tangent goes on the later list, not into the work |

## One-shots

The user named a skill inside `/use-levistack` (for example "use-levistack: second-opinion on my branch"): run steps 1, 2, 3 with that skill, skip 4, then 5, 6 and 7. A bare `/skill` call without this router runs that skill alone; prime and deliver do not run.

## Hard rules

1. Steps run in order. Prime before invoke. Deliver after the work. Those are two `output-savers` touches on two different targets.
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

- `find-skills`: step 4 hunt and skills.sh installs.
- `output-savers`: step 2 prime and step 7 last gate.
- `verify`: step 6 proof.
- `polyglot-copywriter`: step 7 prose for people.
- `codebase-learner`, `trace`, `second-opinion`, `challenge-me`, `execution-ready-spec-plan`: step 3 first picks.
- `get-moving`: the user is stuck on the work, not on the skill.
