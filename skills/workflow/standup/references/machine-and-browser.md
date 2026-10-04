# Machine and browser history

What `scripts/collect.mjs` reads, what it hides, and how to do the same by hand.

```bash
node "${CLAUDE_SKILL_DIR}/scripts/collect.mjs" range
node "${CLAUDE_SKILL_DIR}/scripts/collect.mjs" machine --start 2026-10-02 --end 2026-10-04 [--sources shell,git,ai] [--repos ~/code] [--author "Jane Doe"] [--json]
node "${CLAUDE_SKILL_DIR}/scripts/collect.mjs" browser --start 2026-10-02 --end 2026-10-04 [--domains git.example.com,*.wiki.example.com] [--include-all] [--json]
```

Flags override the config file. Output is compact text; `--json` gives the same data structured.

## Machine

| Source | Read from | Gives you |
|---|---|---|
| Shell | `$HISTFILE`, `~/.zsh_history`, `~/.bash_history`, fish history | commands in the window, top tools, distinct commands in order |
| Git | repos found under `repoRoots` (3 levels deep) | the user's commits on every branch, uncommitted files edited in the window |
| AI sessions | Claude Code transcripts under `~/.claude/projects` | per project: sessions, prompts in the window, the first few prompts |

How to read it:

- **Commits** are the firmest evidence. Group them by branch or ticket key.
- **Shell tools** show the shape of the day: a run of `git rebase`, `kubectl`, `terraform plan` or test commands says what kind of work it was. Do not list commands; name the work.
- **AI sessions** show topics and the repos they touched. A prompt is intent, not outcome: confirm it against commits before claiming it.
- **Uncommitted files** edited in the window are work in progress; say "started on" rather than "finished".

Shell history is only usable when it carries timestamps. zsh needs `EXTENDED_HISTORY`, bash needs `HISTTIMEFORMAT`, fish always has them. The collector says how many lines it had to ignore.

Not collected: Cursor, Codex and other editors' session stores, IDE activity, terminal scrollback. Ask the user if one of those mattered.

## Browser

Reads the history database of Chrome, Arc, Brave, Edge, Chromium, Vivaldi (every profile), Firefox and Safari (macOS). The live database is locked by the running browser, so the collector reads a temporary copy and deletes it. Needs the `sqlite3` CLI. Windows is not supported natively; WSL counts as Linux.

It keeps only visits that look like work:

- hosts in a built-in list (code hosting, issue trackers, Lark and Feishu, Notion, Figma, Google Docs, Slack, Stack Overflow, observability and cloud consoles, localhost) plus `workDomains` and `--domains`
- any host whose path looks like a merge request, pull request or Jira issue (`/-/merge_requests/N`, `/pull/N`, `/browse/KEY-N`), so self-hosted tools are caught without configuration

Everything else is counted, not read: no titles, no URLs. With `--include-all` it also lists the busiest other domains (host and count only), so you can tell the user which to add to `workDomains`. Query strings and fragments are always dropped.

How to read it: pages grouped by host with visit counts. Repeated visits to one MR or ticket suggest real attention; a single visit is a glance. Treat the list as leads for the forge, Jira and Lark steps.

## Privacy and redaction

- Nothing leaves the machine except what you put in the summary.
- Shell commands containing words like token, secret, password, api key, authorization, bearer or credential, `curl -u user:pass`, or a long mixed-case token-shaped string are withheld and counted. Commit hashes are not mistaken for tokens.
- AI-session prompts get the same filter and are clipped to 140 characters.
- Never copy raw history, full URLs of non-work sites, or command lines into the saved standup.

## By hand

```bash
# commits by you on any branch
git -C <repo> log --all --no-merges --author="<name or email>" --since="2026-10-02T00:00:00" --until="2026-10-04T23:59:59" --pretty='%h %ad %s' --date=short

# zsh history with real times
fc -li 1 | awk '$2 >= "2026-10-02" && $2 <= "2026-10-04"'
```

Browser history without the script: copy the `History` file (Chromium) or `places.sqlite` (Firefox) to a temp folder and query the copy with `sqlite3`. Never open the live file.
