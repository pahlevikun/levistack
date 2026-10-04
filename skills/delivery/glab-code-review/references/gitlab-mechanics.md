# GitLab mechanics

## Read open discussions

```bash
glab api "/projects/:project_id/merge_requests/<number>/discussions" --repo <repo> \
  | jq '[.[] | select(.notes[0].resolvable == true and .notes[0].resolved == false)]'
```

Read CI pipelines and failing job traces before attributing a local lint, test, or build failure to the MR.

## Resolve write context

```bash
eval "$(scripts/mr-context.sh <repo> <number>)"
```

Sets `PROJECT_ID`, `BASE_SHA`, `START_SHA`, and `HEAD_SHA` for inline comments and draft notes.

## Draft notes (preferred write path)

Draft notes are **pending comments** — only you see them until published. The MR author is not notified until bulk publish.

### Post inline draft

Write the complete comment body to a temporary file:

```bash
scripts/post-draft-inline-comment.sh <repo> "$PROJECT_ID" <number> <file> <line> \
  "$BASE_SHA" "$START_SHA" "$HEAD_SHA" <body-file>
```

### Post general draft (no diff line)

```bash
scripts/post-draft-note.sh <repo> "$PROJECT_ID" <number> <body-file>
```

### List pending drafts

```bash
scripts/list-draft-notes.sh <repo> "$PROJECT_ID" <number>
```

The user reviews and edits drafts in the GitLab UI (**Pending comments** / review bar) before publishing.

### Publish all drafts

Only after explicit user confirmation:

```bash
export REVIEWER_STATE=requested_changes   # or reviewed
# Leave SUMMARY_FILE unset to skip a rollup summary note (prefer inline drafts only)
scripts/publish-draft-notes.sh <repo> "$PROJECT_ID" <number>
```

See [draft-review-flow.md](draft-review-flow.md) for the full glab draft workflow. `bulk_publish` posts pending draft notes; avoid a top-of-MR summary wall. `reviewer_state` sets review status but does not replace formal MR approval. **Do not use `approved` for automated reviews.**

## Immediate inline discussion (legacy)

Skip draft when the user explicitly requests immediate publish:

```bash
scripts/post-inline-comment.sh <repo> "$PROJECT_ID" <number> <file> <line> \
  "$BASE_SHA" "$START_SHA" "$HEAD_SHA" <body-file>
```

A design-level finding without a diff line must be a general note (draft or published). Reply to or resolve an existing thread only when explicitly requested and after verifying the current code.

## glab shortcuts (when available)

Newer `glab` versions expose draft management under `glab mr note draft`. Prefer the bundled scripts for consistent JSON payloads across glab versions.
