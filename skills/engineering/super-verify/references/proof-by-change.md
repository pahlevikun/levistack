# Proof by kind of change

Type checks and unit tests are a baseline, not sufficient proof on their own. Match the check to the change. Reading code is not a verification strategy: if no row fits, use the last row and say so.

## Contents
- Check by change type
- Adversarial probe
- Blast radius
- Traps that look like proof

## Check by change type

| Change | Required check |
|---|---|
| Frontend (component, page, form) | Start it, use the feature in a browser, read the console. Exercise the happy path and one failure path |
| Backend endpoint or handler | Call it for real (`curl`). Check status and response shape, and one error path (bad input, missing auth) |
| Queue, job or async workflow | Trigger the real entry point, wait up to its documented deadline, inspect the durable business effect. "Enqueued" proves nothing. Exercise one terminal failure or dead-letter path and check what it records |
| CLI | Run the binary with real input; check stdout, stderr and exit code. Run it from a different directory to catch "only works from the source tree" |
| Infrastructure as code | `terraform plan`, `docker build`, `kubectl apply --dry-run=server`. Review the plan before applying |
| Database migration | Up, down, up again, on production-shaped data. Check row counts and constraints |
| Refactor, no behavior change | The existing tests pass unchanged, and the public surface diff shows nothing removed |
| Mechanical or scripted sweep (rewrap, regex rewrite) | A parser or compiler (`tsc --noEmit`, `cargo check`, a build). Never the linter's error count |
| Dependency or library update | The consumer's test suite on the new version, and deprecation warnings read |
| Published package or release artifact | Install the published version in a scratch directory and call the API the release added. The working tree shares source and uncommitted edits, so it proves nothing about what a consumer gets |
| Schema or contract change | Old consumers parse the new shape, and new consumers handle old data still in flight |
| Documentation | Read the rendered output; click the links; confirm it says what was intended |
| Config with no validator | Parse it (`jq .`, `yamllint`); otherwise read it against the intended change |
| Non-runnable | `git diff`, confirm it matches intent, and state: "No automated verification available; verified by reading the diff." |

## Adversarial probe

For any change to production logic, include at least one probe that tries to break it, chosen from:

- **Boundary:** 0, -1, empty string, empty list, null, maximum value, a combining character.
- **Concurrency:** two parallel requests with the same id (races, double spend).
- **Idempotency:** the same mutation twice. The second must no-op or fail cleanly.
- **Orphan:** update or delete an id that does not exist.
- **Shape variation:** vary what callers supply to an extension point or I/O path: with and without each optional method, a path that exists and one that does not, a symlink, a read-only parent.
- **Error return:** for a producer that measures something (an offset, a cursor), feed one input per early-return error path, not only well-formed input.

Exempt: docs, typo fixes, pure renames. Everything else needs one. A report with no probe is a happy-path confirmation, not verification.

A test set built to expose a defect cannot test the fix: every row is a case the fix targets. Add a second set the base already handles correctly and show none of them regresses. State both counts.

## Blast radius

Before marking a change done, trace what else it touches:

| Question | How |
|---|---|
| What fires when this runs? Callbacks, middleware, observers, handlers | Read the real code two levels out |
| Do tests exercise the real chain? | If every dependency is mocked, add one test with real objects through the full chain |
| Can failure leave orphaned state? | If state is written before an external call, test the failure and the retry |
| What other entry points expose this? | Search for the behavior in sibling classes, CLIs, jobs |
| Do error strategies across layers conflict? | List the errors each layer raises and handles; check retries do not double-execute |

Skip for leaf changes with no callbacks and no persisted state.

## Traps that look like proof

- A falling lint count with a corrupted file: most linters report only the first parse error per file. Use a parser or build.
- A scripted rewrite that replaces a symlink with a regular file: check `git status --short` for a type change.
- "Successfully rebased" with a hunk silently gone: after any rebase or cherry-pick, diff the touched-file list across the operation and confirm the content is still there. A clean run is not the evidence.
- Reviewing `git diff HEAD` when HEAD already holds an earlier attempt at the same fix: diff against the upstream branch and re-read the whole changed region.
- A release or build step that rewrites a file the commit or upload step never ships: for each file a step produces, name the step that ships it.
