# Evidence that matches the claim

A skill/document edit needs package validation and application scenarios, not application builds. Product changes need checks on the affected product surface. Select checks from current instructions, manifests, lockfiles, scripts and CI; record actual installed versions and prerequisites.

## Establish the verification boundary

For every material claim record source state, command or observation, environment, outcome and artifact. Distinguish compilation/typechecking, behavioral tests, production packaging, rendered inspection and interactive/native acceptance. A pass at one level does not establish the others.

Use isolated fixtures, profiles, preferences and temporary files. Do not run installed user scripts, capture unrelated desktop windows or use a personal browser profile as test data. Preserve unrelated processes and resources. Use permitted tools and writable task-local caches; a missing prerequisite is reported exactly. Do not patch vendor code or bypass execution/permission restrictions to make a check pass.

Run focused checks for the changed behavior and required project gates. Broaden or repeat only for new edits, failures or unresolved concerns. Inspect actual output. Save evidence before removing task-owned tools/containers. Check that a disposable build's source, assets, manifest, lockfile and relevant configuration match the delivered working files.

## Behavior and production artifact

- Reproduce reported defects before fixing them. Use observable data, focus, selection, navigation, pending/error state and actual side effects as assertions. Controllable deferred responses expose races better than guessed sleeps.
- For async editors test delayed success/failure, A → B → A, Cancel → reopen the same record, repeated input and removal. Also test submit revision 1 → edit revision 2 in one session: either editing is explicitly blocked while pending or old success/failure preserves the newer draft/editor. Recheck deferred focus as well as visible data. Keep cancellation of an editor distinct from cancellation of an accepted service write.
- Validate complete-record import preservation and no-write behavior on malformed input when those flows change. Test the real mutation owner and boundary wiring; pure planners alone do not establish integration.
- Build the production artifact after asset/import/manifest changes. A mocked asset path or passing typecheck does not prove bundler resolution, native resource inclusion or README embedding.
- Read persisted state and actual returned resource IDs. A success toast alone does not prove capture/restore. For restored tabs, wait for the relevant URLs/order to become observable; group creation can precede navigation metadata. Retain the matched observation rather than racing a separate transient read. Loading completion and registered URLs are different claims.

## UI and motion matrix

Choose representative sizes from the actual product, including a reported failing/minimum viewport. For web apps this often includes narrow, intermediate and wide pages plus popup/panel containment. For native apps use supported device/window classes. Validate real text, long/missing content, scrolling, required empty/pending/error/recovery states, keyboard focus and current navigation.

Exercise Light, Dark and System where supported, both system appearances, explicit overrides, native field color scheme, forced/increased contrast and Reduced Motion. Measure visible control bounds and gaps; do not infer pointer mode from a touch-capable navigator alone. Verify the actual media query and applied rule before diagnosing CSS. Touch emulation may need reapplying after extension-page navigation. Keep native checkbox/radio artwork compact while enlarging its hit region.

Measure consumed semantic foreground/background roles and actual visible text on its composited surface. Include hover, pressed, selected, placeholder and focus. Use the contrast procedure in [design](design.md). Record thresholds, supported color parsing, sampled states and exclusions. Do not count internal slider values, disabled/non-painted text or offscreen content as measured normal text. Native/composite/image cases outside the sampler need separate inspection.

Wait for finite transitions to settle when checking the settled palette. Do not mistake a transient interpolation sample for the final mapping or claim all-frame contrast. For forced-color aliases, compare probes with automatic color forcing disabled against platform colors; automatically forced body text can mask a broken semantic override.

Open the saved screenshots and judge hierarchy, density, alignment, complete content and the intended visual direction. Record which states were inspected and what changed after review. Automated absence of overflow/errors is not an aesthetic review. Same-size captures and an inspected target are required for pixel-parity claims; generated concepts are labeled separately.

Observe actual motion or bounded state samples: property, timing, progress, final hold/state, interruption and Reduced Motion. Verify that disabling or removing animation leaves usable final content and behavior. Static images do not establish playback. SVG optimization requires repeating reduced-motion checks because a raster match can hide deleted CSS.

## Native evidence limits

Inspect the actual owned window/device when available. Confirm capture validity, appearance, viewport and complete controls before using an image as evidence. A zero window ID, blank/partial offscreen render or invalid compositor connection is a failed/unavailable capture, not a clean UI.

In-process native view fixtures can establish the layout, selection, scrolling, focus assignment and actions they execute. They do not prove visible interpolation, rendered native contrast, status-item placement, human keyboard traversal, screen-reader output, live OS preference changes, multi-display behavior or hardware. Keep library tests, app source typechecks, full native packages and desktop/device observations separate. A GUI-only skipped test stays skipped.

Use documented preference APIs and valid appearance fixtures. Do not fabricate unsupported appearance objects or change personal OS preferences to obtain a pass. Any final-state fallback needs a demonstrated condition and a narrow owner; report whether the evidence came only from a disconnected/headless host.

## Browser and host limits

A browser extension must run with real extension APIs in an isolated profile. Serving its HTML over HTTP or stubbing Chrome APIs is not equivalent product evidence. A popup document opened in a tab does not prove the native popup container. Mocked private-storage regressions do not prove real split-incognito worker lifetime. Pointer emulation does not certify a physical touchscreen or screen reader.

If a scanner/inspector cannot support the product protocol, use equivalent direct checks in a valid driver and name the gap. Do not fabricate a scanner pass or rewrite the app to satisfy a tool limitation.

A permitted Docker runtime can provide disposable browser/build verification when the host blocks it. Confirm host/daemon/image architecture; avoid accidental cross-architecture emulation. Use compatible browser/driver versions, a read-only source mount and disposable writable build copy. Install from the frozen lockfile, compare inputs, preserve outputs and remove only task-owned containers. A browser/emulation/tool startup crash is not automatically a product defect.

## Report honestly

Keep passed, failed, skipped and unavailable outcomes distinct. Name source coverage and exact missing prerequisites. Record corrected harness mistakes and rerun results without erasing earlier failures. State what each sample proves and its practical limit. Tests, screenshots and contrast samples do not establish general security, accessibility, performance or release certification.

Optional project examples in [Eave](../examples/eave.md) and [Tabshelf](../examples/tabshelf.md) identify their relevant source paths. Their commands and platform assumptions do not apply to unrelated repositories.
