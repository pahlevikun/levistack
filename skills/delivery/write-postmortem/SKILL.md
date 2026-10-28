---
name: write-postmortem
description: "Write blameless incident postmortems and near-miss reports with a full report template, measured impact, evidence-linked timeline, causal analysis, response review, and accountable corrective actions. Use when asked for an incident report, postmortem, outage review, RCA document, or after-action review after stabilization. Keeps uncertain causes and unverified claims explicit and checks action effectiveness. Not for live operations (write-runbook), a causal investigation without a report (trace), or a sprint retrospective."
metadata:
  version: 1.1.0
  author: levistack
  license: MIT
  group: delivery
  category: delivery
  department: delivery
  related_skills:
    - trace
    - write-runbook
    - create-tickets
    - diagram
    - infographic
    - polyglot-copywriter
  invokes:
    - skill: trace
      when: Incident mechanisms need an evidence-backed causal investigation
    - skill: diagram
      when: The incident report needs an evidence-backed technical causal or response-flow figure
    - skill: infographic
      when: The incident report needs an audience-facing impact or timeline visual with evidence and uncertainty preserved
  tags:
    - postmortem
    - incident-report
    - near-miss
    - timeline
    - impact
    - follow-up
  capabilities:
    - incident_postmortem
    - timeline_evidence_and_followups
    - structured_incident_report
    - causal_and_action_effectiveness_review
  languages:
    - en

---

# Write a postmortem

Record what happened after the immediate response has stabilized. Keep confirmed events separate from causal interpretation, recollection, and proposed follow-up work.

Start from [the full report template](templates/postmortem.md), or preserve an established incident format with equivalent coverage. For causal questions, recurrence, and an optional document review, read [analysis-and-review.md](references/analysis-and-review.md). Both support this standalone workflow; no general documentation skill is required.

## Establish the record

1. Confirm the incident or near miss, audience, scope, recovery state, and existing incident format. Follow local document locations and already authorized docs scope. Separate the incident's recovery state, the report's review state, and the completion of corrective work.
2. If the incident is active, prioritize the operational response and maintain a timestamped working record. Use an existing runbook for operations or `trace` for an unexplained cause. Do not present a final postmortem before stabilization.
3. Read primary incident logs, alerts, metrics, deployment records, support reports, relevant code changes, and scoped Git history. Check an existing diagnosis against its cited evidence instead of repeating the investigation without cause. Record the source, time range, snapshot, and missing records. Supplied facts can support a draft, but do not claim firsthand log review when no logs were available.
4. Lead with the expected service behavior, observed failure, affected users or operations, impact scope, and recovery state. State how counts were measured, including denominators and observation windows where relevant, or mark them unknown. Keep estimates, financial effects, data loss, and SLO breaches separate from verified measurements.

## Build the timeline and explanation

Distinguish impact start, first signal, detection, acknowledgement, mitigation, and recovery where those events are known. Include dates and timezones, especially across midnight. Name the event used for each interval. Calculate impact duration separately from detection-to-recovery time when the failure began earlier. Preserve estimates and uncertainty instead of manufacturing precise times.

Give each timeline event its evidence and relevant decision or observed result. Mark recollections and disputed events explicitly. A nearby deployment is not proof of causation. Label gaps instead of filling them with plausible events. Keep diagrams optional and source-backed.

When a visual helps, use `diagram` for technical flows or causal relationships, or offer `infographic` for an audience-facing impact or timeline visual. Choose one visual owner and pass the evidence, dates, uncertainty, and intended audience once. Do not cycle between the two skills or require a figure when prose suffices.

Explain the conditions that allowed the incident without blaming people. Separate the triggering event from contributing mechanisms and missing detection or prevention. Do not force a single root cause when the evidence supports interacting conditions, or when the trigger remains unknown.

Trace onset, detection delay, and recovery delay as separate causal questions when they differ. Ask why safeguards failed only where evidence establishes a gap. A five-whys exercise is a technique, not a required count or proof of causation. Keep unsupported explanations as hypotheses, with the evidence needed to resolve them.

Record misleading signals and failed response attempts when they change how the next responder should act. For a disputed cause, retain competing explanations and the evidence needed to decide. For a near miss, separate actual impact from hypothetical impact.

Assess what helped and what hindered recovery with concrete observations. Preserve why responders chose an action using what they knew then. Distinguish temporary mitigation, partial recovery, and confirmed restoration. Do not turn blameless language into an omission of factual actors, decisions, or failed attempts.

## Assign follow-up work

Each action needs a linked finding, accountable owner, intended outcome, and acceptance evidence. Classify its purpose as prevention, detection, or recovery when useful. Include priority, tracking, target date, and state when available. Mark unassigned owners, missing dates, and pending tracking explicitly. Prefer a focused fix at the supported mechanism over one task for every causal question.

Distinguish proposed actions from accepted or completed actions. Do not file external tickets, notify other people, or change the service unless that work is separately authorized. Link to operational improvements and decisions where those records exist.

Specify how completion will be checked and how effectiveness will later be assessed. Use an agreed review date or mark review pending. A closed ticket alone does not prove reduced recurrence or faster detection. Check related incidents for recurring mechanisms and whether earlier actions addressed them; do not invent an escalation policy.

## Output shape

Use the local incident format, or the full template's progression. Keep one action register; the prevention section explains its coverage rather than copying task status into another checklist.

```text
Incident metadata and separate incident/report states
Summary and measured impact
Timeline with evidence, decisions, and gaps
Failure explanation and contributing conditions
What went well and what could improve
Owned actions with acceptance and effectiveness checks
Lessons, related incidents, and prevention coverage
Supporting evidence, communications, and remaining uncertainty
```

## Verify

- Reconcile the timeline with primary records, check duration calculations, and test causal claims against the available evidence.
- Reconcile impact totals, units, denominators, and time windows with their sources. Do not infer no data loss or no security impact from silence.
- Use the organization's severity system. Mark severity unknown when no scheme or decision exists.
- Keep the report blameless while retaining accountable ownership. Sanitize client-facing records without removing facts needed to understand the incident.
- Preserve approved history and record later corrections or supersession visibly according to local policy.
- Distinguish report readiness from service recovery and remediation completion. An unknown cause can remain in a useful draft or reviewed report. Do not claim a review meeting, communication, ticket, or corrective action happened without evidence.
- Report what was checked and what remains a draft or hypothesis. Writing a postmortem does not authorize replaying a failure or performing production mutations to verify prose.

Behavior scenarios are in [evals/evals.json](evals/evals.json).

## Related skills

- `trace`: investigate a failure mechanism or disputed causal explanation.
- `write-runbook`: turn verified recovery lessons into an operational procedure.
- `create-tickets`: create follow-up tickets when the user authorizes that work.
- `diagram`: create an optional evidence-backed technical flow or causal figure.
- `infographic`: create an optional audience-facing impact or timeline visual from the same evidence.
- `polyglot-copywriter`: improve clarity without weakening evidence or uncertainty.
