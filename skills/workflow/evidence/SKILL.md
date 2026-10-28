---
name: evidence
description: "Frame a concrete goal, run an evidence-led task, or judge completed work against claims and checks. Use when asked for an evidence workflow, a reusable goal prompt, a read-only judge of one artifact or parallel agent results, an evidence-based report rewrite, or a domain workflow. Not for routine test execution (verify) or an adversarial code-change decision ledger (second-opinion)."
metadata:
  version: 1.1.0
  author: levistack
  license: MIT
  group: workflow
  category: workflow
  department: workflow
  related_skills:
    - use-levistack
    - verify
    - second-opinion
    - rumbling
    - create-skill
    - convert-as-skill
    - diagram
    - infographic
  invokes:
    - skill: verify
      when: Run mode needs fresh claim-matched checks or Report mode has a checkable claim
    - skill: second-opinion
      when: A consequential code change needs an adversarial decision review
    - skill: create-skill
      when: Domain mode creates a new skill without existing source material
    - skill: convert-as-skill
      when: Domain mode adapts or merges existing skill material
    - skill: diagram
      when: Domain mode needs a technical flowchart that text cannot show clearly
    - skill: infographic
      when: Domain mode needs an evidence-based audience-facing visual workflow
  tags:
    - evidence
    - goal
    - plan
    - judge
    - audit
    - domain-skill
  capabilities:
    - observable_goal_framing
    - explicit_evidence_workflow
    - read_only_claim_judge
    - parallel_result_judgment
    - domain_skill_routing
  languages:
    - en

---

# Evidence

Use this entry point when the user asks to frame, run, or judge work through evidence. Keep each mode separate. A request to judge existing work stays read-only; a request to run a task may edit within its authorized scope.

## Select a mode

| Request | Mode | Read |
|---|---|---|
| "Turn this idea into a goal", "write a goal prompt for a fresh session" | **Goal** | [goal.md](references/goal.md) |
| "Use evidence to do this task", "run the evidence workflow", or "run the evidence loop" | **Run** | [run.md](references/run.md) |
| "Evidence plan" or "evidence workflow plan" | **Plan** | [run.md](references/run.md), stop before changes |
| "Audit the evidence", "judge this work", "judge these agent results", or "judge suite" | **Judge** | [judge.md](references/judge.md) |
| "Rewrite the evidence report" | **Report** | [report.md](references/report.md) |
| "Build a domain workflow" or "make a domain adapter" | **Domain** | [domain.md](references/domain.md) |

The modes share three rules. State what result would count as done. Read the actual source of each fact before using it. Match every completion claim to a check run on the finished artifact. A source conflict or missing verification stays visible in the result. Goal writes a prompt for a later session only when the user requests that prompt; otherwise Run carries out the task here.

Use the project's instructions and the matching task-specific skill inside Run. Do not replace a specialized security, medical, legal, finance, deployment, or incident procedure with this general workflow. Reversible local edits follow the user's task authorization. Posting, publishing, pushing, deploying, installing, and destructive actions require authorization for the exact action.

## Related skills

- `use-levistack`: default catalog entry point when the user did not request this workflow.
- `verify`: run fresh, claim-matched checks and report limits.
- `second-opinion`: challenge a code change with independent reviewers and resolve its decision ledger. Judge checks claims and artifacts; it does not replace that review.
- `rumbling`: coordinate parallel agents on independent tasks, competing solutions, or one judgment question, then hand their completed results to Judge.
- `create-skill`: author a new domain skill with evals and catalog metadata.
- `convert-as-skill`: adapt or merge existing domain material rather than inventing a new skill.
- `diagram`: draw a technical flowchart when branching needs a figure.
- `infographic`: explain an evidence-backed workflow visually for its audience.

## Done when

- The requested mode produced its own result without leaking into another mode.
- Every stated fact names evidence, and every completion claim names a fresh check or an explicit limit.
- [evals/evals.json](evals/evals.json) covers the entry modes, parallel-result judgment, and requests that should use another skill.
