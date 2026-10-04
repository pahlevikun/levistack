---
name: standup
version: 2.0.0
description: "Write today's standup from what you actually did yesterday: machine history, browser history, GitLab or GitHub (MRs, reviews, comments, reactions), Jira movement, then a final Lark polish. Handles weekends and holidays. Use when the user says standup, daily update, what did I do yesterday, yesterday summary, or standup report. Also runs a read-only multi-branch consolidation room when asked to reconcile worktrees, branches or PRs."
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Task
  - AskUserQuestion
---

# standup

Two jobs share this name. Pick by what the user asked:

- **Daily summary** (default): "standup", "what did I do yesterday". Collect evidence, write the update. Everything below.
- **Branch room**: "reconcile these worktrees / branches / PRs into one". Read [references/branch-room.md](references/branch-room.md) and follow it instead.

## How this works

Memory is a poor record of yesterday; machines keep a better one. Collect from the most local source outward, then write.

1. Machine history: shell, git, AI-coding sessions
2. Browser history
3. GitLab / GitHub: MRs and PRs, reviews, comments, reactions
4. Jira: tickets moved, created, assigned, commented
5. Lark last, to polish: meetings, docs and chats that name and explain the work

Earlier sources find leads, later ones confirm them. A browser visit to a ticket is a lead; a status change by the user is a fact.

## Rules

- **Evidence only.** Every bullet traces to something collected. Nothing invented, nothing inflated: "looked at" is not "worked on", "MR open" is not "shipped".
- **Local and read-only.** Collection reads files and calls read APIs. Never post, comment, transition, or send anything unless the user asks, and confirm recipient and text first.
- **Private by default.** Browser and shell data stay on this machine. Only work-matched sites are read; the collector withholds secret-looking commands and strips URL query strings. Do not paste raw history into the output or into a message.
- **A configured source that fails stops the run.** Say what broke, give the exact fix, and let the user fix it or say "skip X". A source that was never configured is skipped quietly and noted at the end.

## Workflow

```
- [ ] 0 Config and readiness
- [ ] 1 Date range
- [ ] 2 Machine history
- [ ] 3 Browser history
- [ ] 4 GitLab / GitHub
- [ ] 5 Jira
- [ ] 6 Lark (polish)
- [ ] 7 Compose
- [ ] 8 Save
```

### 0. Config and readiness

Settings live in `~/.config/standup/config.json` (or `$STANDUP_CONFIG`). If the file is missing, this is a first run: read [references/setup.md](references/setup.md), ask the user for the few values it lists (repo folders, forge host and username, Jira domain, output folder), and write the file. Do not guess usernames or hosts.

Then see what is available, in one pass:

```bash
for t in git sqlite3 gh glab lark-cli jq; do command -v $t >/dev/null && echo "ok  $t" || echo "--  $t"; done
gh auth status 2>&1 | head -2; glab auth status 2>&1 | head -2
lark-cli auth status 2>&1 | grep -q '"ok": *true' && echo "ok  lark auth" || echo "--  lark auth"
```

Compare against the config. Report every configured-but-broken source together, with the fix from `setup.md`, before collecting anything.

### 1. Date range

```bash
node "${CLAUDE_SKILL_DIR}/scripts/collect.mjs" range
```

Gives `start`, `end`, ISO bounds with the local offset, and unix bounds. The window runs from the last working day through yesterday: Tuesday to Friday is yesterday alone, Monday is Friday to Sunday, and days listed in `holidays` are walked back over. The collector cannot know holidays it was not told. If the whole window turns out empty, ask whether the user was off, and add the dates to `holidays`.

### 2. Machine history

```bash
node "${CLAUDE_SKILL_DIR}/scripts/collect.mjs" machine --start <start> --end <end>
```

Shell commands, commits by the user across every branch of the repos under `repoRoots`, uncommitted edits, and AI-coding sessions with their opening prompts. Commits are the strongest signal; sessions and shell history say what the time went on. Details and manual fallbacks: [references/machine-and-browser.md](references/machine-and-browser.md).

