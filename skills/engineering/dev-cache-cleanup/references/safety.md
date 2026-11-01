# Cleanup boundary

A scan report is untrusted input and never authorizes deletion. The planning
command takes the approved roots again, reclassifies each selected path from
current filesystem evidence, and compares it to the scanned snapshot. The apply
command requires the digest of the exact reviewed plan plus an explicit mutation
flag. Editing the plan invalidates its digest. A digest is an integrity check,
not a signature or proof that the user consented; the agent must obtain consent.

## Eligible and excluded objects

Only recognized generated directories below a bounded project root are eligible.
Some build directories also need an adjacent ecosystem marker. The names, markers,
and sample layouts are in the cache catalog (`references/caches.md`). The tool rejects
tracked content and repositories nested inside a candidate. Generic names such
as `build`, `dist`, `bin`, `obj` and `out` need project-specific investigation and
remain excluded from scripted mutation. A bounded search inside manual `build`,
`dist`, `bin`, `obj`, `DerivedData`, and `Carthage` directories records `.apk`,
`.aab`, `.apks`, and `.ipa` files as separate manual rows. That does not make the
parent directory eligible. Individual oversized files and packaged apps are useful
audit findings but remain manual-only. An extension or size never proves disposability.

Language runtimes, package-manager stores, Go module stores, toolchain shims and
VM/container stores are excluded. In particular, this CLI does not infer a Go
module-cache path from a directory name or invoke a global cache-clean command.
Use the relevant tool's supported operations as a separate, explicitly scoped
workflow when requested. A container disk may hold active databases.

## Current-state checks

The plan preserves device/inode identity for approved roots and recursive names,
lstat metadata and link destinations for target trees. Any observed metadata
change, added/deleted entry, root replacement, path symlink or expired plan causes
refusal. Every target is preflighted before the batch starts, then checked again
immediately before deletion. These are metadata fingerprints, not content hashes;
this local helper is not a security boundary against an attacker who can preserve
metadata or mutate objects concurrently. Stop writers before approval.

The deletion implementation opens directories without following symlinks and
uses descriptor-relative unlink/rmdir calls. The opened root and selected target
must match their approved device/inode identities, binding the destructive step
to the reviewed filesystem objects after preflight. Each opened directory and
encountered item must remain on the approved root's device; mounted subtrees are
refused even when encountered after the metadata checks. Internal symlinks are unlinked as
objects; they never redirect traversal outside the approved tree. Special files,
filesystem boundaries and unsupported safe-deletion primitives cause refusal.
Concurrent changes can still produce a partial removal. A failure stops later
targets, is reported explicitly, and has no automatic rollback. Never claim an
atomic transaction or guaranteed recovery for filesystem deletion.

## Operational review

- Keep audit and approval artifacts outside selected targets and protect their
  access: paths can reveal private project names. New output files use mode 0600.
- A permission failure or skipped link is a coverage gap; inspect the scan's
  `issues` list. A scan with gaps exits nonzero while retaining its report.
- Compare suspiciously incomplete results with an independent read-only size
  inventory of the same approved root. Do not widen scope silently.
- Confirm no build, editor, watcher or package manager is writing to a target.
- Prefer smaller batches when interruption or reinstallation cost matters.
- Report estimated file bytes separately from observed physical disk recovery.
- Do not bypass protection by relabeling a report entry or changing its basename.

## Reading the report

The standalone HTML page needs no server or external assets. It separates eligible
candidates from manual-review-only files and directories, lists category totals,
and gives known byte estimates alongside counts of unmeasured objects. Neither
manual bytes nor unknown sizes inflate the eligible estimate. Search and category
filters apply to both item tables; column buttons sort only their own table and
support numeric byte ordering. Category totals always describe the whole scan,
not only the currently filtered rows. All path/reason text is escaped before it
enters the page. Without JavaScript, the complete tables and totals remain visible.

## Explicit global-cache audit

`scan --audit-home` is a separate read-only option. It inspects the closed
subpath list in the cache catalog (`references/caches.md`) and never scans all of the home
directory. It does not alter the
report's deletable `roots`; all resulting entries carry `scope: global-audit` and
`eligible: false`. Planning rejects those rows even if a caller supplies their
home path again. The CLI does not run a toolchain-cache command or provide a
special override to delete them.

Each cache measurement visits at most 2,000 filesystem objects with a best-effort
half-second iteration budget. Filesystem calls can take longer on slow or blocked
storage; this is a work budget, not a hard process deadline. Measurements use
metadata, not file contents, and never follow links. A missing cache is skipped;
permission failures, links, special objects or exhausted budgets are visible
scan gaps. Incomplete sizes remain unknown, with observed bytes retained only as
partial measurement data, not a complete total. Load-bearing toolchain siblings,
including `.cargo/bin`, lie outside the closed audit list.
