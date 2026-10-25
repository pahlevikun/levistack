# Change-type checks

Extra checks for the kinds of change in the diff. Pick the rows that match, and paste their checks into `{CHANGE_TYPE_CHECKS}` in the reviewer prompt. A diff can match several rows.

When the levistack rules are installed, the rule in the last column holds the full standard. Point reviewers at it instead of repeating it.

| Change type | How to spot it | Check | Rule or skill |
|---|---|---|---|
| **Database migration** | new files under `migrations/`, `priv/repo/migrations/`, schema changes | Can it run on a live table without a long lock? Does it work with the old code still running (deploy order)? Is there a way back? Does a backfill run in batches? | `rules/architecture/migrations-and-soft-delete.md` |
| **Query or index** | new queries, ORM calls in loops, new `WHERE` or `ORDER BY` | N+1 queries? Does an index back the new filter or sort? Is the result set bounded (limit, pagination)? | `rules/architecture/queries-and-indexes.md` |
| **API or event contract** | changed request or response shapes, routes, OpenAPI, `.proto`, event payloads | Can an existing caller see any difference? New fields additive and optional? Error codes and bodies unchanged for old callers? Versioning if not? | `rules/architecture/external-contracts.md`, `super-protobuf` |
| **Endpoint or auth** | new routes, middleware, permission checks | Authentication and authorization on every new path? Input checked once at the edge? No secrets or personal data in logs or errors? | `rules/architecture/api-security.md`, `rules/core/pii-logging.md` |
| **Background job or consumer** | workers, queues, cron, retries | Safe to run twice (idempotent)? What happens on a crash halfway? Retry with backoff and a limit? Poison messages handled? | `rules/architecture/async-jobs-and-consumers.md` |
| **Outbound call** | new HTTP clients, SDK calls to other services | Timeout set? Retries bounded and only on safe errors? What does the caller see when the other side is down? | `rules/architecture/outbound-integrations.md` |
| **Config or feature flag** | new env vars, flags, settings | Safe default when the value is missing? Flag removal planned? Both flag states tested? | `rules/architecture/configuration-and-feature-flags.md` |
| **Cache** | new cache reads or writes, TTLs | What invalidates it? Can stale data cause a wrong decision? Stampede on expiry? | `rules/architecture/data-stores-and-caches.md`, `super-caching` |
| **Money or billing** | amounts, currency, invoices, payouts | Integer minor units or decimals, never floats? Rounding rule stated? Audit trail? | `rules/architecture/financial-data.md`, `rules/architecture/audit-events.md` |
| **Error handling** | new `try`/`catch`, `rescue`, error mapping | Errors surfaced, not swallowed? One place maps errors to responses? | `rules/architecture/error-boundaries.md`, `rules/core/failure-visibility.md` |
| **Layering** | imports across modules, handlers that grew logic | Does the dependency point the right way? Business logic out of the handler? | `rules/architecture/layering-and-dependency-direction.md`, `rules/architecture/thin-handlers-and-middleware.md` |
| **Shutdown or health** | new long-running processes, servers, health checks | Graceful shutdown drains work? Health check tells "alive" from "ready"? | `rules/architecture/health-and-shutdown.md` |
| **Dependency bump** | lockfile and manifest changes | Major version? Breaking changes read from the changelog? New transitive packages? License change? | none. Read the package's changelog |
| **Refactor only** | the PR says "no behavior change" | Is behavior really the same? Do the existing tests still pass unedited? Any public name changed? | `safe-refactor` |
| **Tests only** | only test files changed | Do the tests fail when the code is broken (not testing mocks)? Behavior, not implementation details? | `rules/core/testing.md`, `tdd` |
| **Elixir code** | `.ex`, `.exs`, `.heex` | OTP supervision, process ownership, Ecto changesets | `super-elixir`, `rules/elixir/*` |
| **Generated code or comments** | AI-written handlers, comment-heavy diffs | Generic errors, filler comments, tutorial layering | `noslop`, `rules/core/noslop.md` |

## How deep to go

`rules/architecture/review-depth.md` scales depth with blast radius. Shared runtime surfaces (middleware wiring, runtime config, migrations, the shared HTTP client, health code, and agent rules, hooks or skills) get the highest depth: check call sites, config wiring, failure modes and the verification commands, not only the diff. A handler for one feature slice gets medium depth. Isolated docs, tests and leaf helpers get normal depth.

Combine it with the risk node from the brief. A highest-depth surface on a production hot path gets every matching row. An internal script at normal depth gets the correctness rows only.
