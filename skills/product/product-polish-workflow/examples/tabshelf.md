# Worked example: Tabshelf

Use this reference only for Tabshelf. Its platform, paths and contracts are not requirements for other products.

Paths below are relative to `tabshelf/`. Recheck current source, `ARCHITECTURE.md`, `DESIGN.md`, verification and plans before editing.

## Result shape illustrated here

The Tabshelf engagement left an architecture record (`ARCHITECTURE.md`), a design system (`DESIGN.md`), a verification record (`docs/verification.md`), a visual preview gallery (`docs/previews-calm.md`) and a phased next-development plan (`docs/plans/2026-10-24-polish-and-next-development.md`). The polish addressed real restore, import, privacy, selection and narrow-layout paths. These artifacts illustrate the [minimum result](../references/minimum-result.md) for a full engagement. The gallery shows inspected states; it does not prove every browser mode or future source revision.

## Ownership and source map

| Boundary | Responsibility |
|---|---|
| `src/domain/` | Records and pure validation/mutations |
| `src/services/` | Capture, import, cleanup and restore plans/workflows |
| `src/ports/`, `src/adapters/` | Browser/TabStore contracts and Chrome/storage effects |
| `src/background.ts`, `src/protocol.ts` | Composition, typed commands and mutation ownership |
| `src/ui/`, `src/tabs/`, popup/options | Shared controls/theme and page interaction state |

Keep browser effects out of React and DOM-dependent theme code out of background services. Preserve the existing manifest permission boundary; incidental polish does not introduce accounts, a backend, host permissions or content scripts.

## Storage and import invariants

- Retain the original browser incognito flag until choosing storage. Regular snapshots and collections persist locally. Private `TabRecord[]` use session storage, not persistent snapshots. Regular/private session keys remain separate. The split-incognito background rejects persistent browsing-record writes and pruning.
- One background mutation queue owns each complete fresh-read/modify/write operation: capture, edits, import, pruning, reset and group snapshots. A rejection must not poison later work. Avoid re-enqueueing from inside an already queued operation. This is not cross-profile locking or a transaction across local and session storage.
- Read and preserve **complete collection records** during import. A `{id, name}` projection cast back to a Collection loses notes and other fields even on an empty merge. Merge keeps the complete existing record on matching IDs; it is not generic field-by-field overwrite.
- Validate the complete import document before writes. Inspect `src/services/importPlan.ts` for current schema, UTF-8 byte/tab limits, nested fields, duplicate-ID policy and chronology. Identical duplicate records can deduplicate; conflicting records reject. Replace affects snapshots/collections, not settings.
- Inspect `src/domain/tab.ts` and `src/services/browserTabs.ts` for accepted protocols, file policy, credential/size limits and decoded sensitive query/hash keys. A URL accepted for storage is not certified safe to visit. Imported JSON cannot prove past private-browsing origin.

Reopen `src/background.integration.test.ts`, `src/privacy.test.ts`, `src/services/importPlan.test.ts` and mutation/adapter tests. Pure planner tests alone do not exercise background wiring.

## Restore and asynchronous UI

Collection restore preserves saved order. Group tabs using the actual IDs returned by that restore operation; a before/after browser-tab difference can capture unrelated concurrent tabs. Audit each caller: a repaired ordinary restore path does not establish that every legacy group path is repaired. Chrome recent-window fixtures must use the real nested `session.window.sessionId` and `session.lastModified` shape.

Bind loaded detail to its entity ID. When selection changes and the new read fails, old data must not become editable under the new selection. Guard reads and mutation refreshes with current selection/request identity. Late deletion must respect a newer selection.

Creation needs a selection/navigation generation: A → B → A has the same final ID but is a different visit. A stale completion must not take over navigation. Rename also needs an editor-session generation: Cancel → reopen A creates a new editor. Late Save responses and deferred focus must not close/refocus that new editor, even when the record ID matches. Test both success and failure with preserved drafts. Clearing a search cancels stale results and pending state. Show confirmed command responses, with one owner for success announcements; clear obsolete success at the next command. Preserve input on errors.

Inspect `src/tabs/collections.tsx`, `src/ui/search.ts`, `src/ui/workflows.test.tsx` and client tests for these contracts.

## UI, theme and brand

`src/ui/theme.css` owns semantic tokens and `tokens.ts` exposes typed references. `constants.ts` is not another palette. The documented calm refinement maps Estuary reference stops through semantic roles. Preserve System/Light/Dark and native field color-scheme/accent behavior; browser group colors remain domain data. Validate actual visible text and consumed state pairs, not only raw token values.

Collection restore controls precede the labeled Note. Collections/Timeline retain a true heading with an explicit Rename action. Quiet Delete opens a named confirmation with Cancel; key confirmation by record identity and preserve async mutation guards. Full selected-tab titles/URLs wrap with responsive actions. Narrow navigation occupies a full-width horizontal row; move conflicting inline flex sizing into the responsive stylesheet. Switch motion uses transform; selection/content updates stay immediate. Reduced Motion preserves final states and Forced Colors tests must verify semantic aliases rather than automatically forced body text.

`AppShell` owns real navigation links and one main landmark. `SplitPane` owns responsive rail/detail behavior, Back focus restoration and narrow new-collection form visibility. Use `DESIGN.md` for current breakpoints, spacing and control sizes. Derive review widths from the current design system; the documented matrix included 375/390/480/768/1280 for pages and 360 for the popup document. Check both popup appearances and actual native popup containment separately. Coarse controls need measured hit regions, not oversized native checkbox glyphs.

The brand import in `src/ui/Brand.tsx` uses `data-base64:../../assets/brand-mark.svg`. A `~assets` alias resolved under `src/` and failed production bundling despite passing mocks/typechecks. Verify current bundler rules with the real package after changing asset paths.

## Next-development proposals

Reopen current `docs/plans/` records, including the next-development plan and any later theme/journey refinements, before implementation.

| Slice | Required contract |
|---|---|
| Selective restore | Exact preview with source revision and selected positions; positions handle duplicate URLs. Re-read source/current tabs at confirmation; reject stale revisions. Report actual opened/skipped/partial-failure results. |
| Local trash and undo | Versioned complete records, retention/storage budget, collision recovery, expiration, reset/export policy and migration. Keep private records out of persistent trash. Use the existing mutation owner; restore focus after undo. |
| Portable saved groups | Stable local IDs distinct from native Chrome group IDs; schema migration from older imports; title/color/collapsed state and membership. Restore windows/tabs before groups and report partial group failures honestly. |

These are proposals, not shipped behavior. Broader privacy, accessibility and release evidence require the real browser matrix in [verification](../references/verification.md).
