# Requesting code review

Dispatch a reviewer with **git range + requirements** — not your session history. Review early, review often.

## When to request

**Mandatory:** after each task in subagent-driven development; after major features; before merge to main.

**Optional:** when stuck; before refactoring (baseline); after fixing a complex bug.

## How to request

1. **SHAs**

```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

2. **Dispatch** using [code-reviewer.md](code-reviewer.md) with `{DESCRIPTION}`, `{PLAN_OR_REQUIREMENTS}`, `{BASE_SHA}`, `{HEAD_SHA}`.

3. **Act on feedback:** Critical → fix now; Important → before proceeding; Minor → backlog; push back with reasoning when the reviewer is wrong.

## Workflows

- **Subagent-driven:** review after each task; fix before the next.
- **Executing plans:** review at task boundaries or checkpoints.
- **Ad-hoc:** review before merge or when stuck.

## Red flags

**Never:** skip review because "it's simple"; ignore Critical; proceed with unfixed Important; argue with valid technical feedback.

**If reviewer wrong:** push back with reasoning; show code/tests; ask for clarification.
