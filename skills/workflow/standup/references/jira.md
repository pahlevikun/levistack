# Jira

What to collect: tickets the user **moved** (status changes), **created**, **was assigned**, or **commented on** inside the window.

## Which route

1. **Atlassian MCP connected?** Use its JQL search and issue tools with the queries below. No tokens needed.
2. **Otherwise** `scripts/jira.mjs`, which needs `JIRA_DOMAIN`, `JIRA_EMAIL` and `JIRA_TOKEN` (see `setup.md`):

```bash
node "${CLAUDE_SKILL_DIR}/scripts/jira.mjs" --start 2026-10-02 --end 2026-10-04 [--projects ABC,DEF] [--json]
```

3. **Neither:** infer keys from branch names, commit subjects, MR titles and browser page titles with `[A-Z][A-Z0-9]+-\d+`, and label the result "inferred from commits".

## What the script does

It resolves your account ID from `/rest/api/3/myself`, finds candidate issues, then keeps only events authored by **you** inside the window:

```
(assignee = <me> OR reporter = <me>
 OR status CHANGED BY <me> DURING (<start>, <end+1>)
 OR assignee WAS <me> DURING (<start>, <end+1>)
 OR worklogAuthor = <me>)
AND updated >= <start> [AND project in (...)]
```

It requests the changelog and comments together, pages with `nextPageToken`, and prints per issue:

| Event | Source |
|---|---|
| `created` | you are the reporter and the issue was created in the window |
| `moved` | a changelog entry of yours on `status`, for example `To Do → In Progress` |
| `assigned` | a changelog entry of yours on `assignee` |
| `changed` | any other field you changed (sprint, priority, labels) |
| `commented` | a comment of yours, flattened from Atlassian Document Format and clipped |

Issues that matched the query but hold nothing by you in the window are dropped, and the header says how many.

## Reading it

- `In Progress → In Review` or `→ Done` is the movement a standup wants. Say the end state: "moved ABC-12 to In Review".
- A ticket you created is "raised ABC-34". Several field edits on one ticket are noise; one phrase covers them.
- Comments matter when they unblock or decide something; otherwise fold them into the ticket's bullet.
- Match each ticket to MRs, commits and Lark docs by key so one piece of work is one bullet.

## Known limits

- Comments on tickets you neither own, reported, moved nor logged time on are not found by JQL, which has no "commented by" clause. Lark, forge comments and the browser step usually cover them.
- JQL date literals use the Jira user's timezone. The script filters events again by exact time in your local zone, so edge-of-day items are placed correctly.
- Atlassian retired the old `/rest/api/3/search`; the script uses `/rest/api/3/search/jql`. If your site is on a very old Jira Server, use the MCP route or raw `/rest/api/2/search`.
- Self-hosted Jira Data Center authenticates differently (personal access token, bearer). The script is for Jira Cloud.
