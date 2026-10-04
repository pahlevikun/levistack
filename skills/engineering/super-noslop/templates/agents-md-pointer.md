# AGENTS.md pointer (first-run install)

**Skip** if root `AGENTS.md` already contains `<!-- super-noslop:start -->` or legacy `<!-- noslop:start -->`.

1. Get user approval before editing root `AGENTS.md`.
2. This package ships **`super-noslop-code`** for comment-only passes.
3. Append at the **end** of root `AGENTS.md` (replace an older block if present):

```md
<!-- super-noslop:start -->
## super-noslop
For backend/API/frontend/database work and code comments, read `skills/engineering/super-noslop/SKILL.md` and `skills/engineering/super-noslop/skills/super-noslop-code/SKILL.md` for comment-only cleanup.
Before starting, ask when super-noslop applies: during the work, or after it is done.
<!-- super-noslop:end -->
```

4. Ask the usage-mode question ([SKILL.md](../SKILL.md)), then proceed.
