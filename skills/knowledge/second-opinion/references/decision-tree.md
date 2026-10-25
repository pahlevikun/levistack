# Decision tree

Every question in a second-opinion review is a node in one decision tree. The review ends only when no node is open.

## Node states

| State | Meaning | Source tag |
|---|---|---|
| **open** | Not decided yet. It blocks every node that depends on it | none |
| **resolved** | Decided | `user` (the user answered or confirmed a recommendation), or `inferred: <path>` (the code, a commit, a PR body or an existing doc settled it) |
| **DEFERRED** | The user chose not to decide it now | the reason the user gave, in their words |

DEFERRED is not the same as open. It does not stop the review from ending, and it shows in the ledger with its reason.

## Node types and dependencies

| Node | Depends on | Created when |
|---|---|---|
| N1 Intent: the change in one paragraph | nothing | always, first |
| N2 Scope: which diff and files | N1 | always |
| N3 Focus: what to weight or skip | N2 | the diff touches several areas or a trust boundary |
| N4 Risk: where the code runs | N2 | not clear from the code |
| N5 Merge pressure | N1 | the change could get structural findings |
| N6 Known gaps | N2 | a feature branch, or TODOs in the diff |
| Q-n Reviewer question | N1, N2, and the finding it affects | a reviewer could not judge without it |
| F-n Finding decision: fix now, follow-up, leave, or dismiss | N4, N5, and every Q-n on that finding | each Act on and Consider finding |
| F-n.fix Which fix | F-n resolved as "fix now" | the finding has more than one reasonable fix |
| T-n Term: what a project word means here | none | the user and the review had to pin a domain term down |

A node is **ready** when every node it depends on is resolved or DEFERRED. Never ask about a node while one of its dependencies is still open. That question comes too early.

## Resolve loop

1. Take the ready open nodes in this order: N1 to N6, then Q-n, then F-n (Act on before Consider), then F-n.fix.
2. **Read before you ask.** If a quick read answers the node (the diff, `git log`, the PR or MR body, a config file, `CONTEXT.md`, an existing decision record), mark it resolved with `inferred: <path>` and do not ask.
3. If not, ask **exactly one question** about that one node. Keep it tight: yes or no, or a short list of choices. Use the shape from `SKILL.md`, with a recommended answer and one sentence of reasoning. `question-bank.md` has ready-made questions for each node type.
4. Wait. The user can confirm, pick another choice, push back, or defer. On pushback, check the code again before you ask again.
5. Record the answer on the node and re-check which nodes are now ready. An answer can create nodes (a reviewer question can open a new finding) or close them (an answer can dismiss a finding).
6. Repeat until no node is open.

One question can resolve many nodes only when it says so: "Take my recommendation on all six Consider findings, and only raise the ones you disagree with?" A yes resolves each of those nodes with source `user (accepted recommendation)`.

## Decision ledger (always)

The resolved tree as a flat list the user can paste into a PR, MR or plan doc. One line per node, in resolve order:

```
- Intent - <one line> - user
- Scope - main...feature/export, 9 files, generated client excluded - inferred: git diff --stat
- Risk - production hot path - user
- Q1 Can userId be null from the cron job - no, the job filters it - inferred: jobs/export.ts:41
- F2 Missing retry on the webhook call - fix now - user
- F2.fix - wrap the call in the existing withRetry helper - user
- F5 Rename ExportSvc - DEFERRED - "after the billing launch"
```

Do not wrap it in a prose summary. Do not hedge inside it.

## CONTEXT.md (offer when terms were pinned down)

Offer it when the review had to pin down project-specific terms (T-n nodes). Do not force it.

- If the repo has a `CONTEXT.md`, merge new terms into it **in place and in its existing format**. Never overwrite or reorder existing entries.
- If there is none, create it with one term per line: `term - what it means here`, in the project's own words.
- Monorepo: if `CONTEXT-MAP.md` exists, write to the bounded context it names.
- Domain words only. No implementation details.

## Decision records (offer for contested or hard-to-reverse nodes only)

Offer one record per node that a future reader would question: the user overrode a recommendation, the reviewers disagreed, or the choice is hard to undo (a data shape, a public API, a guard kept on purpose). Skip the obvious ones. A record for a small choice is noise.

- Use the repo's existing folder: `docs/adr/` or `docs/decisions/` if either exists. Otherwise create `docs/decisions/`.
- Read the folder first and number from the highest existing record (`NNNN-slug.md`), so two records never collide.
- Each record holds the context, the choice, the options turned down, and why. Keep it short and in the project's own words, not a generic template.

Write either file only after the user says yes. Name every file you wrote in the output.
