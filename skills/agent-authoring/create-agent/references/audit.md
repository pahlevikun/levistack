# Audit checklist

Run `node scripts/lint.mjs <path>` first. It covers the mechanical checks marked (L). The rest need judgment. Score each item pass or fail, report `passed/total`, and list failures by priority.

## Subagents

| # | Check | |
|---|---|---|
| A1 | `name` is lowercase with hyphens and matches the filename | L |
| A2 | `description` exists and states **when** to call it | L (heuristic) |
| A3 | `tools` (or `readonly`) is the minimum that works; no write tools on a read-only job | L (heuristic) |
| A4 | `model` is pinned only for mechanical work | |
| A5 | The body names the inputs the caller must pass | |
| A6 | The body gives numbered steps, a verification step, and an output format | |
| A7 | The body has an explicit "Do not" list, including spawning other agents | |
| A8 | It does not overlap another agent in the roster | |
| A9 | It is under about 80 lines and links to rules instead of pasting them | L |
| A10 | No secrets, personal paths, or product names a stranger could not use | |

To audit a skill instead, use the `create-skill` skill.

## Report format

```
Score: 14/18

Broken
- A2: description has no trigger. Fix: "... Use after <x> or when <y>."

Weak
- A6: no verification step. Fix: add a final step that names the check and the output format.

Polish
- A5: the body never names the inputs the caller must pass. Fix: add an "Inputs" line.
```

- **Broken:** it will not load, will not trigger, or will do the wrong thing.
- **Weak:** it loads but misroutes, wastes context or is unverifiable.
- **Polish:** clarity and consistency.

Every finding gets a concrete fix. Say "no findings" when there are none; do not invent items to look thorough.
