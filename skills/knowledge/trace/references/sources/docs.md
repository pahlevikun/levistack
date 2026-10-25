# Long-form docs (every kind)

Design docs, RFCs, ADRs kept outside the repo, postmortems, runbooks, specs and meeting notes. They live in many tools. Search each one the session can reach, and say which ones you could not.

## Where they live

| Tool | Reach it with |
|---|---|
| Confluence | its MCP server or REST API (`/wiki/rest/api/search?cql=...`) |
| Google Docs, Sheets, Drive | the Google Drive connector or MCP server |
| Notion | `notion.md` |
| Lark Docs and Wiki | `lark.md` |
| SharePoint, OneDrive | the Microsoft Graph connector if there is one |
| Coda, Quip, Dropbox Paper | their MCP server or API |
| Markdown vaults (Obsidian, a docs repo) | the file system or the repo |
| PDFs and slide decks | read them directly. Huge ones go to the `bulk-reader` agent |

## How to search it

1. **Follow links first.** PR or MR bodies, tickets, and code comments often link the design doc. Open those before searching.
2. **Search by name and by words.** The feature name, the service name, the key term, "RFC", "design", "postmortem", "runbook", "decision".
3. **Check the date.** A doc written before the code is a plan. One written after is an explanation. Both count, but say which.
4. **Read the comments and the history.** Doc comments and version history often hold the real debate, and show what changed after review.

## What good evidence looks like

- An "Alternatives considered" section that names the rejected option and why
- A postmortem with a timeline, a root cause and action items
- A runbook step with a warning ("do not run this during peak hours, because…")
- A doc version that changed right before the code shipped

## Pitfalls

- **Stale docs.** A plan that changed later still reads as current. Compare its date with the code.
- **Many copies.** The same doc copied into three tools drifts. Cite the one closest to the code's date.
- **Access.** A doc you cannot open is a gap, not a guess.

## What to return

Title, tool, author, created and last-edited dates, the quoted passage, and the link.
