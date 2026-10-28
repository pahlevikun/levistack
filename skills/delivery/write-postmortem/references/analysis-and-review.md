# Check the explanation and follow-up

Use this when an incident's explanation is shallow, sources disagree, earlier incidents recur, or a document review needs structure. It supports incident writing; `trace` owns a separate causal investigation.

## Follow evidence through the failure

1. Start with the deviation from expected behavior and the primary observations. Identify which claims are measured, supplied, recalled, inferred, or still hypothetical.
2. Separate the triggering event, the failure mechanism, and conditions that changed its impact. A deployment before an outage is a lead, not a causal conclusion.
3. Investigate onset, detection delay, and recovery delay independently when they have different explanations. Do not force every branch into one root cause or ask exactly five questions.
4. For each causal link, state its supporting evidence, any conflicting evidence, and the limit of the conclusion. Stop at unsupported links and record what evidence would settle them.
5. Ask about safeguards and operational decisions without assuming they failed. A missing check is a finding only when the evidence establishes its relevance to the incident.

Useful questions include:

- What changed, and what evidence connects that change to the observed failure?
- What was visible before impact, at detection, and during recovery? Which signals reached responders?
- Which limits, dependencies, configuration, or data conditions affected the mechanism?
- What information and options did responders have when they chose an action?
- Did a mitigation restore user behavior, only reduce impact, or restore code while leaving harmful state behind?
- Which parts of the explanation remain disputed or need a separate investigation?

Describe factual actions and ownership without moral judgments. Replacing a person's name with "the process" does not make an unsupported claim true. Keep the actual decision and outcome, then examine the conditions around it.

Do not turn hindsight into certainty. A proposed alert, canary, or runbook might help future incidents; prove a claim that it would have prevented this incident before presenting that claim as established.

## Check impact and chronology

- Define incident start and recovery from user-visible behavior when known. Keep first alert, acknowledgement, mitigation, and restoration as distinct events.
- Use consistent timezone and date boundaries. Name the anchors for every interval, especially when different teams use "detection" differently.
- For rates and counts, check the observation window, denominator, units, rounding, and deduplication where relevant. Mark estimated business effects and explain their basis.
- Silence is not evidence that data loss, security impact, customer communication, or prior warnings were absent.

## Make actions testable

Map each proposed action to a finding and observable outcome. Prefer the smallest supported change that addresses the mechanism, improves detection, or reduces recovery time. An investigation can be a valid action when its output and decision criterion are clear.

Use confirmed ownership and dates. When either is missing, record the gap. Follow the organization's priority and escalation policy instead of inventing a deadline or treating every action as a closure blocker.

Distinguish these checks:

- **Completion:** the promised deliverable exists and its acceptance check passes.
- **Effectiveness:** later evidence shows the intended improvement, or records that the result remains uncertain.

An action's status, test result, measured outcome, and review date are different facts. Record them separately. A closed issue is not enough evidence of prevention.

## Review without inventing a meeting

When a review is requested, use a document-first sequence:

1. Correct the chronology, calculations, sources, and unknowns.
2. Challenge causal links, alternative explanations, and hindsight claims. Preserve unresolved disagreement.
3. Check that actions address the findings and have meaningful acceptance and effectiveness criteria.
4. Agree actual owners, priorities, dates, and a follow-up review according to local policy. Record pending decisions rather than making commitments for absent people.
5. Record accepted changes and preserve the report's history. Keep report acceptance, incident recovery, and corrective-action completion separate.

Retain useful lessons about successful decisions as well as failures. Compare related incidents by mechanism, not only by service name, and inspect whether prior actions were completed and effective.

A draft agenda is not a conducted review. Writing an action is not filing a ticket. A communication appendix records messages already sent; it does not authorize new messages.
