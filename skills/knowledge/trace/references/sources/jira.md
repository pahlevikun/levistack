# Jira

## What this source holds

- Issues: the problem, the business reason, acceptance criteria
- Comments, and the change log (status, assignee, fix version, priority changes over time)
- Links: blocks, relates to, duplicates, caused by
- Epics and parent issues, which often hold the "why"
- Fix versions and sprints, which tie work to a date

## How to search it

Use the Jira MCP server if one is connected, the `jira` CLI, or the REST API with the user's token (read-only calls only).

1. **Start with the ids** from commits, PR or MR bodies, and branch names (`ABC-123`).
2. **Read the whole issue**: description, every comment, and the change log (`GET /rest/api/3/issue/<key>?expand=changelog`).
3. **Walk the links and the parent**: the epic or parent often says why the work exists.
4. **Search with JQL** when there is no id:
   ```
   text ~ "<feature or error string>" ORDER BY created DESC
   project = <KEY> AND labels in (incident, postmortem) AND created >= -180d
   issueFunction in linkedIssuesOf("key = <KEY-123>")   # if ScriptRunner is installed
   ```
5. **Check the fix version and the dates** for the timeline check.

The `standup` skill has read-only helpers for Jira's document format (`skills/focus/standup/scripts/jira.mjs`), useful when comments come back as ADF JSON.

## What good evidence looks like

- A description that states the customer, the deadline or the rule behind the work
- A comment that records a decision: "we chose B because A needs the billing team"
- A "caused by" link to an incident ticket
- A priority raised right after an incident

## Pitfalls

- **Scope changes**: read the change log, not only the current description.
- **Boilerplate "why" sections** with generic text are not an answer.
- **Restricted issues**: if you cannot open one, record it as a gap. Do not guess its content.
- **Tokens**: never print the token or the auth header in the output.

## What to return

Issue key, title, type, status, the quoted reason, decisive comments with author and date, the links that matter, and the fix version.
