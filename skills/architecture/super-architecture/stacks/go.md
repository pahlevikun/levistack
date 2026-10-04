# Stack: Go

Go favors simple structure. Ask which architecture the team prefers (flat, clean, hexagonal, DDD) and do not impose a heavy one on a small service.

## Layout

```
cmd/orders-api/main.go        composition root: builds adapters, injects them, starts the server
internal/orders/
  domain/                     entities, value objects, domain errors
  application/                use-case structs and their tests
  ports.go                    small interfaces owned by the consuming package
  adapters/
    http/                     handlers (inbound)
    postgres/                 repository implementation (outbound)
```

Everything under `internal/` cannot be imported from outside the module, which gives compile-time encapsulation.

## Rules
- **Interfaces belong to the consumer.** Define a small interface in the package that uses it; implementations satisfy it implicitly. Avoid one large interface per implementation.
- **Constructors are explicit:** `NewPlaceOrder(repo OrderRepository, pay PaymentGateway) *PlaceOrder`. Wire in `main`.
- **Functional options** for constructors that grow optional settings: they add options without breaking callers. Use a builder only when you need staged construction.
- **No `init()` and no mutable package-level state:** they hide dependencies and make tests brittle.
- **Context first:** pass `context.Context` as the first argument to anything that does I/O; check `ctx.Err()` between retries and honor cancellation.
- **Timeout every external call;** retry with backoff only on retryable errors.
- **Resource lifecycle:** `defer Close()` right after opening; shut down gracefully (stop accepting, drain, then close dependencies).
- **Errors:** handle the error case first with an early return; return errors for anything a caller can handle, panic only for programmer errors.
- Enums start at 1 so the zero value means unset.

## Enforce the boundaries
Keep domain packages free of `net/http`, `database/sql` and vendor SDK imports; check with a small test that parses imports of `internal/*/domain` (or a Go architecture linter). `go vet` and `go build ./...` catch cycles.

## Tests
Table-driven unit tests for domain and use cases with fake implementations of the small interfaces; integration tests for adapters with a containerized database; HTTP handler tests with `httptest`.

## Pitfalls
Interfaces defined next to their implementation instead of their user, global database handles, `init()` registering dependencies, ignoring context, mixing transport structs into the domain, over-layering a service that fits in one package.
