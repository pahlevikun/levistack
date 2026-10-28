# Postmortem: <incident title>

Incident reference: <existing ID or not assigned>.
Incident date and timezone: <date, timezone, or unknown>.
Authors and service owner: <confirmed people or roles, or pending>.
Severity: <organization's assigned level, or unknown>.
Incident state: <active, mitigated, monitoring, recovered, or the local state>.
Report state: <draft, under review, accepted, or the local state>.
Evidence checked: <snapshot and observation window; keep private source paths in working notes for external reports>.

<!-- Replace prompts with evidence-backed content. Mark unknowns or inapplicable sections explicitly. Never copy sample measurements into an incident record. -->

## Summary

<Describe expected behavior, the observed deviation, who was affected, the supported failure explanation, and how service was restored. Keep causal uncertainty visible. Write for a reader who was not present.>

## Impact

| Dimension | Observed effect | Evidence and measurement limits |
|---|---|---|
| Users and operations | <affected groups, count, rate, or unknown> | <source, denominator, time window, estimate method> |
| Service behavior | <errors, latency, unavailable functions, or other measured deviation> | <baseline and incident measurement> |
| Data and security | <verified loss, corruption, disclosure, verified absence, or not established> | <checks supporting the claim> |
| Business or SLO effect | <supported effect or unknown> | <record or calculation; distinguish estimates> |

Impact window: <first user impact to confirmed recovery, or known bounds>.
Detection interval: <impact start to the defined detection event, or unknown>.
Recovery after detection: <defined detection event to recovery, or unknown>.
<Show calculation assumptions. First alert and acknowledgement may be different events.>

## Timeline

All times use <timezone>. Include full dates when the incident crosses a date boundary.

| Time or bounds | Event or decision | Observed result | Source and confidence |
|---|---|---|---|
| <time> | <first impact, signal, detection, response, or recovery event> | <what changed or remained broken> | <primary record, supplied fact, recollection, or hypothesis> |

<Include relevant failed attempts, rejected hypotheses, partial recovery, communications already sent, and confirmation of restoration. Name unexplained intervals rather than inventing entries.>

## Failure explanation

Finding F1: <the supported mechanism, interacting causes, or cause still unknown>.
Trigger: <event or condition that initiated failure, with evidence, or unknown>.
<Explain why the evidence supports the mechanism. Separate what happened from why it could happen. A change preceding the incident is not proof of causation.>

Unresolved explanations: <hypotheses, evidence for and against each, and what would resolve them>.

## Contributing conditions

| Finding | Condition and effect | Evidence | Remaining uncertainty |
|---|---|---|---|
| <F2> | <what increased exposure, delayed detection, or hindered recovery> | <source> | <unknowns or none established> |

<Follow separate onset, detection, and recovery questions where useful. Do not force a list of assumed process failures.>

## What went well

<Describe specific actions, checks, tools, or decisions that helped, and the observed benefit. Factual ownership is compatible with blameless language. Do not invent praise to fill the section.>

## What could improve

<Describe observed gaps, misleading signals, unsuccessful attempts, or recovery limitations. Explain what responders knew at the time. Distinguish a counterfactual proposal from a measured missed opportunity.>

## Actions

| Action and linked finding | Purpose and intended outcome | Owner | Priority, target, tracking | State and completion evidence | Effectiveness review |
|---|---|---|---|---|---|
| <specific change; F1> | <prevention, detection, or recovery; observable result> | <confirmed owner or pending> | <actual values or pending> | <proposed, accepted, or completed; acceptance check> | <measure, reviewer, agreed date or pending> |

<Retain one authoritative action register. A proposed action is not an approved commitment. A completed deliverable is not proof that it worked. Do not file tickets, change systems, schedule meetings, or send messages merely to populate this table.>

## Lessons

<State a non-obvious lesson grounded in this incident and where it applies. Avoid promises that a single fix guarantees prevention.>

## Related incidents

<Link relevant prior records, explain the shared mechanism or material difference, and check what happened to earlier corrective actions. If no comparison was possible, say so.>

## Prevention and review

<Explain how the chosen actions cover the supported mechanisms and remaining detection or recovery gaps. Refer to the action register without duplicating its task list. State residual uncertainty and the agreed effectiveness review, or that review is pending.>

## Supporting material

<Include necessary sanitized log excerpts, graphs, calculations, implementation changes, or editable diagram source. Links must resolve for the intended audience. Never imply a linked record was inspected if it was unavailable.>

Communication record: <what was actually sent, when, to whom, and its evidence; omit or mark not supplied if unavailable>.

## Unknowns and verification limits

<List missing records, disputed facts, unverified causal claims, incomplete measurements, untested fixes, and actions not yet accepted or checked. Keep incident recovery, report review, and remediation status distinct.>
