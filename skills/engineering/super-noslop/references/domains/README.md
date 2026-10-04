# Domain index

Load **one** domain checklist plus the [core pack](../core/slop-patterns.md) (patterns, R-01–R-38, delivery gate). Domains overlap; pick the primary surface of the change.

| Domain | File | When |
|---|---|---|
| Backend | [backend.md](backend.md) | Services, handlers, workers, repos, clients, jobs |
| API | [api.md](api.md) | Routes, envelopes, status codes, OpenAPI, webhooks |
| Database | [database.md](database.md) | SQL, ORM, migrations, indexes, transactions |
| Frontend | [frontend.md](frontend.md) | Components, styles, client state, a11y, UI perf |
| Infra / config | [infra-config.md](infra-config.md) | Env, flags, IaC fragments, wiring in diff |
| Tests | [tests.md](tests.md) | Specs, fixtures, mocks, assertion style |
| Docs-only | [docs-exclusions.md](docs-exclusions.md) | No executable surface — use writing skills |

Surface routing (legacy table): [surfaces.md](../core/surfaces.md).
