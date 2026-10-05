# Audit checklist

Run `node scripts/lint.mjs <path>` first. It covers the mechanical checks marked (L). The rest need judgment. Read the whole agent file before scoring. Score each item pass or fail, report `passed/total`, and list failures by priority.

## Subagents

| # | Check | |
|---|---|---|
| A1 | `name` is lowercase with hyphens and matches the filename | L |
| A2 | `description` exists and states **when** to call it | L (heuristic) |
| A3 | `tools` (or `readonly`) is the minimum that works; no write tools on a read-only job | L (heuristic) |
| A4 | `model` is pinned only for mechanical work | |
| A5 | The body names the inputs the caller must pass, and says what to do when one is missing | |
| A6 | The body gives numbered steps, a verification step, and an output format | |
| A7 | The body has an explicit "Do not" list, including spawning other agents | |
| A8 | It does not overlap another agent in the roster | |
| A9 | It is under about 80 lines and links to rules instead of pasting them | L |
| A10 | No secrets, personal paths, or product names a stranger could not use | |
| A11 | It never needs to ask the user: no `AskUserQuestion`, no "wait for confirmation"; open questions go in the report | L |
| A12 | The role is a specific specialty, not "a helpful assistant" | |
| A13 | The description is differentiated from neighboring agents (what it does and does not cover) | |
| A14 | The report says what was covered and what was not; a failure is stated, not hidden | |
| A15 | Where it can fail (network, missing file), the prompt names a fallback or a stop | |

To audit a skill instead, use the `create-skill` skill.

## Judge function, not style

- Before saying a section is missing, search the whole file for the same content under another name ("Approach" for "Steps", "Boundaries" for "Do not"). Flag missing function, never a missing heading.
- Do not flag a formatting preference that does not change behavior.
- Apply context:

| Type | Weigh |
|---|---|
| Simple (one task, few tools) | Focus areas may be implicit; a short prompt is fine; light error handling is enough |
| Complex (several steps, external systems, risk) | Missing constraints, output format and error handling are real defects |
| Delegating (it calls other agents) | Context handling and a success definition become important |

Tier the findings by effect:

- **Critical:** the description has no trigger; a generic role; no steps; no boundaries; more tools than the job needs; it needs a user it cannot ask.
- **Recommended:** focus areas, an output format, a done condition, a model that fits the work, error handling, an example.
- **Optional (note, do not flag as missing):** a context strategy for long-running agents, thinking guidance, caching order, a test plan, logging.

## Report format

Cite `file:line` for every finding, and check the numbers against the file before you report. Say why each finding matters for this agent.

```
Score: 12/15

Assessment
One or two sentences: is it fit for purpose, and what is the main point?

Broken
- A2 (agents/x.md:3): description has no trigger. Fix: "... Use after <x> or when <y>."

Weak
- A6 (agents/x.md:14): no verification step. Fix: add a final step that names the check and the output format.

Polish
- A5 (agents/x.md:9): the inputs the caller must pass are never named. Fix: add an "Inputs" line.

Strengths
- The "Do not" list at agents/x.md:30 is concrete and complete.

Context
Type: simple. Tools: appropriate. Model: appropriate. Effort to fix: low.
```

- **Broken:** it will not load, will not trigger, or will do the wrong thing.
- **Weak:** it loads but misroutes, wastes context or is unverifiable.
- **Polish:** clarity and consistency.

Every finding gets a concrete fix. Say "no findings" when there are none; do not invent items to look thorough. Make no edits during an audit.
