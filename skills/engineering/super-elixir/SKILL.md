---
name: super-elixir
description: "Use for any Elixir work: .ex, .exs and .heex files, mix.exs, Phoenix, Ecto, OTP, GenServer, Supervisor, ExUnit and mix tasks. One skill with specialities: write idiomatic code, design OTP, Ecto and Phoenix apps, work test-first, write docs, and review code, security, performance and anti-patterns. It detects the job, loads only the guide it needs, and can run a full multi-pass review in one invocation."
when_to_use: "Use proactively when the user asks to write, change, refactor, test, document or review Elixir; asks 'is this idiomatic', 'should this be a GenServer or a process', 'review this Elixir code', 'security review', 'why is this slow', 'add a changeset' or 'write a doctest'; pastes an Elixir stack trace or a failing mix test; or is working in a mix project."
metadata:
  version: "1.0.0"
---

# Super Elixir

One skill, many specialities. Call it once. It picks the speciality from the job, loads only that guide, and for reviews it can run several passes and return one report.

The guides are kept whole. Each is a full, separate skill that was merged in; the router decides which to open.

## Step 0: detect the job

Do this first and do not announce it. Signals and precedence are in [references/auto-detect.md](references/auto-detect.md). For project facts (Elixir version, Phoenix, Ecto, Oban, which linters exist), run `node scripts/elixir-scan.mjs detect <dir>`.

| If the user is doing this | Speciality | Load |
|---|---|---|
| Writing or changing Elixir, "is this idiomatic", moving from OOP habits | thinking, idioms | [thinking](specialities/thinking/GUIDE.md), [idioms](specialities/idioms/GUIDE.md) |
| `case`, `with`, guards, function heads, destructuring | pattern-matching | [pattern-matching](specialities/pattern-matching/GUIDE.md) |
| GenServer, Supervisor, Agent, Task, Registry, "should this be a process" | thinking first, then otp | [thinking](specialities/thinking/GUIDE.md), [otp](specialities/otp/GUIDE.md) |
| Schemas, changesets, queries, transactions, migrations | ecto | [ecto](specialities/ecto/GUIDE.md) |
| New Phoenix project, umbrella, Bun assets, devenv, end-to-end tests | phoenix | [phoenix](specialities/phoenix/GUIDE.md) |
| LiveView pages, components, streams | the separate `phoenix-liveview` skill | `phoenix-liveview` |
| Designing a new app, supervision trees, Ash, ADRs, a docs package | architect | [architect](specialities/architect/GUIDE.md) |
| Implementing a feature or fixing a bug | tdd | [tdd](specialities/tdd/GUIDE.md); language-agnostic loop: `super-tdd` |
| `@moduledoc`, `@doc`, `@typedoc`, doctests, cross-references | docs | [docs](specialities/docs/GUIDE.md) |
| "Review this code" (style, patterns, OTP basics, docs) | code-review | [code-review](specialities/code-review/GUIDE.md) |
| "Security review", user input, secrets, `String.to_atom`, `Code.eval_string` | security-review | [security-review](specialities/security-review/GUIDE.md) |
| "Slow", throughput, mailbox growth, memory, N+1 | performance-review | [performance-review](specialities/performance-review/GUIDE.md) |
| Known bad patterns, refactoring toward better ones | antipatterns | [antipatterns](specialities/antipatterns/GUIDE.md) |
| "Review everything", "audit this repo", "full review" | the review pipeline below | several |
| "Act as an Elixir expert", broad checklists, BEAM background | foundations, expert | [foundations](specialities/foundations/core-principles.md), [BEAM expert](specialities/foundations/beam-expert.md), [expert](specialities/expert/GUIDE.md) |

Order of precedence: a safety finding, then the user's explicit words, then the detected job. A security finding, a data-loss risk or an irreversible action is always stated in full sentences.

## Review pipeline: several passes, one report

Use this for "review everything", "full review" or any request naming more than one concern. A single named concern runs only its own pass.

1. **Facts.** Run `node scripts/elixir-scan.mjs detect <dir>`. It tells you which passes apply (no Ecto, no GenServers, no Phoenix) and which gates the project really has.
2. **Candidates.** Run `node scripts/elixir-scan.mjs scan <dir>`. The output is a list of places to look, not findings. Never report a candidate without reading the code around it.
3. **Passes, in this order.** Open each guide and its references, apply its checklist, its *Valid Patterns (Do NOT Flag)* and its *Context-Sensitive Rules*.
   1. [code-review](specialities/code-review/GUIDE.md): style, pattern matching, OTP basics, docs.
   2. [security-review](specialities/security-review/GUIDE.md): injection, atoms, secrets, process exposure.
   3. [performance-review](specialities/performance-review/GUIDE.md): GenServer bottlenecks, memory, concurrency, database.
   4. [antipatterns](specialities/antipatterns/GUIDE.md): the known-bad catalog, only for what the earlier passes did not already cover.
4. **Verify every finding** with [references/verification-protocol.md](references/verification-protocol.md). A finding that fails a gate is dropped or downgraded to a question.
5. **Report once.** Fill [templates/review-report.md](templates/review-report.md). De-duplicate across passes, order by severity, give each finding a `path:line`, the evidence, and a fix.

