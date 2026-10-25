# Skill audit checklist

Run the linter first (see `SKILL.md`). It covers the mechanical checks marked (L). The rest need judgment. Score each item pass or fail, report `passed/total`, and list failures by priority.

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

## Report format

```
Score: 14/18

Broken
- S2: description has no trigger. Fix: "... Use when the user asks to <x> or mentions <y>."

Weak
- S5: the core rule is only in references/rules.md. Fix: move it into SKILL.md.

Polish
- S9: "route" and "endpoint" are used for the same thing. Fix: choose "endpoint".
```

- **Broken:** it will not load, will not trigger, or will do the wrong thing.
- **Weak:** it loads but misroutes, wastes context or is unverifiable.
- **Polish:** clarity and consistency.

Every finding gets a concrete fix. Say "no findings" when there are none; do not invent items to look thorough.
