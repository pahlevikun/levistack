# Refactor plan protocol

Use in **plan** mode. **Do not edit product code** while planning unless the user only asked for a plan and explicitly allows probe reads.

## Steps

1. Search and read: implementation, tests, config, and docs that touch the target.
2. Map affected files, dependencies, hidden coupling, and public contracts.
3. Sequence work: types/contracts → implementations → callers → tests → cleanup.
4. Insert verification between phases (commands the repo already runs).
5. Add rollback notes for risky phases (state moves, renames at scale).
6. Output the plan format below.
7. **Stop and ask for confirmation** before implementing. If the user said "plan then implement", still show the plan first unless they waived review after the plan.

If the request is too ambiguous to plan safely, ask concise clarifying questions instead of guessing.

## Output format

```markdown
## Refactor Plan: [title]

### Current state
[How it works today]

### Target state
[How it will work after — behavior preserved unless scoped]

### Affected files
| File | Change | Depends on |
|------|--------|------------|
| path | modify/create/delete | … |

### Execution plan

#### Phase 1: [name]
- [ ] Step …
- Verify: …

#### Phase 2: …

### Rollback
1. …

### Validation
Final: [exact commands]
```

After approval, switch to `core/safe-refactor-protocol.md` for execution (see [SKILL.md](../../SKILL.md)).