Review only. Do not edit code during a review pass unless the user asked for fixes.

## Build pipeline: one feature, in order

1. **Think.** [thinking](specialities/thinking/GUIDE.md): does this need a process at all? What is the data, what are the functions?
2. **Shape.** New app or large feature: [architect](specialities/architect/GUIDE.md). Otherwise skip.
3. **Test first.** [tdd](specialities/tdd/GUIDE.md): a failing test, then the smallest change.
4. **Write.** [idioms](specialities/idioms/GUIDE.md), [pattern-matching](specialities/pattern-matching/GUIDE.md), plus [otp](specialities/otp/GUIDE.md) or [ecto](specialities/ecto/GUIDE.md) as the code needs.
5. **Document.** [docs](specialities/docs/GUIDE.md) for public modules and functions.
6. **Gate.** `mix format`, `mix compile --warnings-as-errors`, `mix test`, then only the linters in `mix.exs` (Credo, Sobelow, Dialyzer). Use [templates/feature-checklist.md](templates/feature-checklist.md) to track it.

## The short list of iron laws

Every guide keeps its own full list. These recur across the sources and rarely conflict:

1. **No process without a runtime reason.** State, concurrency or fault isolation. Otherwise plain functions.
2. **Supervise every long-lived process.** No bare `start_link` in production.
3. **Tagged tuples for expected failure.** Raise for bugs. `rescue` only around external code.
4. **In `with`, every failable step uses `<-`.** A `=` swallows the error.
5. **Guards use `and`, `or`, `not`.** Never `&&`, `||`, `!`.
6. **No atoms from external input.** `String.to_atom/1` on user data leaks the atom table.
7. **Messages are copied.** Keep them small.
8. **Changesets for external data.** `cast/4` for input, `change/2` for internal changes.
9. **No code without a failing test first.**
10. **Verify before you report.** Evidence, not impression.

Where two guides disagree, the stricter rule wins, and the project's own `AGENTS.md` and rules (see `rules/elixir/`) win over both.

## Overlaps: which copy to read

These topics exist in more than one guide. All are kept. Pick by the job.

| Topic | To write code | To review code |
|---|---|---|
| Pattern matching | [pattern-matching](specialities/pattern-matching/GUIDE.md) (full), [idioms/pattern-matching](specialities/idioms/references/pattern-matching.md) (short) | [code-review/pattern-matching](specialities/code-review/references/pattern-matching.md) |
| OTP | [otp](specialities/otp/GUIDE.md) (full), [idioms/otp-patterns](specialities/idioms/references/otp-patterns.md) (short) | [code-review/otp-basics](specialities/code-review/references/otp-basics.md) |
| Anti-patterns | [antipatterns](specialities/antipatterns/GUIDE.md), [extended catalog](specialities/antipatterns/assets/extended.md) | [idioms/anti-patterns](specialities/idioms/references/anti-patterns.md) |
| Documentation | [docs](specialities/docs/GUIDE.md) | [code-review/documentation](specialities/code-review/references/documentation.md) |
| Errors | [idioms/error-handling](specialities/idioms/references/error-handling.md) | the anti-patterns guides |

## Layout

| Folder | Holds |
|---|---|
| [specialities/](specialities/) | One folder per speciality. `GUIDE.md` is the entry point; `references/` and `assets/` hold the depth |
| [references/](references/) | [auto-detect.md](references/auto-detect.md), [verification-protocol.md](references/verification-protocol.md) |
| [templates/](templates/) | [review-report.md](templates/review-report.md), [feature-checklist.md](templates/feature-checklist.md) |
| [scripts/](scripts/) | `elixir-scan.mjs`: project detection and risk-pattern candidates |

## Old skill names

Text inside the guides may name the skill it came from. Resolve it here.

| Old name | Speciality |
|---|---|
| `elixir`, `elixir-pro` | foundations |
| `elixir-thinking` | thinking |
| `elixir-idioms` | idioms |
| `elixir-pattern-matching` | pattern-matching |
| `elixir-antipatterns` | antipatterns |
| `elixir-otp-patterns` | otp |
| `elixir-ecto-patterns` | ecto |
| `elixir-phoenix` | phoenix |
| `elixir-architect` | architect |
| `elixir-tdd` | tdd |
| `elixir-writing-docs` | docs |
| `elixir-code-review` | code-review |
| `elixir-security-review` | security-review |
| `elixir-performance-review` | performance-review |
| `elixir-expert` | expert |

## Related skills

- `super-tdd`: drive a change test-first.
- `super-refactor`: clean up Elixir without changing behavior.
- `super-protobuf`: the service exposes protobuf, gRPC or Connect.
- `super-verify`: prove tests and gates pass before you claim done.
- `handoff`: pause a long review or change.

## Done when

- The right speciality (or the pipeline) ran, and only the needed guides were opened.
- Code compiles and tests pass, or the review report is complete with evidence for every finding.
- No finding was reported that failed the verification protocol.
