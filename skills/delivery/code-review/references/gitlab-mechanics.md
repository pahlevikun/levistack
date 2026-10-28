# GitLab mechanics

Set `REVIEW_SKILL_DIR` to the absolute directory containing this skill's `SKILL.md` before running any helper below. Keep the target repository as the working directory; use the quoted absolute helper path.

## Read open discussions

```bash
glab api "/projects/:project_id/merge_requests/<number>/discussions" --repo <repo> \
  | jq '[.[] | select(.notes[0].resolvable == true and .notes[0].resolved == false)]'
```

Read CI pipelines and failing job traces before attributing a local lint, test, or build failure to the MR.

Read the full discussion body and current resolved state before drafting a finding or addressing a thread. The first note alone may not contain the latest answer. Distinguish a reviewer's question from an accepted change request.

## Verify the review target

Record the project path, MR IID, `HEAD_SHA`, and pipeline ID in the preview. Read source at `git show <head-sha>:<path>` when the working tree is on another branch or contains unrelated edits. Confirm every inline anchor belongs to a changed line in the current diff. Refresh the context immediately before writing a draft; if the head changed, recheck the finding and suggestion.

When a pipeline fails, inspect its jobs and the relevant failing trace. State which job and pipeline supplied the evidence. A local toolchain failure is not automatically an MR regression. When safe local tests are unavailable, report that separately from CI status.

## Resolve write context

```bash
eval "$("$REVIEW_SKILL_DIR/scripts/mr-context.sh" <repo> <number>)"
```

Sets `PROJECT_ID`, `BASE_SHA`, `START_SHA`, and `HEAD_SHA` for inline comments and draft notes.

## Draft notes (preferred write path)

Draft notes are **pending comments** — only you see them until published. The MR author is not notified until bulk publish.

### Post inline draft

Write the complete comment body to a temporary file:

```bash
"$REVIEW_SKILL_DIR/scripts/post-draft-inline-comment.sh" <repo> "$PROJECT_ID" <number> <file> <line> \
  "$BASE_SHA" "$START_SHA" "$HEAD_SHA" <body-file>
```

### Post general draft (no diff line)

```bash
"$REVIEW_SKILL_DIR/scripts/post-draft-note.sh" <repo> "$PROJECT_ID" <number> <body-file>
```

### List pending drafts

```bash
"$REVIEW_SKILL_DIR/scripts/list-draft-notes.sh" <repo> "$PROJECT_ID" <number>
```

The user reviews and edits drafts in the GitLab UI (**Pending comments** / review bar) before publishing.

### Publish all drafts

Only after explicit user confirmation:

```bash
export REVIEWER_STATE=requested_changes   # or reviewed
# Leave SUMMARY_FILE unset to skip a rollup summary note (prefer inline drafts only)
"$REVIEW_SKILL_DIR/scripts/publish-draft-notes.sh" <repo> "$PROJECT_ID" <number>
```

`draft-review-flow.md` gives the full GitLab draft workflow. `bulk_publish` posts pending draft notes; avoid a top-of-MR summary wall. `reviewer_state` sets review status but does not replace formal MR approval. **Do not use `approved` for automated reviews.**

## Immediate inline discussion (legacy)

Skip draft when the user explicitly requests immediate publish:

```bash
"$REVIEW_SKILL_DIR/scripts/post-inline-comment.sh" <repo> "$PROJECT_ID" <number> <file> <line> \
  "$BASE_SHA" "$START_SHA" "$HEAD_SHA" <body-file>
```

A design-level finding without a diff line must be a general note (draft or published). Reply to or resolve an existing thread only when explicitly requested and after verifying the current code.

## Address open threads

For a request to fix review threads, inventory every open thread and record its current disposition. Inspect the source and contract before changing code. Group threads that share one cause, then run the project's checks against the fix. Local fixes do not authorize a commit, push, reply, or resolution.

If the user authorizes a remote reply with a commit link, push only when that push is also authorized. Confirm that the commit is reachable at the linked remote URL before posting. Reply to each addressed thread with the actual change and link. Resolve only threads whose requested fix was made and verified. Leave advice, unanswered product decisions, and blocked issues open, with their reason.

## glab shortcuts (when available)

Newer `glab` versions expose draft management under `glab mr note draft`. Prefer the bundled scripts for consistent JSON payloads across glab versions.
