# Auto-detect: pick the speciality for the current job

Run this before answering. One scan of the user's words, the open files, the last tool output and `mix.exs`. Do not ask which speciality to use. Pick, load the guide, and say nothing about it unless the pick changes the result.

Precedence: **safety finding**, then **explicit user words**, then **detected job**.

## 1. Safety override

Switch to plain, full sentences, then return to normal, when the answer involves a security finding, a secret, data loss, an irreversible action (a destructive migration, a production `mix ecto.reset`), or a step order that matters.

## 2. Explicit words

| The user says | Load |
|---|---|
| "review", "code review", "check this module" | code-review |
| "security", "vulnerability", "injection", "secrets", "audit auth" | security-review |
| "slow", "performance", "bottleneck", "mailbox", "memory", "throughput", "N+1" | performance-review |
| "full review", "review everything", "audit the repo" | the review pipeline |
| "anti-pattern", "code smell", "refactor this" | antipatterns |
| "test first", "TDD", "write a test for", "fix this bug" | tdd |
| "docs", "moduledoc", "doctest", "typespec docs" | docs |
| "new app", "architecture", "supervision tree", "ADR", "Ash" | architect |
| "new Phoenix project", "umbrella", "Bun", "devenv" | phoenix |
| "GenServer", "Supervisor", "Task", "Agent", "Registry", "should this be a process" | thinking, then otp |
| "schema", "changeset", "query", "migration", "transaction", "Repo" | ecto |
| "case", "with", "guard", "pattern match" | pattern-matching |
| "idiomatic", "the Elixir way", "coming from Ruby / JS / Java" | thinking, idioms |
| LiveView, `.heex`, `Phoenix.Component`, streams | the separate `phoenix-liveview` skill |

## 3. Files in play

| Open or changed file | Likely speciality |
|---|---|
| `lib/**/*.ex` (contexts, modules) | idioms, pattern-matching |
| `*_server.ex`, `application.ex`, `*supervisor*.ex` | otp |
| `schemas/*.ex`, `priv/repo/migrations/*.exs`, `*_repo.ex` | ecto |
| `*_live.ex`, `*.heex`, `components/*.ex` | `phoenix-liveview` |
| `test/**/*_test.exs`, `test/support/*` | tdd |
| `mix.exs`, `config/*.exs`, `rel/*` | phoenix, architect, security-review (secrets) |
| `.credo.exs`, `.formatter.exs` | idioms (style gates) |

## 4. Last tool output

| You see | Likely speciality |
|---|---|
| `(FunctionClauseError)`, `(MatchError)`, `(CaseClauseError)`, `(WithClauseError)` | pattern-matching |
| `GenServer ... terminating`, `** (EXIT)`, `:noproc`, `:timeout` in `call` | otp, thinking |
| `Ecto.NoResultsError`, `Ecto.Changeset` errors, `(Postgrex.Error)` | ecto |
| a failing `mix test` | tdd |
| compiler warnings (unused variable, unused alias, undefined function) | idioms |
| Dialyzer or `@spec` complaints | docs, idioms |
| `Sobelow` findings | security-review |
| a profiler or `:observer` dump, growing process memory | performance-review |

## 5. The project

`node scripts/elixir-scan.mjs detect <dir>` reports what is really there. Use it to skip passes that cannot apply: no Ecto, no ecto guide; no GenServer, no otp pass; no Phoenix, no phoenix guide. It also lists which gates exist, so you never suggest a linter the project does not use.

## 6. How much to load

- One job usually needs one or two guides. Open a guide's `references/` files only when its table points at your case.
- The review pipeline opens the four review guides in turn, not all fifteen.
- Prefer the short copy (a reference inside `idioms/`) for quick questions, and the full guide for implementation or review work.
- Never open `specialities/expert/scaffold/`. It holds inert placeholders from the original package.

## 7. Why this skill sets no `paths:`

Claude Code and Cursor both treat `paths:` as a **restriction**: the skill is then surfaced only while matching files are being read or edited. This skill must also fire on a plain question such as "should this be a GenServer?" with no file open, so it relies on the description and `when_to_use` instead. Both are kept short and lead with the use case, because Claude truncates the two together at 1,536 characters. Do not add `paths:` to "improve" auto-invocation.
