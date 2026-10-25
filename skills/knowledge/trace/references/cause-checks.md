# Cause checks

Run every check on every chain before you accept a root cause. They catch the two common failures: a chain that sounds right but does not hold, and a chain that stops at a symptom.

## 1. Backward read

Read the chain from the root cause back to the symptom, as "therefore" sentences:

> Migration review does not check query plans, **therefore** the index was not in the migration, **therefore** the query does a full scan, **therefore** it takes 45 seconds, **therefore** the payment call times out, **therefore** checkout returns 500.

Every "therefore" must follow from the line before it, with no hidden step. If you have to add "and also…" to make a step work, a link or a branch is missing.

## 2. Counterfactual

For each link, ask: **if this cause had not been there, would the symptom still happen?**

- No: the link is necessary. Keep it.
- Yes: it is not the cause, or it is only one of several. Look for the other branch.

Run it on the root cause last: if the proposed fix had been in place, would this incident have happened? If yes, the root is wrong or incomplete.

## 3. Falsification

For each link, name the evidence that would **prove it wrong**, then look for that evidence.

| Link | Would be wrong if… | Looked at | Found |
|---|---|---|---|
| The query takes 45 s | the slow-query log shows it under 1 s | the slow-query log for the incident window | 44 to 47 s, so the link holds |

A link you could not try to falsify keeps its tier at `Inferred` or lower, whatever the story says.

## 4. Timeline

Causes come before effects. Check the dates:

- The commit, deploy, config change or data change that the chain blames must come **before** the first time the symptom was seen.
- If the symptom started before the blamed change, the chain is wrong, or that change only made it worse (a contributing factor).
- Use `git log --format='%h %ad %s' --date=iso`, deploy logs, and the first-seen time in error tracking.

## 5. Competing chain

Build at least one other chain that could explain the same symptom, and say why it lost:

> Competing: "The payment provider was slow that day." Lost because the provider's status page and our outbound-latency dashboard show normal times during the incident.

If you cannot rule the other chain out, both stay in the output as competing hypotheses. Do not pick the tidier one.

## 6. Human-error rule

If any link says a person made a mistake ("forgot", "misconfigured", "did not test"), it is never the root. Ask two more whys:

1. Why was the mistake **possible**? (no guard, no type, no default, no checklist)
2. Why was it **not caught**? (no test, no review step, no alert)

The answers are where the root cause usually sits.

## 7. Scope check

Ask whether the root cause explains **only this case** or **the whole class**:

- Other places with the same shape (other migrations, other test configs, other Dockerfiles): search for them. If they share the flaw, the root cause is confirmed and the fix must cover them too.
- If this is the only place with the flaw, the root may still be one why higher: why was this place different?

## Before you report

- Every link has a citation or a tier of `Speculative` with what would confirm it.
- The backward read has no hidden step.
- The root cause passes the counterfactual.
- The timeline holds.
- At least one competing chain was considered.
- No link stops at human error.
- "What we don't know" names specific gaps. If it is empty, be suspicious.
