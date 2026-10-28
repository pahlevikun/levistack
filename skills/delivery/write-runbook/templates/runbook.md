# <Task or recovery goal>

Status: <draft, partly exercised, or verified scope>.
Owner: <responsible role or team>. Review date: <date>.
Applies to: <service, environment, and release range>.
Cadence: <established schedule, if applicable>.

## When to use this procedure

<Triggering symptom or task, intended outcome, scope, and conditions where another procedure applies.>

## Evidence and operating context

Source snapshot: <scripts, configuration, tests, incident records, and relevant revision>.
Working directory: <verified location>. Target: <account, environment, service, and artifact identifiers>.
Access: <required role and how to obtain it; no credential values>.

## Readiness

| Prerequisite | How to verify | Evidence needed | Stop or decision condition |
|---|---|---|---|
| <relevant requirement> | <actual command, record, or observation> | <expected result and currency> | <what blocks progression and who decides> |

<Include dependencies, current health, configuration, capacity, and backup/recovery checks where relevant. Mark unknown or unexercised prerequisites explicitly.>

## Procedure

### <Step ID>. <Action>

Precondition: <required observed state and any warning before the action>.

```text
<exact verified command or UI action, with named placeholders and their source>
```

Expected evidence: <tool result, output, relevant state, and how to observe it>.
Continue when: <observable condition>. Stop when: <failure or uncertainty condition>.
Failure handling: <diagnostic, recovery, or escalation and its success check>.
Repeat or resume: <safe replay conditions, partial-effect checks, or compensation>.

<Repeat for material actions. At each phase boundary, state the required evidence, promotion criteria, and stop/rollback decision.>

## Recovery limits

<Verified rollback target and actions, prerequisites, irreversible effects, data-loss boundary, and last reversible point. State when rollback is unavailable, incompatible, or untested.>

## Completion and observation

| Criterion | Observation or command | Expected result | Required scope and duration |
|---|---|---|---|
| <service or user outcome> | <verified check> | <source-backed value> | <actual required checks and observation window> |

<Explain full, partial, failed, unconfigured, and skipped checks. A required check that did not run cannot establish completion. Include supported cleanup and handoff conditions.>

## Troubleshooting and escalation

| Symptom or stop condition | Diagnostic evidence | Recovery or next decision | Escalation role and established channel |
|---|---|---|---|
| <searchable symptom> | <cheap discriminating check> | <action and observable success> | <verified contact or unresolved contact gap> |

## Exercise history and limitations

Last exercise: <actual date, environment, runbook revision, and attempt ID; or not exercised>.
Branches checked: <actual checks and results>. Not checked: <unrun paths and missing evidence>.
Last review: <document inspection date, distinct from execution>.

### Optional attempt record

Attempt ID: <unique identifier>. Runbook revision: <revision>.
Operator and target: <actual role and environment>. Times: <start/end with timezone>.

| Step | Action actually taken | Actual result and evidence | Deviation or uncertain effect | Decision and next checkpoint |
|---|---|---|---|---|
| <ID> | <redacted action> | <status, output, and evidence reference> | <what differed or remains unknown> | <continue, stop, recover, or escalate> |

<Do not fill actual-result fields with planned output. Preserve earlier attempts. Before resume, verify current target state and reconcile uncertain actions. Finish with recovery state, unmet criteria, and follow-up ownership.>
