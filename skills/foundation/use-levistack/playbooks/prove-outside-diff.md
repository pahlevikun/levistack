# Playbook: prove-outside-diff

Matches "what could this break", "blast radius", "is this safe to ship", "I don't trust this small diff", "review this before merge".

| Step | Do | Skill |
|---|---|---|
| 1 Restate | Say what the change does, including the part the diff does not spell out, before judging it | — |
| 2 Outside the diff | Find the one fact the change is safe because of, look where grep stops, and prove that fact by running real code | `blast-radius` |
| 3 Gates | The ordinary tests, lint, and build | `verify` |
| 4 Adversarial | When the change is wide or the user asked for a review. A finding stays only when a run proves it | `second-opinion` |

Read-only unless the user asks for a fix. A fix goes through the `bug-fix` playbook.

**Reply:** the safety fact with its proof or marked unproven, the confirmed risks with `file:line`, what was checked and cleared, and the cheapest check to run before merge.
