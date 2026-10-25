# Setup

One config file, then one login per source. Every source is optional; the more you connect, the less the summary relies on memory.

## Config file

`~/.config/standup/config.json`, or the path in `$STANDUP_CONFIG`. No secrets in it: tokens come from the environment or from each CLI's own login.

```json
{
  "repoRoots": ["~/code"],
  "gitAuthor": "",
  "workdays": [1, 2, 3, 4, 5],
  "holidays": ["2026-12-25", "2026-12-26"],
  "workDomains": ["git.example.com", "wiki.example.com"],
  "forges": [
    { "kind": "gitlab", "host": "git.example.com", "user": "jdoe" },
    { "kind": "github", "user": "jdoe" }
  ],
  "jira": { "domain": "acme.atlassian.net", "email": "jdoe@example.com", "projects": ["ABC"] },
  "outputDir": "~/standups"
}
```

| Key | Meaning | Default |
|---|---|---|
| `repoRoots` | Folders scanned (3 levels deep) for git repos | current directory |
| `gitAuthor` | Name or email to match commits; empty uses `git config --global` | your git identity |
| `workdays` | ISO weekdays that count as working, 1 = Monday | `[1,2,3,4,5]` |
| `holidays` | Dates to walk back over when finding the last working day | none |
| `workDomains` | Extra sites counted as work in browser history; `*.` prefix allowed | built-in list plus forge and Jira hosts you add |
| `forges` | Where MRs and PRs live, and your username there | inferred from git remotes |
| `jira` | Domain, login email, optional project keys | not used |
| `outputDir` | Where standups are saved | `~/standups` |

`collect.mjs` reads `workdays`, `holidays`, `repoRoots`, `gitAuthor` and `workDomains`; `jira.mjs` reads `jira`; the rest is for the agent. Add your self-hosted forge, wiki and Jira hosts to `workDomains`, or the browser step will not see them.

## Tools

| Tool | Needed for | Install | Log in |
|---|---|---|---|
| `git` | commits | preinstalled or your package manager | `git config --global user.name` and `user.email` |
| `sqlite3` | browser history | preinstalled on macOS; `apt install sqlite3` | none |
| `gh` | GitHub | `brew install gh` | `gh auth login` |
| `glab` | GitLab | `brew install glab` | `glab auth login --hostname <host>`; token scope `read_api` |
| `jq` | reading API output | `brew install jq` | none |
| Jira | tickets | none | token below |
| `lark-cli` | Lark polish | `npm install -g @larksuite/cli` | below |

### Jira

Create an API token at `https://id.atlassian.com/manage-profile/security/api-tokens`, then export it from your shell profile or a secrets manager:

```bash
export JIRA_DOMAIN="acme.atlassian.net"
export JIRA_EMAIL="jdoe@example.com"
export JIRA_TOKEN="..."
```

If the Atlassian MCP server is connected, the skill uses that and none of this is needed.

### Lark

```bash
lark-cli config init --new              # blocks and prints a URL; open it to create or bind the app
lark-cli config init --new --brand lark # international Lark tenants; the default brand is feishu
lark-cli auth login --domain calendar,vc,minutes,im,drive,docs,wiki
lark-cli auth status                    # prints JSON; look for "ok": true (the exit code is 0 either way)
```

Both blocking commands wait for you in a browser. In Claude Code run them yourself with the `!` prefix so the output lands in the session, for example `! lark-cli auth login --domain calendar,vc,minutes,im,drive,docs,wiki`. Review what `auth login` asks for and decline write scopes you do not want: the skill only reads. `lark-cli auth scopes` lists what the app allows.

### macOS access to browser history

Chromium browsers and Safari keep history in folders macOS protects. Grant your terminal app access under System Settings, Privacy & Security, Full Disk Access, then restart it. Without that the collector reports "permission denied" for the browser and carries on. Firefox and Linux paths usually need nothing.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Browser step says permission denied | Full Disk Access, above |
| Browser step finds no browser | Unsupported browser or profile path; check `references/machine-and-browser.md` for the list |
| Shell history empty or "no timestamps" | zsh: `setopt EXTENDED_HISTORY`; bash: `export HISTTIMEFORMAT="%F %T "` (applies going forward) |
| No commits found | `gitAuthor` does not match the commit author, or the repo is outside `repoRoots` |
| `glab` 401 | Token expired; `glab auth login --hostname <host>` again |
| `glab` talks to the wrong host | Pass `--hostname <host>` on every call |
| Jira 401 | Wrong email or token; the token belongs to the email that created it |
| Jira returns nothing for `currentUser()` | Use the account ID from `/rest/api/3/myself`; `jira.mjs` already does |
| `lark-cli` scope or permission error | Re-run `lark-cli auth login` with the missing `--domain` or `--scope`, then retry |
| Lark docs search says a scope is missing | The error names the scope; request it with `lark-cli auth login --scope "<scope>"` |
