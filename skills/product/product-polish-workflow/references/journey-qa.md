# User-story QA for a broad product audit

Use this when the request covers many features or says to test every user journey. For a narrow fix, add focused cases to the existing test suite instead of creating a new tracker.

## Inventory one observable surface at a time

Confirm the checkout, branch, dirty state, applicable instructions and user-facing boundary. Search for an existing tracker and update it; otherwise create one parseable CSV or spreadsheet in the project's normal documentation area. Preserve current working-tree changes in the tested state unless the user explicitly asks for a clean base. Inventory routes, screens, commands, imports/exports, install and background effects that a user can observe. Do not make rows for private helpers.

Use these 14 columns, in this order: Feature ID, Surface, Feature / capability, User story, Expected behavior based on code, Code anchors, Initial test approach, Initial test command or route, Status, Test result, Errors, Fix status, Retest result, Notes. Evidence goes in Test result and Errors. The failure class is the Status value (see below). A row needs a stable ID, at least one code anchor and expected behavior grounded in current source or docs. Use one row per independently observable capability or important state, not every branch. Validate the tracker structure after edits. Keep the original failure in the row after a fix.

## Exercise and classify

Choose the strongest feasible current-session evidence: real task smoke, focused integration test, existing suite or manual path. An old pass is not a new pass. Use only statuses that distinguish not tested, passed, product failure, UX failure, setup/logistical failure, test-infrastructure failure, environment block and passed after fix. Record the command/route and actual result before marking passed. Classify failures before changing code:

- **Product:** task or data behavior violates the grounded story.
- **UX:** behavior works but its path, wording or feedback misleads or obstructs.
- **Logistical:** repo-owned setup, packaging or scripts prevent the valid path.
- **Test infrastructure:** fixture, race or assertion does not test the contract.
- **Environment:** an external prerequisite is unavailable.

Audit-only work records a proposed remedy; it does not authorize product fixes. If fixes are authorized, reproduce each in-scope defect, change the correct owner, run the focused check and relevant broader gate, then update the same row with retest evidence. Never weaken an assertion to manufacture a pass. After repeated failed approaches, revisit the underlying assumption before another patch. Report untested, blocked and out-of-scope rows honestly.

Finish when every in-scope row has an anchored story, expected result, status and evidence or explicit gap. Report tracker path, failed/fixed counts by class, checks and remaining limits. Do not claim exhaustive coverage beyond the inventoried surface.

## Rows from ui-ux-kit

When `ui-ux-kit` wrote `ux-acceptance.csv`, merge its rows into the canonical tracker. The columns are the same: Feature ID, Surface, Feature / capability, User story, Expected behavior based on code, Code anchors, Initial test approach, Initial test command or route, Status, Test result, Errors, Fix status, Retest result, Notes. Renumber IDs if they collide. Keep its rule ids (for example `TOUCH-02`) in Notes. Validate the merged file with its checker, `node <ui-ux-kit>/scripts/check-acceptance.mjs <tracker>.csv`, or by eye if the skill is not installed.

