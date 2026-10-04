---
description: "Default work loop for non-trivial tasks: gather context, plan only if needed, implement, test, review, check the goal."
alwaysApply: false
---

# Work loop

Classify the task first.

- **Direct:** the flow already exists and the change is bounded. Implement it, with no plan or spec files.
- **Planned:** several steps, a new flow or an architecture choice. Write **one** plan (not a spec and then a plan), with an eval per task.

Then:

`gather context → (plan, if Planned) → implement → focused test → review → security review when relevant → goal check`

- Loop back to implementation when tests fail, review finds an issue or the outcome is incomplete.
- Keep architecture and security judgment in the primary model. Delegate only bounded bulk reads and mechanical template fills to the cheap agents (`bulk-reader`, `template-writer`).
- Use the agents in `agents/` by role: `explorer`, `planner`, `implementer`, `tdd-runner`, `reviewer`, `security-reviewer`.
- Do not auto-commit or auto-push.
- Write reusable context back to the docs only when it is genuinely reusable.
