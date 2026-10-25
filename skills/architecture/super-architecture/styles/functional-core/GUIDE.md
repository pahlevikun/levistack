# Functional core, imperative shell

Business decisions are pure functions of data. All I/O, retries, clocks and framework hooks live in a thin shell that interprets commands the core returns. Tests of rules need no doubles for databases or HTTP.

## Pick when
- Rules are tangled with database calls, HTTP or filesystem I/O; unit tests are slow or brittle.
- You want deterministic tests on plain data, plus a thin integration layer for the shell.
- Adapters and frameworks churn and you are tired of rewriting the same decisions.

## Avoid when
- A hot path where allocation from immutability is a measured problem.
- A purely imperative codebase with no appetite for this split; start with hexagonal ports instead.
- There is almost no business logic: a layered CRUD service is enough.

## Core idea

The **core** takes domain data in and returns a **decision**: new state, and a small set of command objects (`PersistOrder`, `PublishEvent`, `NotifyUser`). It never imports a framework, socket, ORM or clock. The **shell** loads data, calls the core, then executes those commands in order (persist, publish, respond), with retries and telemetry.

This is the dependency rule with functions instead of port interfaces. Hexagonal still fits when you want explicit ports and several adapters; functional-core fits when the seam is "pure decision versus effect."

## Layout

```
core/                     pure functions, types, decisions, command objects
shell/
  adapters/               persistence, HTTP, queues, filesystem
  handlers/               load input, call core, interpret commands
composition/              wiring, config
```

## Dependency rules

| Piece | May import | Must not |
|---|---|---|
| Core | Language standard library, core types | Shell, adapters, frameworks, I/O |
| Shell | Core, adapters | Business `if` that belongs in the core |
| Adapter | Shell contracts, technology | Core internals |

## Build steps
1. **Inventory side effects.** Map every database write, HTTP call, UI event and file access to the shell. Do this before extracting.
2. **Model the core** as pure functions: data in, decision and commands out. No shared mutable state.
3. **Define a small command schema** the shell understands. Grow it only when a new effect appears.
4. **Extract high-churn modules first.** Wrap legacy I/O behind adapters; move calculations into the core.
5. **Enforce with architecture tests:** zero I/O or framework imports in `core/`.
6. **Prove a thin adapter** against the real framework lifecycle before a large rewrite.

## Testing
- Core: unit and, where it pays, property-based tests. No I/O mocks. Coverage of decisions should be high because it is cheap.
- Shell: contract tests that the commands are interpreted, retried and logged correctly.
- Architecture test: `core/` imports nothing from shell or adapters (`scripts/arch-scan.mjs check`).

## Pitfalls
Decisions leaking into the shell ("just this once" in a handler). Command objects that smuggle ORM types. A core that calls the clock or UUID generator instead of taking them as data. Rewriting the whole app before a side-effect map exists. Treating this as opposed to hexagonal: a shell adapter can implement a hexagonal port.

## Combines with
Hexagonal (ports are the shell's edges), domain-driven (pure functions named in the ubiquitous language), CQRS (core handles commands; shell runs queries), pipeline (each filter can be a pure core).
