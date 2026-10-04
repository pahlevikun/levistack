# Part 1: Backend slop patterns (warning signs)

Diagnostic scan — not a ban list. [mandatory-rules.md](mandatory-rules.md) Hard Gate rules are absolute. Other patterns need a written reason (R-31).

## Architecture and layering

| Pattern | Telltale signs |
|---------|----------------|
| Tutorial layering | Controller→service→repo for one query |
| God service | One file owns HTTP, SQL, email, and scheduling |
| Utils dump | `helpers.go` / `utils.py` catching unrelated one-offs |
| Event bus for one listener | Pub/sub to avoid a direct call |
| Interface cleanliness | `IUserService` + single impl, no second consumer |
| Clone architecture | Clean Architecture / hex sample dropped into unrelated repo |
| Premature microservice | New service boundary for one endpoint |

## Names and types

| Pattern | Telltale signs |
|---------|----------------|
| Generic names | `Manager`, `Helper`, `Util`, `Processor`, `DataService` |
| Generic DTOs | `Data`, `Info`, `RequestDTO`, `ResponseModel` everywhere |
| Stringly typed | Status, role, error kind as raw strings across layers |
| Buzzword logs | "Robust seamless enterprise handler initialized" |

## API and messages

| Pattern | Telltale signs |
|---------|----------------|
| Generic errors | `An error occurred`, `Something went wrong`, `Invalid request` |
| String matching | `if err.Error() == "not found"` |
| Template OpenAPI | "Returns data", "Handles the request" |
| Generic success | `{ "message": "Success" }` with no contract |
| Em dash copy | User-facing API text with `—` |
| Fake statistics | "99.9% uptime" in docs with no source |

## Behavior and stubs

| Pattern | Telltale signs |
|---------|----------------|
| Fake success | `200` + empty body; prod path with `TODO` |
| Happy path only | No empty, validation, timeout, or upstream error path |
| Fail open | Auth/validation ambiguity → proceed anyway |
| Mock in prod DI | In-memory repo or stub client wired by default |
| Dead routes | Registered handler that 404s or noops |
| Silent swallow | `catch {}` / log and return OK |

## Data, config, and integrations

| Pattern | Telltale signs |
|---------|----------------|
| Invented config | Plausible hostnames, queue names, API keys as if real |
| N+1 / unbounded read | Loop queries; no pagination or limit |
| Non-idempotent retry | Retry on create/charge without dedupe key |
| Patch-script fix | sed/regex on deployed SQL or config instead of source |
| Fabricated fixtures | Realistic customer rows presented as production samples |

## Observability and jobs

| Pattern | Telltale signs |
|---------|----------------|
| Log every line | Info log on entry/exit of every private method |
| Duplicate errors | Same failure logged at handler, service, and client |
| Mystery cron | Scheduled job with no trigger story or idempotency |
| Decorator soup | `@Transactional` / `@Retry` / `@Cacheable` on every method |
