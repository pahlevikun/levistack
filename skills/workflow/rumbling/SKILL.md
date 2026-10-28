---
name: rumbling
description: "Coordinate parallel agents on independent tasks, competing solutions, or one judgment question, then judge their combined result against evidence. Use when the user asks to rumble, dispatch multiple agents, compare parallel approaches, or convene a model-diverse council. Not for a single routine task or a read-only second opinion on one code change."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: workflow
  category: workflow
  department: workflow
  related_skills:
    - evidence
    - second-opinion
    - verify
    - use-levistack
  invokes:
    - skill: evidence
      when: All parallel workers have finished; Judge mode weighs reports against the actual artifacts and decision criteria
    - skill: verify
      when: The coordinator has integrated accepted work and must check the finished result
    - skill: second-opinion
      when: A consequential code change also needs an adversarial decision ledger before acceptance
  tags:
    - parallel-agents
    - contest
    - council
    - judge
  capabilities:
    - independent_task_fanout
    - parallel_candidate_contest
    - model_diverse_council
    - evidence_judged_synthesis
  languages:
    - en

---

# Rumbling

Run bounded agents in parallel, bring their work together, and make one evidence-backed call. The coordinator owns scope, integration, and the final answer. A worker's completion message is a lead to inspect, not proof that its result works.

## Pick the shape

| The user needs | Mode | Read |
|---|---|---|
| Different independent tasks finished together | **Split** | [split.md](references/split.md) |
| Several candidate solutions to the same task | **Contest** | [contest.md](references/contest.md) |
| Independent judgments about one decision or risk | **Council** | [council.md](references/council.md) |

If tasks depend on each other's output, sequence them instead of starting them together. If the user wants adversarial review and a decision ledger for one existing code change, use `second-opinion`. `rumbling` is the owner when the requested result is parallel work and one synthesized outcome.

## Shared contract

1. State the result, the artifact or question, the deadline or scale if given, and 3–6 observable decision criteria. Read project instructions and identify what workers may edit. Keep externally visible or destructive actions with the authorized owner; a worker cannot infer permission from a broad goal.
2. Define each seat before launch: input sources, exact scope, output path or report shape, constraints, checks, and a stop condition. Give workers enough context to stand alone. Use different models first for judgment-heavy work when the host supports them; use distinct perspectives after that. Never claim model diversity that the host did not provide.
3. Isolate writers in separate worktrees or non-overlapping output directories. Read-only investigators may share a checkout. Do not run workers concurrently against shared mutable files, live environments, or a dependent sequence. If isolation is unavailable, use read-only workers or sequence the work.
4. Launch the seats together. Track every seat as completed, failed, or missing. Inspect each report **and** its actual artifact. Ask the same worker for missing evidence when useful. Do not start final judgment while a seat is still writing.
5. Follow the selected mode's integration rule. Contest also asks Judge to compare candidates before choosing a base. Run the relevant checks on the integrated artifact or decision record. Then give a separate read-only agent `evidence` in **Judge** mode with the original criteria, every seat's result, the final artifact, and the checks. If no separate judge agent is available, run Judge yourself and disclose that independence was reduced. Reproduce a disputed claim if Judge and the coordinator disagree; revise the outcome or explain the evidence behind the final call.
6. Report one outcome: what each seat contributed, what was accepted or rejected and why, the Judge verdict, the checks observed, and material limits. A failed seat does not force a rerun when the remaining evidence is enough; name the dropout.

When the host has no subagent capability, do distinct sequential passes with the same briefs, then run the same integration and Judge steps. Say plainly that the run was sequential and had no agent or model diversity.

## Related skills

- `evidence`: frames observable completion and judges the finished work; its Judge mode is the final read-only gate here.
- `second-opinion`: adversarial code-change review with a decision ledger when the specific artifact warrants that deeper review.
- `verify`: runs fresh checks on the integrated artifact.
- `use-levistack`: selects the ordinary task skill for each worker's domain.

## Done when

- Every seat has a visible result or named dropout, and no writer is still running.
- The integrated artifact or decision has one coherent owner and has been checked as a whole.
- `evidence` Judge has issued a verdict with claim-level support or explicit limits.
- [evals/evals.json](evals/evals.json) covers all three modes and the main failure boundaries.
