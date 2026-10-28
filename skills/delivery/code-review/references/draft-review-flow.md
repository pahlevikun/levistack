# Draft review flow (glab + GitLab)

Prefer **draft notes** over live discussions. Drafts are visible only to you until published.

Set `REVIEW_SKILL_DIR` to the absolute directory containing this skill's `SKILL.md` before running bundled helpers. Keep the target repository as the working directory.

## Read MR (always first)

```bash
glab mr view <iid> --repo <group/project>
glab mr diff <iid> --repo <repo>
glab mr view <iid> --repo <repo> --web   # optional: open UI
```

## Resolve SHAs for inline comments

```bash
eval "$("$REVIEW_SKILL_DIR/scripts/mr-context.sh" <repo> <iid>)"
# PROJECT_ID, BASE_SHA, START_SHA, HEAD_SHA
```

Or manually:

```bash
glab api "/projects/:id/merge_requests/<iid>" --repo <repo> | jq '{base: .diff_refs.base_sha, start: .diff_refs.start_sha, head: .diff_refs.head_sha}'
```

## Post draft inline comment (preferred)

Write the body (markdown + optional suggestion fence) to a file, then:

```bash
"$REVIEW_SKILL_DIR/scripts/post-draft-inline-comment.sh" <repo> "$PROJECT_ID" <iid> <path/to/file> <new_line> \
  "$BASE_SHA" "$START_SHA" "$HEAD_SHA" /tmp/comment.md
```

## Post draft general note (no diff line)

```bash
"$REVIEW_SKILL_DIR/scripts/post-draft-note.sh" <repo> "$PROJECT_ID" <iid> /tmp/note.md
```

## List your pending drafts

```bash
"$REVIEW_SKILL_DIR/scripts/list-draft-notes.sh" <repo> "$PROJECT_ID" <iid>
```

GitLab UI: MR → **Pending comments** (wording may vary by version).

## Publish drafts (explicit request)

List pending drafts first. Confirm that every draft on the MR belongs to the exact set the user asked to publish. The command below publishes all pending drafts on that MR; if the sets differ, stop and resolve the mismatch before using it. A generic "ok" is not an instruction to publish.

```bash
export REVIEWER_STATE=requested_changes   # or reviewed
# Omit SUMMARY_FILE to avoid a top-of-thread summary note
"$REVIEW_SKILL_DIR/scripts/publish-draft-notes.sh" <repo> "$PROJECT_ID" <iid>
```

This calls GitLab **bulk publish** on pending draft notes and optionally sets reviewer state. It does **not** replace human approval.

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
