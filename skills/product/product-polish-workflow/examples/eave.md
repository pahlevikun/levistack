# Worked example: Eave

Use this reference only for Eave. Its platform, paths and contracts are not requirements for other products.

Paths below are relative to `eave/`. Confirm current source; these are contracts to inspect, not a substitute for discovery. Read `ARCHITECTURE.md`, `DESIGN.md`, `docs/verification.md` and the relevant development plan first.

## Result shape illustrated here

The Eave engagement left an architecture record (`ARCHITECTURE.md`), a native design system (`DESIGN.md`), a verification record (`docs/verification.md`) and a phased next-development plan (`docs/plans/2026-10-24-polish-and-next-development.md`). The polish also addressed real first-use, recovery, lifecycle and native-presentation paths. These artifacts illustrate the [minimum result](../references/minimum-result.md) for a full engagement. Their historical checks do not prove the current checkout or visible animation on a real desktop.

## Ownership and source map

| Boundary | Owns | Start here |
|---|---|---|
| EaveCore | Domain values, discovery, script execution, scheduling, pure plans/geometry | `Sources/EaveCore/Script/PluginScheduler.swift`, `ScriptRunner.swift` in the same directory |
| EaveKit | AppKit/SwiftUI adapters, menu bar, overflow, permissions and Touch Bar | `Sources/EaveKit/` |
| Application | Startup, watcher, reconciliation, Settings | `Eave/AppState.swift`, `Eave/PluginFolderWatcher.swift`, `Eave/Settings/` |

Core is AppKit-free, not entirely pure: discovery reads files and the runner starts processes. Keep scheduling and registration policy out of native presenters. Do not add a database, cloud service or framework migration as incidental polish.

## Lifecycle invariants

- Treat registration validity, in-flight execution and UI delivery as distinct lifetimes. `PluginDeliveryToken` retires a removed/replaced registration. A run ticket identifies the execution; stale completion must not clear a newer run.
- Retiring a registration does not stop its process. Keep in-flight exclusion until the process actually completes. Record completion time after execution.
- Recheck the current token and its identity in AppState after the main-actor hop, immediately before applying results. Checking only inside the scheduler leaves a delivery race.
- Removal reconciles native presentations, diagnostics, failure state, Touch Bar and overflow. Failed discovery retains useful prior state and exposes an error; it does not mean an empty folder.
- Interval parsing uses checked arithmetic. An overflowing interval is invalid; discovery falls back to its default interval rather than crashing or discarding the whole plugin.
- An unchanged Plugin registration at the same path is retained. The next execution reads changed file contents; do not claim content-fingerprint invalidation.

Reopen `Tests/EaveCoreTests/LifecycleRegressionTests.swift`, `SchedulerTests.swift`, `DiscoveryTests.swift` and `Tests/EaveApplicationTests/AppStateTests.swift` when changing these paths. Use temporary fixture scripts, never installed user plugins.

## Native design and interaction

`DESIGN.md` and existing Settings metrics own dimensions. The documented calm refinement uses Fieldstone for app-owned pane/detail surfaces; text, focus, selection and controls retain native semantics. Resolve custom colors from the supplied appearance, read Increase Contrast through NSWorkspace and refresh existing views on display-option notifications. Avoid frozen CGColor values. Amber/ink remains branding. A hidden Settings window should not keep refreshing its table.

First use has one executable-script instruction and the actual Scripts Folder path. Healthy empty state collapses unused diagnostics. Keep Retry scan available and expose complete scan/rejection recovery in a named selectable detail mode; return to the selected script’s Last run details without losing its selection. Recovery clearing removes stale notices.

Preserve diagnostic selection and scroll. Reassigning an unchanged `NSTextView.string` can reset both; a changed value needs a valid selection clamp. Retain the overflow hosting view; skip redundant content replacement while still recomputing geometry when the display changes. Cache identity alone must not prevent Touch Bar href/enabled-state updates. Inspect `Tests/EaveKitTests/NativePresentationTests.swift` and `Tests/EaveApplicationTests/ScriptsPaneTests.swift`.

The documented overflow opening uses a brief opacity transition after final geometry; closing and updates remain immediate and Reduce Motion reaches final state immediately. Headless alpha checks do not establish visible fade quality. Overflow is informational until the actionable-overflow slice is implemented. Touch Bar is attached to Settings, not system-wide. Ordinary script execution does not require all optional OS permissions. The transparent template status mark is distinct from the colored application icon.

## Limits to preserve in copy

Local scripts are trusted code running with the user's privileges. A returned-output cap is not a bound on temporary-file growth while running. A timeout does not establish descendant-process cleanup. Do not advertise full xbar action compatibility, global status-item control or hardware acceptance from unit tests.

## Next-development proposals

Reopen the current `docs/plans/` records, including the original next-development plan and any later theme/journey refinements, before implementation.

| Order | Proposed slice | Decisions and proof required |
|---|---|---|
| 0 | Bound generated output and child lifetime | Separate returned/generated bytes, stdout/stderr, timeout, cancellation and child cleanup. Compare bounded draining with monitored files. Prove concurrent streams cannot deadlock; verify process-group membership before signaling; clean up all fixtures. |
| 1 | Run selected script now | Add a scheduler actor command using existing registration/run identity. Repeated clicks create one process; removal prevents stale UI delivery. UI preserves diagnostics and focus. |
| 2 | Persist local preferences | Versioned application-owned value and injected UserDefaults adapter. Isolated test suite; corrupt/future schema handling. Do not persist OS permission claims or script output. |
| 3 | Actionable overflow | Shared typed supported actions in Core; execution in Kit. Define keyboard navigation, focus restoration and current-registration checks. Unsupported actions remain unavailable. |

These are planned capabilities. Inspect source before saying any is implemented. Native release evidence remains separate from SwiftPM and application typechecking; see [verification](../references/verification.md).
