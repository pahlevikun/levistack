# Lark (Feishu)

Lark holds several kinds of evidence at once. Treat each as its own source and say which ones you searched.

## What this source holds

| Lark part | Evidence |
|---|---|
| Group chats and threads | Real-time decisions, incident chatter, "why don't we just…" debates |
| Docs and Wiki | Design docs, RFCs, postmortems, runbooks |
| Sheets and Base | Trackers, support queues, incident logs, rollout lists |
| Approvals | Who approved a change or an exception, and when |
| Calendar | When a decision meeting or an incident review happened |

## How to search it

Use the Lark MCP server or the Lark Open API with the user's app token. Check the tool schema first. If it needs auth and auth fails, stop and report the gap.

1. **Author and date window.** Messages from the PR or MR author, or the incident commander, in the days around the merge date or the first-seen time.
2. **Links.** Search for the PR or MR URL, the ticket id, the commit hash, and the error string.
3. **Incident groups.** Incident or on-call groups around the incident window. Read the whole thread, not single messages.
4. **Docs and Wiki.** Search titles and bodies for the feature name, the service, "RFC", "postmortem", "design".
5. **Base and Sheets.** Support queues and trackers: filter by the affected id, the date, or the issue type. Note the record id for the citation.
6. **Approvals.** For an exception or a risky change, look for the approval record and its stated reason.

## What good evidence looks like

- A thread where the team picks an option and says why
- A postmortem doc with a timeline and action items
- A support-queue record with the first customer report and its time
- An approval with the approver's reason

## Pitfalls

- **Chat is casual.** "lol just ship it" is not a decision. Look for considered discussion.
- **Context collapse.** One message out of its thread reads differently. Fetch the thread.
- **Permissions.** Many groups and docs are private. Record what you could not open as a gap.
- **Personal data.** Support records hold names, phone numbers and ids. Quote only what the question needs, and mask the rest (`rules/core/pii-logging.md`).
- **Message links expire or move.** Cite the group name, the date and the sender as well as the link.

## What to return

For each item: the Lark part (chat, doc, sheet, base, approval), its title or group, author, date, the quoted text, and the link or record id.
