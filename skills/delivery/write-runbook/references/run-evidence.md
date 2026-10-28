# Exercise records and restart evidence

Use this when drafting a record for an authorized exercise, reviewing earlier attempts, or improving a runbook after a partial failure. The authoring skill does not execute the recorded actions by default.

## Separate the procedure from the attempt

Keep the runbook revision stable while recording what happened in each attempt. Follow the repository's existing record location. Use a unique attempt identifier so two runs cannot overwrite each other. A timestamp may help ordering, but is not sufficient uniqueness by itself.

Identify the runbook revision, target, release, operator, start and end times with timezone, and applicable authorization or change record when available. Distinguish document review, syntax checks, dry runs, tests, and actual exercises. Expected output is not execution evidence.

For each step, record:

- Step identifier and actual time.
- Action or command actually used, with sensitive values removed.
- Preconditions checked and current state observed.
- Actual output, tool exit status, and relevant protocol or business result.
- Comparison with the expected result and a result such as completed, failed, blocked, skipped, or uncertain.
- Evidence reference, deviation, and the decision to continue, stop, recover, or escalate.

Use only states that the evidence supports. A successful log writer cannot override a failed underlying command. For an HTTP action, distinguish a completed transport from the intended status, body, and business effect.

## Preserve evidence without exposing secrets

Capture only material needed to assess the step. Redact credentials, cookies, authorization headers, personal data, and private identifiers before placing captures in shareable or committed records. Do not recommend verbose request logging or echoing all command arguments as a default. Store approved sensitive evidence only in the established restricted location and link to it appropriately.

Keep original attempt records traceable. Add a correction or follow-up record instead of replacing the previous result with the expected outcome. Missing evidence remains missing. A template with empty fields is not a completed exercise.

## Document a safe restart

Record the last confirmed step and any action whose result is uncertain. Before retrying, require a current observation of the target and reconciliation of partial effects. State whether the action is safe to repeat, needs compensation, or requires an operator decision.

Include the resume preconditions in the procedure. A checkpoint can be stale after another operator, an automatic job, or a rollback changes the system. Avoid replaying a write simply because the process that issued it exited or timed out.

## Close the record

Report the criteria met, criteria not checked, unresolved effects, recovery state, and follow-up owner where known. Separate a partially exercised procedure from one whose required branches passed. Promote confirmed deviations into a proposed runbook correction, then verify that correction at the available safe level.
