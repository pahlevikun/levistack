# Feature checklist: <feature>

Copy, fill, and tick as you go. Skip a step only with a reason.

## 1. Think
- [ ] Does it need a process? At least one of: state across calls, concurrency, fault isolation. If not, plain functions.
- [ ] Data shape decided (struct, map, schema); behavior is module functions.
- [ ] Expected failures listed and returned as tagged tuples.

## 2. Shape (new app or large feature only)
- [ ] Boundaries and supervision tree sketched.
- [ ] Decision recorded (ADR) if it is hard to reverse.

## 3. Test first
- [ ] Failing test written and run; it fails for the intended reason.
- [ ] Cases: happy path, validation failure, edge values, not-found, authorization where relevant.
- [ ] Assertions match shape and content, not truthiness.

## 4. Write
- [ ] Smallest change that passes.
- [ ] Function heads and guards before `if`/`case`; `with` steps use `<-`.
- [ ] No atoms from external input; changesets for external data.
- [ ] Long-lived processes are supervised.

## 5. Document
- [ ] `@moduledoc` and `@doc` on public modules and functions; `@spec` on exported functions.
- [ ] Doctests for pure functions.

## 6. Gate
Run only the gates the project has (`elixir-scan.mjs detect` lists them).
- [ ] `mix format --check-formatted`
- [ ] `mix compile --warnings-as-errors`
- [ ] `mix test`
- [ ] `mix credo --strict`, `mix sobelow`, `mix dialyzer` if configured
- [ ] Review pass if the change touches input handling, processes or queries

## Result
- Commands run and their real output:
- Open follow-ups:
