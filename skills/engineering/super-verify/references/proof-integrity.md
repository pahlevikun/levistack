# Proof integrity

Evidence only counts if the check itself is honest. This file covers the ways a green result can be manufactured, and what to check before running anything that touches real state.

## Contents
- Do not make the oracle easier
- Fixture versus live
- Tightening validation you cannot test
- Positive path before refusal path
- Before running anything
- Upgrades and migrations
- Dirty tree and isolation

## Do not make the oracle easier

An oracle is whatever decides pass or fail: a test, an assertion, a validator, a snapshot, an acceptance criterion. Evidence is invalid when the change made the oracle easier to satisfy rather than the behavior correct.

- Do not weaken, loosen or delete an assertion to get green.
- Do not skip, quarantine or mark a test expected-to-fail unless the user asked and you say so.
- Do not hard-code the value the test exercises, or special-case the success path.
- Regenerate snapshots and expected output only after reading the diff and justifying each semantic change.
- If an oracle must change, change it in its own step and name it in the report.

## Fixture versus live

Fixtures, mocks, seeded rows, recorded responses and retained captures support deterministic tests. They are not live evidence. Claim live behavior only after a fresh process exercises the real entry point, with subjects that vary independently of the test where that matters. Say which kind of proof you have: "passes against recorded responses" is a different claim from "works against the service".

## Tightening validation you cannot test

When a change moves a parser from lenient to strict (`strict=True`, `validate=True`, a tight regex replacing a permissive one) and the input comes from a secret store, an environment variable or a person, the tests build their input with the canonical encoder and pass by construction. They cannot produce the stray byte the old leniency was absorbing. "It has worked in production for a year" is also zero evidence: the leniency is what hid the byte. Pair the strictness with an explicit normalization step and report the coverage gap instead of calling the change verified.

## Positive path before refusal path

When the positive capability is safe, authorized and in scope, a path that only refuses is incomplete. Verify the refusal, then verify the positive behavior through its real entry point. Do not close the feature until it works.

## Before running anything

Before a suite, migration, seeder or legacy binary runs (a baseline run included), resolve what it will connect to after test overlays apply: the database URL or `DB_*` variables, queue, cache and mail drivers, external base URLs.

- Every target must be disposable: a dedicated test database, a container, a throwaway schema.
- A developer's own dev database is local but not disposable. A shared dev, staging or production service is neither.
- If any target is not disposable, stop and ask which environment to use. A truncating suite or `migrate:fresh` with no test override destroys the data it reaches.
- Stop every server or background process the verification started, and say so in the handoff.

## Upgrades and migrations

For a dependency or framework upgrade, codegen change or migration:

1. **Capture the baseline before the first write.** Run the repo's validation against the existing state, record the exact command set, and save the output (runner log with its summary line, or JUnit XML). A typed-up table or a remembered count is not a baseline.
2. **If the baseline is red, stop and report** before changing anything. Starting on a red base makes every later failure unattributable.
3. **Rerun the same command set** afterward with the same config and environment. A different command set proves nothing.
4. **Diff the tests.** `git diff --stat <base> -- <test paths>`. Deleting, skipping or loosening tests invalidates the proof; name every test the upgrade edited.
5. **Check silent deltas.** For each changelog entry that changes behavior without a compile or test failure (a changed default, a deprecation that now no-ops, an encoding or casting change), point to a test that exercises the call site and passes on both sides. If none exists, add a characterization test on the base first, then re-capture the baseline.
6. Split multi-major or runtime-plus-framework moves into hops that each go green.

## Dirty tree and isolation

First run `git status --porcelain` and note unrelated edits. A green run in a tree with unrelated work-in-progress is not proof for a shared-module change: untracked files and uncommitted edits can supply a missing symbol or mask a break.

To prove the change on its own, check it out clean:

1. Pick a known-good base commit and list the exact files that are yours, including deletions and both sides of renames. No globs.
2. Export the base into a scratch directory: `git archive <base> | tar -x -C "$scratch"`.
3. Copy in only your listed files (or apply a reviewed patch of just those hunks).
4. Confirm the scratch tree holds what you intend: compare a few files byte for byte against the source.
5. Run the build and tests there, against disposable targets.
6. Remove the scratch directory. Never stash, reset or overwrite the caller's files or index.

A clean pass of your change alone is the proof. If it fails while the local tree stays green, the surrounding work was masking a break; investigate that before claiming anything. State the base commit, the file list and the checks you ran.
