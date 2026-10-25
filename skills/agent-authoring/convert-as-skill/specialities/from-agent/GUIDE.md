# From an agent

A subagent and a skill are different tools. Converting one loses isolation and `tools`, so decide keep / wrap / convert **before** copying. Do not treat an agent like a rule.

Detail: [subagent.md](subagent.md). Script: `scripts/convert.mjs` (add `--fork` to wrap).

## Keep, wrap or convert?

| Goal | Do |
|---|---|
| Give a subagent a `/name` entry point, or let the model load it | **Wrap**: keep the subagent, add a thin skill with `context: fork` that tells it what to do |
| Its knowledge should load into the current context, no isolation needed | **Convert** (copy the body; list any "you are a separate agent" line edits) |
| It exists to isolate noisy work, restrict tools or use a cheaper model | **Keep it a subagent** |

Default to keeping or wrapping. Convert only when isolation and the tool list do not matter.

## Steps

1. Read the subagent. List the fields from [subagent.md](subagent.md) that would be lost and say so to the user before converting.
2. Preview: `node scripts/convert.mjs agents/<name>.md --out <skills-dir> --dry-run` (add `--fork` to keep it isolated). The script refuses PDFs and skill folders.
3. Rewrite the description if it only says when to call an agent. Fix any body lines that speak as a separate agent ("Return a summary to the caller"). Those edits are the one allowed deviation from a straight copy; list them.
4. Convert, lint with the `create-skill` linter, and try it on the task the agent was built for.
5. Keep the subagent file until the skill has been tried. Roster docs (for example `docs/agents/README.md`) must change only if the agent is removed, and removal is the user's call.

## Do not

- Skip the keep / wrap / convert question.
- Convert an isolation-first subagent into an inline skill without saying what is lost.
- Harvest a conversation or distill a document on this path.
