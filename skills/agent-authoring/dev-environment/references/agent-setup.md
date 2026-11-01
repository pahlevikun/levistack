# Agent setup

Move the agent surface in or out. The place is a raw directory or git. Git is a local repo path or a remote URL.

A setup is skills, rules, agents, commands, hooks, and MCP server entries. `PACK.md` says what the setup is for, what should be present, and how to tell it worked. The files are the setup. This is not a prose-only description.

## Place

| The user gives | Do |
|---|---|
| A directory path | Read or write that directory |
| A local git repo | Read or write that working tree |
| A git URL | Clone into a temp directory to read. Do not push. Do not create a remote repo unless the user says yes |

When they name no source for an export, scan this project (`skills/`, `agents/`, `rules/`, `commands/`, `hooks/`, `.cursor/`) and the user-level config for Claude Code, Cursor, and Codex. Do not scan other products. Do not read chat history unless they ask.

## Export

1. List what you found: path, kind (skill, rule, agent, command, hook, MCP), and one line on what it is. Wait while they drop or add items.
2. Write the pack directory they name. Default is `./setup-pack/` in the current directory when they do not name one.
3. Write `PACK.md` in your own words, then copy the selected files, keeping their relative paths.
4. In MCP config, keep the server name and the variable name. Delete token, key, and password values. Write `<redacted>` in their place.
5. A git destination gets the files only. Commit or push only after a yes.

## Import

1. Read `PACK.md` and the file list from the directory or the cloned URL.
2. Show every file that would be created and every file that would be overwritten. Name the destination. The destination is the directory they name, or this project when they do not.
3. Wait for a yes. Then copy. Do not install packages. Do not run hooks. Do not push.

## Output

Export: the pack path, the file count, and any secret fields you redacted. Import: the destination, the files written, and the files you skipped.
