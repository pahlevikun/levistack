# Git evidence for a short changelog

Collect evidence before drafting. Use local history and the repository's established release process. These commands are read-only. Replace the illustrative refs and path with confirmed values, quote them as arguments, and keep the selected range in working notes.

## Establish the range

```sh
git rev-parse --show-toplevel
git status --short
git rev-parse --is-shallow-repository
git rev-parse --verify 'BASE^{commit}'
git rev-parse --verify 'TARGET^{commit}'
git merge-base --is-ancestor 'BASE' 'TARGET'
```

Use the user's explicit refs when supplied. Otherwise inspect the existing changelog, release tags, and current release branch to select the previous release and target. Do not silently use the newest tag on another release lane. A manifest version, commit date, or tag name does not establish deployment or the release date.

The base is exclusive and the target inclusive. If the target itself is a release tag, do not select that same tag as the previous release. For a date-window request, state the dates, timezone, target ref, and whether the result describes commits or confirmed releases.

An ancestor check that fails needs investigation, not an empty summary. If the project intentionally compares unrelated release branches, explain that scope and inspect the explicit endpoints. Missing refs or shallow history limit coverage. Do not substitute all history or an unrelated tag and claim a complete release.

## Read commits and final behavior

```sh
git log --reverse --format='%H%n%B%n---' 'BASE..TARGET'
git diff --name-status 'BASE' 'TARGET'
git show 'COMMIT' -- 'path/to/component'
git diff 'BASE' 'TARGET' -- 'path/to/component'
```

Read the full body and footers for migration and breaking-change details. Conventional Commit types help discovery but are not a filter: a plain or mislabeled commit may contain the most important public change.

Use path restrictions for a package or component, then inspect shared dependencies and configuration that can affect it. A subject scope is not enough to prove a package boundary. A two-endpoint diff shows the net release change. A three-dot review diff uses a merge base and may answer a different question.

Read relevant tests, schemas, public flags, or product docs at the selected target when a message is vague. Avoid accidentally validating the working-tree version instead. Note tests inspected separately from tests run.

## Collapse work without losing effects

- Group a feature and its follow-up corrections into one consumer outcome when they ship together. Keep separate bullets for independently useful changes.
- Inspect merge and squash history. Do not count a merge summary and all of its component commits as separate delivered features.
- Confirm cherry-picks, carry-forwards, and similar summaries against their diffs before deduplicating. Identical wording does not prove identical work.
- Check reverts against the final diff. A feature introduced and fully reverted before this release needs no announcement. Reverting something already released may be a visible removal, regression, or fix and needs its own accurate note.
- Keep omitted internal-only work and exclusion reasons in working evidence. Do not suppress a real security, privacy, compatibility, or operational change because of its commit type.

Optional PR or release records can explain the evidence, but the release ref still determines reachability. If a remote listing is used, check pagination before claiming complete coverage. Verify public links and any requested contributor credits; do not expose private tracker details or assume the person who merged wrote the change.

## Update an existing record

Identify the intended release or Unreleased section before writing. Reuse the host's generator when that is the authoritative maintained source and a safe preview is available; inspect its output against the Git evidence. Do not install a generator or replace an established format merely for this task.

Preserve earlier accepted entries. If the target heading already exists, edit that entry within scope rather than prepend a duplicate. Preserve a cumulative comparison's original base unless the requested release boundary changes it. A repeated run with the same evidence should not duplicate bullets.

Keep the final report short: name the file or draft, the inspected range, checks, and material gaps. The full commit-to-bullet mapping can remain in working notes. No tagging, publication, version mutation, or external message is part of these evidence checks.
