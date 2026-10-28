# Deployment and cutover procedures

Document the release path the service actually uses. Do not choose a platform or add deployment infrastructure merely to fill the runbook.

## Establish preflight evidence

Record the exact artifact or revision, destination, current release, operator role, dependencies, and approved change scope. Verify target identifiers before commands can change traffic or data. List relevant configuration changes and secret references without storing their values.

Define readiness from available release records, tests, migration checks, observability, capacity, and backup evidence. State how recent each piece of evidence must be according to local policy. A green build is one input; it does not prove that a backup can be restored or that the destination is healthy.

Use the real service thresholds and their sources. For each metric, identify the baseline, allowed change or absolute limit, sampling window, and observation location. Keep promotion criteria distinct from emergency stop or rollback criteria. Unknown thresholds remain a readiness gap.

## Document the phase boundaries

| Phase | Evidence required before the next phase | Failure handling to document |
|---|---|---|
| Prepare | Correct artifact and target, required checks, configuration, compatible dependencies, and recovery prerequisites | Stop for missing or failed required checks; name the decision owner for uncertainty |
| Apply | Actual deployment or migration result and current target state | Reconcile partial effects before retry; identify the last reversible point |
| Promote | Intended release is healthy at the destination that will receive traffic | Preserve the previous viable target when supported; specify exact stop and recovery conditions |
| Observe | Service, dependency, and user outcomes meet the established criteria for the stated window | Identify whether to hold, revert, compensate, or escalate, and what proves recovery |
| Handoff | Intended release is active, unresolved work has an owner, and cleanup conditions are satisfied | Retain necessary recovery capacity and monitoring until local retirement conditions are met |

Each phase uses the service's actual actions and artifacts. An inactive deployment must be checked at its own address; testing the existing live release does not verify the new one. In a gradual rollout, state the real increments and the evidence needed between them rather than assuming a universal percentage sequence.

## State rollback limits before cutover

Identify the rollback target and verify its compatibility with schema, configuration, data, and in-flight work. An application version reversal may be insufficient after a migration. A backup restore can discard later writes. Traffic reversal does not undo external side effects.

Document the command or UI action, its prerequisites, maximum recoverable data boundary, expected recovery evidence, and situations where rollback is no longer appropriate. Mark an unknown or untested path explicitly. Do not promise zero downtime, instant recovery, or a recovery duration without evidence.

If an action times out, first establish whether it took effect. Document a safe repeat only when the tool's or operation's semantics support it. Otherwise give reconciliation, compensation, or escalation instructions. A prior success marker alone cannot justify skipping current-state verification.

## Complete and maintain the procedure

Specify final release identity, service health, required user-flow checks, and any applicable migration or backlog checks. Record which checks were executed and their scope. Skipped, missing, or unconfigured required checks remain incomplete.

Keep retention, cleanup, and the end of the recovery window tied to existing policy or an explicit decision. Include operator handoff and established escalation contacts when needed. Draft publication or stakeholder messages only when requested; writing the runbook does not send them.
