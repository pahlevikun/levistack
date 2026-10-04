# Surfaces (routing)

Prefer the domain router in [SKILL.md](../../SKILL.md) Step 0. This table maps legacy "surface" language to files.

| Surface | Load | Scope |
|---------|------|--------|
| **Backend / API / services** | [domains/backend.md](../domains/backend.md) or [api.md](../domains/api.md) + core pack | Handlers, services, repos, clients, workers, routes, OpenAPI |
| **Database** | [domains/database.md](../domains/database.md) + core pack | SQL, ORM, migrations |
| **Frontend** | [domains/frontend.md](../domains/frontend.md) + core pack | Components, CSS, layout, client state |
| **Code comments** | Core **and** [`super-noslop-code`](../../skills/super-noslop-code/SKILL.md) | Comments only — never executable code |
| **Infra / config** | [domains/infra-config.md](../domains/infra-config.md) + core pack | Env, flags, wiring in diff |
| **Tests** | [domains/tests.md](../domains/tests.md) + core pack | Specs and fixtures |
| **Docs-only** | [domains/docs-exclusions.md](../domains/docs-exclusions.md) | No executable surface |

Never fetch subskills from the network. Never invent folders that are not on disk.

Before inventing layers, read `AGENTS.md`, the project docs and sibling modules in the same package. Repo facts outrank generic patterns.
