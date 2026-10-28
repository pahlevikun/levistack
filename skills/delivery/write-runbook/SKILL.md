---
name: write-runbook
description: "Write operational runbooks for recovery, troubleshooting, deployment, and migration, with verified prerequisites, phase gates, commands, expected evidence, rollback limits, checkpoint recovery, and escalation. Use when asked to create or revise a runbook, recovery procedure, deployment checklist, operational playbook, migration guide, or troubleshooting procedure. Not for executing production operations, a postmortem (write-postmortem), or an implementation plan (write-plan)."
metadata:
  version: 1.1.0
  author: levistack
  license: MIT
  group: delivery
  category: delivery
  department: delivery
  related_skills:
    - create-documentation
    - write-postmortem
    - write-plan
    - verify
    - polyglot-copywriter
  invokes:
    - skill: verify
      when: Runbook commands or recovery branches need safe local verification
  tags:
    - runbook
    - recovery
    - migration
    - operations
    - deployment
    - phase-gates
    - resume
  capabilities:
    - runbook_authoring
    - recovery_and_branch_verification
    - deployment_phase_and_rollback_gates
    - resumption_and_redacted_run_evidence
  languages:
    - en

---

# Write a runbook

Write for an operator who must act under pressure. A documentation task does not authorize the operation itself.

## Establish the operating context

1. Identify the triggering symptom or scheduled task, affected system, intended outcome, operator role, and limits. Use the existing runbook format and document location. Record its owner and review date. Keep those separate from the last actual exercise and its result. Add recurrence only when the task has an established schedule.
2. Find an existing procedure before creating a second owner. Read current scripts, configuration, tests, operational records, and relevant Git history. Check earlier incident lessons and plans where they explain dependencies. Record source locations and the revision checked. Search connected knowledge sources read-only when relevant and available.
3. Verify prerequisites against the actual tooling. Identify the target account, environment, service, release artifact, working directory, and required access where relevant. Include current health, backups, and dependencies where they matter. Name the established escalation route and confirm contact currency from available records. Leave unavailable values explicit and say how to obtain them.
4. Continue within the user's authorized documentation scope without another approval pause. Keep service code unchanged. Execution of production or destructive steps needs its own authorization.

## Build the procedure

Write the shortest usable sequence. For every material action, provide the exact command or UI action, expected evidence, and what to do when the result differs. Keep prerequisites and conditions before the step they guard.

Give steps stable identifiers. At a phase boundary, state what evidence permits continuation, what stops the procedure, and who decides when the result is uncertain. Derive metric thresholds, observation windows, backup requirements, and rollout increments from the target service's policies or configuration. Missing values are unresolved gates, not permission to substitute generic numbers.

Put a destructive or irreversible consequence immediately before its action. Explain a required order when reversing steps can cause failure. Do not repeat the full sequence in a second overview.

Give a stop condition and recovery path for each state-changing stage. State when rollback cannot restore data or undo an external effect. Do not invent a rollback command to fill a template.

Document whether a step can be repeated safely. After an interruption or timeout, require the operator to inspect current state and reconcile any uncertain outcome before resuming. A saved checkpoint identifies prior evidence; it does not prove that the target still has that state. Explain compensation or escalation where replay is unsafe.

Finish with observable service and user checks. Include cleanup or a monitoring period when supported by the system. Name the evidence that allows the operator to stop or escalate.

Use a troubleshooting table for branching symptoms. Start with the searchable symptom, give a cheap diagnostic, then the recovery action and its success check. Avoid speculative causes without a way to distinguish them.

For a migration, add old-to-new mappings, caller changes, cutover conditions, rollback limits, and treatment of unmigrated callers. Record dates and retirement conditions only when established.

For a deployment or cutover, read [deployment.md](references/deployment.md) for preflight, promotion, rollback boundaries, and handoff. When the document needs an exercise record or must learn from an interrupted attempt, read [run-evidence.md](references/run-evidence.md). These references describe the operator's evidence requirements; they do not authorize execution.

## Output shape

Use the local format, or start from [the runbook template](templates/runbook.md). Its minimum shape is:

```text
Task and when to use it
Scope, environment, access, prerequisites
Procedure: action, expected evidence, stop or recovery condition
Completion checks
Recovery and escalation
Phase gates and restart conditions where applicable
Last exercise: date, environment, branches checked, limitations
```

Use exact commands, paths, units, and system names. Label placeholders and explain where the operator obtains their values. Exclude credentials and personal data from examples.

## Verify

- Check commands against installed tools, scripts, tests, or documented interfaces. Exercise safe paths in a local or disposable environment when available.
- Distinguish syntax checks, dry runs, tests, and live exercises. Label examples and branches that were not run. A dry run does not prove a destructive rollback works.
- Define the meaning of tool outcomes. A required probe that failed, never ran, is unconfigured, or rejected its arguments cannot pass a gate. Record partial coverage separately from full success. Confirm that logging or capture pipelines preserve the actual command result; an HTTP client exit alone may not establish the expected HTTP or business outcome.
- Do not contact production, execute a destructive command, or reproduce an outage merely to prove prose. If only production can exercise a branch, retain a draft or explicit verification limitation.
- Check completion, stop, rollback, and escalation conditions against the source. Open links and review the procedure as an operator without author context.
- Where possible, have a reader unfamiliar with the task rehearse the safe path. Record which prerequisites or branches could not be exercised. Update the procedure from confirmed deviations without overwriting earlier execution evidence.
- Deliver the document, evidence snapshot, branches exercised, and remaining limitations. An untested recovery sequence remains a draft or carries an explicit limitation.

Keep publishing, announcements, external ticket updates, and execution outside the authoring task unless separately requested. An execution-only request belongs to the applicable operator workflow; do not disguise it as a documentation check or impose a new approval count of your own.

Behavior scenarios are in [evals/evals.json](evals/evals.json).

## Related skills

- `verify`: investigate a failing check or run safe authorized validation.
- `write-postmortem`: record an incident after stabilization and preserve its recovery lessons.
- `write-plan`: plan implementation work that makes a proposed operational path possible.
- `create-documentation`: document ordinary product use and reference material.
- `polyglot-copywriter`: clarify operator instructions while preserving exact commands and consequences.
