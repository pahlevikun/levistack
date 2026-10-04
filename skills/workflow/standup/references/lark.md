# Lark: the final polish

Lark comes last on purpose. By now the draft has the work; Lark supplies names, context and the things nobody committed: meetings, decisions, docs, threads.

Flags below were checked against `lark-cli` 1.0.97 `--help`. Use the ISO bounds from `collect.mjs range` (they carry your local offset) and `--as user`; the default output is JSON.

## Gather

```bash
# calendar
lark-cli calendar +agenda --start "<startIso>" --end "<endIso>" --as user

# meetings that happened (needs at least one filter; the time range is one)
lark-cli vc +search --start "<startIso>" --end "<endIso>" --as user
# notes and summaries for the ones that matter; send the files to a temp folder, the default is ./minutes
lark-cli vc +notes --meeting-ids "<id1>,<id2>" --output-dir "<tmp>/standup-minutes" --as user

# chats you wrote in the window (self lookup returns your open_id)
lark-cli contact +get-user --as user
lark-cli im +messages-search --sender "<open_id>" --start "<startIso>" --end "<endIso>" --page-all --as user

# docs you created, and docs you edited or commented on (the edit windows are "mine")
lark-cli drive +search --created-by-me --created-since "<start>" --created-until "<end>" --as user
lark-cli drive +search --edited-since "<start>" --edited-until "<end>" --doc-types doc,docx,wiki --as user
lark-cli drive +search --commented-since "<start>" --commented-until "<end>" --as user
```

`drive +search` times accept `YYYY-MM-DD`, RFC3339, relative like `7d`, or unix seconds. Edit and comment times are aggregated by the hour, so sub-hour precision is not available. The CLI prints a notice when it rounds.

`lark-cli skills read lark-im` and similar print the CLI's own guides when a command misbehaves.

If a call fails with a missing scope, the error names it. Ask the user to run `lark-cli auth login --scope "<scope>"` (with the `!` prefix in Claude Code) and retry. If the user chose to skip Lark, say so at the end of the standup.

## Polish

Work through the draft and use Lark to improve it. Add only what the evidence supports.

1. **Name the work.** Replace "had a sync" with the meeting's real title, and the doc's title for "wrote up the design".
2. **Say what came out of it.** One clause from the notes: the decision, the agreed approach, the action item that became a ticket.
3. **Fill gaps.** A long meeting block with no commits explains a quiet day. A doc edited for hours is work even without a ticket.
4. **Connect.** Link a ticket or MR to the thread or doc behind it. If a chat shows something blocked, put it under Blockers.
5. **Cut.** Drop calendar noise: lunch, focus holds, declined invites, standups themselves. Keep one-on-ones only when they were work ("planning quarter goals"), not by default.
6. **Trim and re-read.** Short, specific, first person, nothing the user did not do.

## Sending is a separate step

Only if the user asks. Confirm the recipient (a chat ID or person), the exact text, and the identity to send as, then:

```bash
lark-cli im +messages-send --chat-id "<oc_...>" --text "<standup text>"
```

That posts to other people and cannot be unsent cleanly. Never send on your own initiative.
