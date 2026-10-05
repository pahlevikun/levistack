# Skill audit checklist

Run the linter first (see `SKILL.md`). It covers the mechanical checks marked (L). The rest need judgment. Read the whole skill (`SKILL.md` and every file it links) before scoring. Score each item pass or fail, report `passed/total`, and list failures by priority.

## Checks

| # | Check | |
|---|---|---|
| S1 | `name` matches the folder and follows the spec (1 to 64 chars, a-z, 0-9, hyphens) | L |
| S2 | `description` is 1 to 1024 chars and has a "when to use" part | L |
| S3 | The description is specific enough to separate it from neighboring skills | |
| S4 | `SKILL.md` is under 500 lines | L |
| S5 | Principles live in `SKILL.md`, not only in a reference | |
| S6 | Every linked file exists and links are one level deep | L |
| S7 | Steps are actions with an observable result, not platitudes | |
| S8 | There is a verification step or success criteria | |
| S9 | One term per concept; one default with at most one escape hatch | |
| S10 | Invocation is set deliberately (`disable-model-invocation` for side effects) | |
| S11 | Scripts are self-contained and fail with clear messages | |
| S12 | No duplicated content across files; no unused files | |
| S13 | It was tested on real requests, including one that should not trigger | |
| S14 | The description is third person and has no first or second person ("I can help you") | L |
| S15 | No hedged obligations ("try to", "generally", "you might want to"); decisions come with criteria | |
| S16 | Freedom matches fragility: exact commands for fragile steps, principles for judgment calls | |
| S17 | Edge cases are answered (empty input, nothing found, duplicates, failure) | |
| S18 | Claims about tools, APIs and versions carry a date or a source | |
| S19 | No secrets or credentials in commands, examples or scripts | |
| S20 | Complexity fits the job: no router for a 40-line task, no 600-line monolith for five tasks | |

## Judge in context

The same gap weighs differently by skill type.

| Type | Missing X is... |
|---|---|
| Simple, one task, under about 100 lines | Fine: no router, few examples, light validation |
| Complex: several tasks, external services, security | A real defect: needs a verification step, error recovery, and the security rules |
| Delegating: it hands work to a subagent | Fine to define success as "the subagent was invoked with the right inputs" |

Flag over-engineering as well as under-specification. For every finding say why it matters for this skill, not only that a rule was broken.

## Report format

Cite `file:line` for every finding and check the line numbers against the file before reporting. Close with what to keep.

```
Score: 14/20

Assessment
One or two sentences: is the skill fit for purpose, and what is the main point?

Broken
- S2 (SKILL.md:3): description has no trigger. Fix: "... Use when the user asks to <x> or mentions <y>."

Weak
- S5 (references/rules.md:12): the core rule is only in a reference. Fix: move it into SKILL.md.

Polish
- S9 (SKILL.md:41, :58): "route" and "endpoint" are used for the same thing. Fix: choose "endpoint".

Strengths
- A worked example at SKILL.md:70 shows the exact output shape.

Context
Type: complex. Length: 212 lines. Effort to fix: low.
```

- **Broken:** it will not load, will not trigger, or will do the wrong thing.
- **Weak:** it loads but misroutes, wastes context or is unverifiable.
- **Polish:** clarity and consistency.

Every finding gets a concrete fix. Say "no findings" when there are none; do not invent items to look thorough. Do not edit during an audit; apply only the fixes the user asks for.
