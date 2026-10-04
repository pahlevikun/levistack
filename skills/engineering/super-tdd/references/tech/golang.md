# Go TDD track

Apply the core loop from [SKILL.md](../../SKILL.md). This file is the Go gate, not a second testing textbook.

**Use when:** `.go` files, `go test`, table-driven tests, or "Go TDD".

## Runner

- Focused: `go test ./path/to/pkg -run TestName -count=1`
- Package: `go test ./path/to/pkg -count=1`
- Broader: `go test ./...` when the change crosses packages
- Prefer `-count=1` while iterating so cache cannot hide a false green

## Seams

Test exported API: handlers via `net/http/httptest`, packages via exported funcs, interfaces you already inject. Do not test unexported helpers as the primary spec.

Table-driven tests at the package seam are the default shape when the project already uses them.

## Green

Smallest change that compiles and passes this case. Do not add options or interfaces until a failing test needs them.

## Refactor

After green, peer `super-refactor` Go track (`tech/golang/refactoring.md` there). Keep `go test` green per step.
