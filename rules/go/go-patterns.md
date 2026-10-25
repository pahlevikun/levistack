---
description: "Idiomatic Go: layering, errors, context, interfaces, tests and format gates."
globs: "**/*.go"
alwaysApply: false
---

# Go patterns

## Layering
- Dependencies point one way: `cmd` → app wiring → domain/feature packages → clients. Lower layers never import higher ones.
- Wiring files hold wiring only, with no business logic. Handlers parse, call, and map errors; they stay thin.
- One package per upstream client. The interface lives with the consumer or in the client's package. Transport errors only.
- No cross-feature imports of internals. Share through a `common` package or a client.

## Idiomatic Go
- **Accept interfaces, return structs.** Keep parameters narrow (`io.Reader`, a small `Client` interface).
- **Make the zero value useful** (`sync.Mutex`, `bytes.Buffer`). Use a constructor where it would panic.
- **Functional options** for more than two optional knobs, not for one-off structs.
- **No `panic`** on request or worker paths, and no `log.Fatal` outside `main`.
- **No ignored errors.** `_ = err` only with a one-line comment saying why it is safe.

## Errors
```go
if err != nil {
    return fmt.Errorf("%s: %s: %w", pkg, step, err)
}
```
- Return typed errors at feature boundaries, not bare `errors.New` deep in task bodies.
- Use `errors.Is` / `errors.As`. Never parse `err.Error()` or `strings.Contains` on an error.
- Clients return a typed HTTP error for non-2xx; map it once, at the boundary that owns the outcome.

## Context
- `context.Context` is the first parameter of domain and client methods.
- Never `context.Background()` inside business logic on a request or worker path.
- Every outbound call has a timeout (`context.WithTimeout`); `defer cancel()` immediately.

## Interfaces and codegen
- Small interfaces at the point of use. Regenerate mocks after an interface changes. Never hand-edit generated files.

## Tests and format
- Table-driven tests with `t.Run`. See `testing`.
- Gate before done: `gofmt`, `go vet`, the project linter, `go mod tidy`.
- Scoped runs: `go test -race -count=1 ./path/to/pkg/...`

## Anti-patterns
- Naked returns in long functions.
- Business logic in wiring files or fat handlers.
- Hidden global state; `init()` doing real work.
