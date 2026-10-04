---
description: "When and how to delegate to subagents: bounded ownership, disjoint writes, independent review, and parent-owned verification."
alwaysApply: false
---

# Delegation

Delegate when the project's orchestration allows it, the collaboration policy permits it, and the task can be bounded by explicit ownership and acceptance. An available specialist alone is not a reason to spawn. Do not ask whether to delegate after the plan is agreed; detect capability and proceed.

## Before dispatch, the parent records
- the working-tree state (`git status`) and task dependencies
- exact owned paths and interfaces, and prohibited paths
- the verification command
- relevant code-graph evidence and its coverage gaps

Tell every worker that other work may exist in the shared checkout, that it must preserve it, and that it must **not** dispatch another worker.

## Parallel work
- Parallel implementation needs **disjoint write ownership** and no producer or consumer dependency.
- Never let two workers edit the same file, migration, router, shared interface, lockfile, generated artifact or overlapping test surface. Otherwise run sequentially.
- Create no branch, worktree, commit, push or external side effect without explicit authorization.

## Review
- An implementer's self-review does not replace an independent one.
- A separate **read-only** reviewer returns both a contract and spec compliance verdict and a quality, architecture and security verdict.
- Send material findings back to the owning implementer, then re-review only the fix.
- The parent integrates everything and runs fresh repository-level verification.

## No delegation available
If the runtime has no safe delegation or task tracking, keep the same task brief and review gates but execute sequentially in the parent session. Never invent tool names or weaken evidence because a runtime differs.

See the `coordinator` agent for routing and `workflow` for the overall loop.
