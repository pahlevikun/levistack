---
name: write-changelog
description: "Write concise changelogs and release notes by inspecting Git commits and diffs first, then summarizing meaningful consumer-visible changes. Covers release scope, breaking migrations, deprecations, and existing history. Use when asked to update CHANGELOG.md, summarize commits between versions, draft release notes or App Store updates, or prepare a release history entry. Not for an MR description (write-mr-description), a chat recap, release automation setup, or publishing a release."
metadata:
  version: 1.1.0
  author: levistack
  license: MIT
  group: delivery
  category: delivery
  department: delivery
  related_skills:
    - create-documentation
    - write-mr-description
    - polyglot-copywriter
  tags:
    - changelog
    - release-notes
    - git-first
    - concise
    - migration
    - release
  capabilities:
    - release_notes
    - release_evidence_and_migration
    - git_commit_and_net_diff_review
    - concise_audience_specific_entries
  languages:
    - en

---

# Write a changelog

Inspect Git first, then write the shortest useful account of what changed for the reader. Preserve the distinction between implementation, release, deployment, and verification.

## Inspect Git before drafting

1. Check the repository and working-tree state. Identify the audience, authorized scope, existing changelog, target ref, release boundaries, version scheme, and release channel. Follow local file locations and proceed within the user's existing docs authorization.
2. Validate the range and inspect full commit messages, bodies, changed files, and the relevant diffs before writing a summary. Use [Git evidence](references/git-evidence.md) for commands and range, scope, merge, and revert checks. Confirm the net change at the target revision; neither a commit prefix nor a PR title proves the resulting behavior. Keep unrelated uncommitted work outside a committed release range.
3. Classify user-visible additions, changed behavior, fixes, deprecations, removals, and known issues. Group commits that deliver one outcome, collapse duplicate or carried-forward work, and omit a fully reverted change that never shipped. A small security fix can deserve an entry. Do not hide a real compatibility change because its commit says `fix`, `chore`, or `refactor`.
4. Confirm the release date and deployment status separately. Keep unshipped work under an unreleased heading or label it explicitly. Do not infer a date from a version number or the current day.

Keep a small working map from each proposed bullet to its commits, relevant diff, and release evidence. Record exclusions and unresolved claims there, not in the public entry. If local history, tags, or a boundary is unavailable, state that limitation. Supplied facts can support a labeled draft; they are not proof that Git was inspected or the release inventory is complete.

## Write entries readers can act on

Lead with breaking changes and required migration actions. Name affected users or integrations and explain the before-and-after behavior. A fix states the failure it corrects and the conditions that triggered it, rather than describing the internal diff.

Default to one release heading and a few short bullets. Give each distinct outcome one sentence. Use the natural number of meaningful changes; do not pad a small release or silently omit important changes to reach a word limit. Keep full evidence and internal commit counts out of reader-facing notes.

For a deprecation, give the replacement and verified removal schedule when known. If the schedule is undecided, say so. Verify any compatibility alias or migration command against the target release.

Keep detailed engineering records and client release notes consistent while adjusting depth for their audiences. Link public issues or source records where appropriate. Do not expose private ticket details, internal repository links, credentials, or personal data to clients.

Omit empty categories, routine build/test/refactor noise, raw commit prefixes, and repeated summaries unless they affect the audience. A dependency or infrastructure change still belongs when it changes compatibility, security, privacy, or operator requirements. Keep older release entries intact and add visible corrections according to the project's history policy. A request to summarize a chat is not automatically a request to create a release record.

For App Store or player notes, use plain product language and any supplied character limit. Technical notes retain exact public flags, fields, and migration commands. Follow the existing format instead of adding parallel changelogs, contributor lists, or announcements. Do not invent performance numbers or claim an experimental feature is generally available.

## Output shape

Use the repository's format, or this compact shape:

```text
Version and confirmed release date, or Unreleased
- Consumer-visible change.
- Failure corrected and the condition that triggered it.
- Required migration or adoption limitation, when applicable.
```

The bullets above are slots, not required categories or a fixed count. Add category headings only when the host format or the amount of material needs them. Use exact product terms, flag names, field names, and versions. The entry should tell consumers what changed and what they must do.

## Version suggestions only when requested

Keep the established version scheme. Under SemVer, reason from the verified public contract: incompatible changes may require a major release, compatible additions a minor release, and compatible fixes a patch. A commit prefix alone is insufficient. Respect the project's pre-1.0 and prerelease policy; do not apply a universal starting version or equate every deployment with a new version.

A recommendation explains its evidence and uncertainty. Do not bump manifests, create tags, change CI, open a PR, publish, or announce a release merely to write its notes.

## Verify

- Trace each entry to the named release range or another primary release record. Flag conflicting or missing evidence.
- Check reachability and the net diff, include relevant non-conventional commits, and reconcile duplicate or reverted work. If there are no meaningful changes for the audience, report that result instead of manufacturing bullets or a version bump.
- Check versions, dates, links, migration instructions, and whether the stated change is included in the target release.
- Check that an implementation or tag is not described as a deployment without deployment evidence.
- Review the final entry for short, concrete wording and unsupported numbers. On repeat runs, update the intended entry without duplicating it. Preserve other release entries and the unaffected comparison-link base.
- Verify commands through safe local checks or existing tests. Label unrun instructions. Do not publish a release, change a version, execute production work, or send announcements merely to validate release notes.
- Report the updated document, evidence range, checks, and remaining uncertainty. A documentation request authorizes documentation edits within its scope, not a commit or publication.

Behavior scenarios are in [evals/evals.json](evals/evals.json).

## Related skills

- `write-mr-description`: describe a change under review rather than a release.
- `create-documentation`: update product docs affected by the released behavior.
- `polyglot-copywriter`: refine reader-facing wording without changing the release facts.
