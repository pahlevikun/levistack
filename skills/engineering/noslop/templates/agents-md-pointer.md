# AGENTS.md pointer (first-run install)

**Skip** if root `AGENTS.md` already contains `<!-- noslop:start -->` or legacy `<!-- noslop:start -->`.

1. Get user approval before editing root `AGENTS.md`.
2. This package ships **`noslop-code`** for comment-only passes.
3. Append at the **end** of root `AGENTS.md` (replace an older block if present):

```md
<!-- noslop:start -->
## noslop
For backend/API/frontend/database work and code comments, read `skills/engineering/noslop/SKILL.md` and `skills/engineering/noslop/skills/noslop-code/SKILL.md` for comment-only cleanup.
Before starting, ask when noslop applies: during the work, or after it is done.
<!-- noslop:end -->
```

4. Ask the usage-mode question ([SKILL.md](../SKILL.md)), then proceed.