### 3. Browser history

```bash
node "${CLAUDE_SKILL_DIR}/scripts/collect.mjs" browser --start <start> --end <end>
```

Pages visited on work sites: MRs, PRs, tickets, docs, dashboards, runbooks. Use it to find what to look up in steps 4 to 6, and to catch work that left no commit (reading, investigating, reviewing). If it reports permission errors, tell the user how to grant access and offer to continue without. Same reference file.

### 4. GitLab / GitHub

Cover each forge in the config; if none is configured, infer hosts from the `git remote` of the repos found in step 2. Collect what the user raised (MRs/PRs opened, updated, merged), what they reviewed (approvals, changes requested), comments they wrote, and reactions they gave. Commands for both, with the pagination and timezone traps: [references/forge.md](references/forge.md).

### 5. Jira

Tickets the user moved, created, were assigned, or commented on. Prefer the Atlassian MCP when it is connected; otherwise:

```bash
node "${CLAUDE_SKILL_DIR}/scripts/jira.mjs" --start <start> --end <end>
```

Without Jira access, infer keys from branch names, commit subjects, MR titles and browser titles (`[A-Z][A-Z0-9]+-\d+`) and mark them inferred. See [references/jira.md](references/jira.md).

### 6. Lark, last

Calendar, meetings and notes, chats, docs the user created or edited. Use them to polish, not to pad: give a meeting or doc its real name, say what was decided, connect a ticket to the discussion behind it, and catch work the other sources missed. Commands and scopes: [references/lark.md](references/lark.md).

### 7. Compose

Merge before writing. One piece of work usually shows up as a branch, commits, an MR, a ticket, some browser tabs and a Lark doc. Join them on ticket key or branch name into one bullet.

```markdown
# Standup: <weekday>, <date>

## What I worked on (<label from step 1>)
- <one bullet per piece of work, ticket key first when there is one>

## Today
-

## Tickets
- **[KEY-123]** <summary>: <status change>, <MR/PR refs>

## Reviews
- !<number> `<repo>`: <title>, <approved | commented | changes requested>

## Blockers
- <waiting-on items, or "nothing blocking">
```

Write like a person typing in chat: first person, contractions, plain verbs ("worked on", not "executed"), specifics over adjectives. Short. For a multi-day window group by theme, not by day, and mention a day off in half a sentence. Skip weekend lines when there was no weekend activity. If the user has a writing-style skill or notes, apply them.

Leave **Today** empty for the user. In your reply, offer two or three carry-overs (open MRs, tickets still in progress) as suggestions only.

Examples across day types: [references/examples.md](references/examples.md).

### 8. Save

Write the standup to `<outputDir>/<end>.md` (default `~/standups`), where `<end>` is the last day reported. Then show it. Close with one line per skipped source: `_Jira not included (not configured)._`

## When data is thin

- One source empty after auth is fine: skip that section.
- Everything empty: ask whether the user was off. Do not fabricate a day.
- Jira unavailable: infer keys, label them, continue.
- Shell history without timestamps: say so; the other sources still stand.

## Files

| File | Use |
|---|---|
| `scripts/collect.mjs` | `range`, `machine`, `browser`; read-only, no dependencies |
| `scripts/jira.mjs` | Jira activity by the token's owner |
| `scripts/room.mjs` | Branch room CLI |
| `references/setup.md` | Config file, per-tool install and auth, troubleshooting |
| `references/machine-and-browser.md` | What the collector reads, privacy, fallbacks |
| `references/forge.md` | GitLab and GitHub commands |
| `references/jira.md` | Jira queries and the MCP path |
| `references/lark.md` | Lark commands and the polish pass |
| `references/examples.md` | Sample standups |
| `references/branch-room.md`, `references/agent-brief.md` | Branch room mode |
