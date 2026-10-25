# Testing architecture

An architecture is correct when the boundaries let you test each part at the right cost, and when the boundaries themselves are checked automatically.

## Contents
- Test per layer
- Seams and fakes
- Contract tests
- Architecture tests
- The boundary validation trick
- Slice and feature tests

## Test per layer

| Layer | Test type | Doubles | Speed |
|---|---|---|---|
| Domain | Unit tests on pure rules | None | Milliseconds |
| Application | Unit tests of use cases | Fake or stub ports (in-memory repositories, a fixed clock) | Milliseconds |
| Inbound adapter | Protocol mapping tests: request to command, result or error back to protocol | The use case, stubbed | Fast |
| Outbound adapter | Integration tests against real infrastructure (real database, real HTTP stub server) | None | Slower, run fewer |
| Whole system | A few end-to-end journeys through an inbound adapter | None | Slowest |

Test the domain exhaustively because it is cheap. Test adapters against real infrastructure sparingly because they exist to talk to it.

## Seams and fakes

Ports are the seams. Provide an in-memory implementation of every outbound port, used by use-case tests and local development. A use case that cannot run in a plain unit test with no database, no network and no framework has leaked infrastructure into the core.

## Contract tests

Write one shared test suite per outbound port and run it against every adapter, including the in-memory one. It proves each adapter honors the port's contract, and that the fake behaves like the real thing. Add it before the adapter is merged.

## Architecture tests

Encode the dependency rule as a test that fails the build:

- the domain imports no framework and no outer layer;
- the application layer imports no adapter or infrastructure;
- adapters do not import each other;
- feature or slice folders do not import each other's internals;
- modules in a modular monolith import only façades;
- a functional core imports no I/O or framework libraries;
- the module dependency graph has no cycles.

Use the stack's tool (see `stacks/`) or a small script that parses imports. `scripts/arch-scan.mjs check` gives candidates when no such test exists yet; turn the confirmed rules into a permanent test.

## The boundary validation trick

If you can run the whole application's business scenarios from a test, with no database and no HTTP server, the boundaries are in the right place. Run the domain's unit tests with the persistence and web layers deleted from the build: they should still compile and pass.

## Slice and feature tests

In feature-first structures, test each feature mainly through its entry point and assert outcomes (stored state, calls to external systems, the response), not internal calls. Add platform or adapter tests for shared technical code. Keep a characterization test around legacy behavior until the new boundary is proven equivalent.
