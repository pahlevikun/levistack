# Draft review flow (glab + GitLab)

Prefer **draft notes** over live discussions. Drafts are visible only to you until published.

## Read MR (always first)

```bash
glab mr view <iid> --repo <group/project>
glab mr diff <iid> --repo <repo>
glab mr view <iid> --repo <repo> --web   # optional: open UI
```

## Resolve SHAs for inline comments

```bash
eval "$(scripts/mr-context.sh <repo> <iid>)"
# PROJECT_ID, BASE_SHA, START_SHA, HEAD_SHA
```

Or manually:

```bash
glab api "/projects/:id/merge_requests/<iid>" --repo <repo> | jq '{base: .diff_refs.base_sha, start: .diff_refs.start_sha, head: .diff_refs.head_sha}'
```

## Post draft inline comment (preferred)

Write the body (markdown + optional suggestion fence) to a file, then:

```bash
scripts/post-draft-inline-comment.sh <repo> "$PROJECT_ID" <iid> <path/to/file> <new_line> \
  "$BASE_SHA" "$START_SHA" "$HEAD_SHA" /tmp/comment.md
```

## Post draft general note (no diff line)

```bash
scripts/post-draft-note.sh <repo> "$PROJECT_ID" <iid> /tmp/note.md
```

## List your pending drafts

```bash
scripts/list-draft-notes.sh <repo> "$PROJECT_ID" <iid>
```

GitLab UI: MR → **Pending comments** (wording may vary by version).

## Publish all drafts (explicit user OK only)

```bash
export REVIEWER_STATE=requested_changes   # or reviewed
# Omit SUMMARY_FILE to avoid a top-of-thread summary note
scripts/publish-draft-notes.sh <repo> "$PROJECT_ID" <iid>
```

This calls GitLab **bulk publish** on your draft notes and optionally sets reviewer state. It does **not** replace human approval.

## glab-native shortcuts (when installed)

Newer glab builds expose draft helpers under `glab mr note` / draft subcommands. The bundled scripts stay canonical for JSON payloads across glab versions. Check:

```bash
glab mr note --help
glab version
```

## Anti-patterns

- Publishing inline comments without a prior draft step unless the user asked
- One giant summary note instead of inline threads
- `reviewer_state=approved` from automation
- Shell-interpolating multiline comment bodies (always use a body file)
