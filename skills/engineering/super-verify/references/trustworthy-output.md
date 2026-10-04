# Trustworthy output

How to tell that a green result really ran what you think it did. Run `scripts/read-run.mjs` first for the counting; use this file for the traps it cannot see.

## Contents
- A suite that ran nothing
- Wrappers that run part of the suite
- A command that cannot return a positive
- A missing output file
- Which binary ran
- Code at a revision
- A checker that did not run
- Totals versus per-item agreement
- Scores built from categories
- Project-declared gates

## A suite that ran nothing

Zero failures is not a pass when zero tests executed. An unloadable module, an unmet skip condition, a collection error or a filter that matches no tests all exit 0 with an empty summary. Read the executed and passed counts, not just the failure count, and require the passed count to be positive. Where a suite can legitimately skip everything (an optional dependency, service-backed cases), keep one unconditional case so a positive count still means something.

## Wrappers that run part of the suite

A project script that calls a different collector than the configured runner (a class-based discoverer over bare test functions, a hand-listed directory, a package list older than the layout) silently skips what that collector cannot see: no error, only a smaller plausible count. Compare the wrapper's executed count with the configured runner's collection count at the same revision. Before switching a wrapper to the configured runner, read that runner's default options; they can pull in a coverage threshold or another gate.

## A command that cannot return a positive

A pathspec the tool globs differently than it reads, a filter that drops `command not found`, a wrapper that exits 0 on an empty stream: each yields a clean zero that supports whatever is being claimed. Before reading a zero, run a positive control through the same invocation (same tool, ref, filter, shell) and read its output. Never filter stderr on the run that proves the harness works.

## A missing output file

When a wrapper writes findings to a file, a run that never started and a run that found nothing both exit 0 with no file. Require the file to exist before interpreting it.

## Which binary ran

A green run says nothing about what ran. A `PATH` lookup, a stale installed copy, a compiled sibling or the system interpreter can shadow the tree under test. Run `command -v`, resolve symlinks, and compare the reported version or build id with the source you are verifying. For deployed code, run the check through the exact interpreter or entry point the service uses (the scheduler entry, the unit's `ExecStart`, the image's `CMD`). An error about a symbol the deployed code plainly uses is a sign you are on the wrong interpreter, not that the deploy is broken.

## Code at a revision

Extracting a tree at a commit can half-fail and leave what was there before. Compare one file under test with its content at that revision, or compare hashes, before trusting the result. The same check catches a run against the working tree that you believed was pinned.

## A checker that did not run

A checker that failed to run is `ERROR`, not `SKIPPED` and not `CLEAN`. A log that could not be created, output that did not parse, an invocation that errored, a missing binary: each is a failed run. Every per-check status table must carry it as `ERROR`. Verify a checker is available before running it instead of inferring that from its exit code.

## Totals versus per-item agreement

Counts, sums and digests all pass when two items' verdicts are swapped, and two independent errors in opposite directions cancel into a correct total. Make one typed per-item record the authority, cross-check every id against the producer that knows them, and derive summaries from that record. Test with a two-row swap whose totals do not move. For an evidence block you assemble yourself, write down the relation the counts satisfy by construction (baseline plus added equals total) and evaluate it, rather than re-running and reproducing the same reading.

## Scores built from categories

For a score built from weighted categories, a skipped or failed category is reduced coverage. Never redistribute it silently into a clean full score. If no category ran, report no score. Compare two scores only when both covered the same categories; otherwise withhold the delta and say why.

## Project-declared gates

Before a push or PR, read `CLAUDE.md`, `AGENTS.md` and `CONTRIBUTING.md` if they are not already loaded. For each declared check, note what triggers it, its scope, its order and whether it blocks or only warns. Run every check that applies to the action in the required order. Stop at the first unmet blocking gate and name it as the file words it. Report warning-only failures without promoting them to blockers. A release-only requirement (a changelog entry, a version bump) applies to a release, not to an ordinary push. Do not invent gates, widen their triggers or skip one that applies.
