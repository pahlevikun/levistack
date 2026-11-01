# Playbook: investigate

Matches "how does X work", "why is X like this", "explain", "teach me", "walk me through", "help me understand this change". Read-only. It produces a cited explanation or a recommendation, not a code change.

| Step | Do | Skill |
|---|---|---|
| 1 Restate | Say the question and what a good answer lets the user do, in two sentences, before reading code | — |
| 2 How | Explain what the code does now: the flow, the owners, where things live | `codebase-learner` (explain mode) |
| 3 Why | Only when the question is about reasons, history, or whether a guard is still needed | `trace` (rationale mode) |
| 4 Explain | Merge the two into one plain explanation: overview, the parts, how they connect, where they live, the gotchas. Use a decision table when the question picks between options | — |
| 5 Deliver | Prose for a person goes through the deliver step | `polyglot-copywriter` |

Skip step 3 when the user only asked how. Skip step 2 when the code is already explained in this chat and the question is only why.

No edits, no MR, no `shape-and-build`. If the answer leads to a change, stop and offer the `feature` or `bug-fix` playbook. If the premise is wrong, say so with the evidence.

**Reply:** the explanation with `file:line` citations, and one line on what was not checked.
