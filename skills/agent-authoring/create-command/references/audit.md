# Command audit checklist

Read the whole command before scoring. Where the repo has its own validation (for example `npm run validate`), run it first. Score each item pass or fail, report `passed/total`, and list failures by priority.

## Checks

| # | Check |
|---|---|
| C1 | The file is where its tool reads commands, and the filename is the intended `/name` |
| C2 | `description` is present, one quoted line, says what the command does, and has no `<tag>` placeholders |
| C3 | `argument-hint` is present when it takes arguments, and absent when it does not |
| C4 | Arguments are used, and the body says what each value is and what to do when it is empty |
| C5 | The body states the outcome and the output (a path, a summary, text to return) |
| C6 | Every side effect (commit, push, post, delete) is named, with the guard ("do not push") |
| C7 | `allowed-tools` pre-approves only what the command needs; no broad `Bash(...)` for a risky action |
| C8 | A state-dependent command reads the state first (status, diff, the file) |
| C9 | No shell injection in a shared command; no secrets or personal paths |
| C10 | It does not copy a skill's procedure; it points to the skill |
| C11 | It is short (about 30 lines) and does one thing |
| C12 | A command and a skill with the same name do not both exist unintentionally (the skill wins) |

## Judge in context

| Type | Weigh |
|---|---|
| Simple, no state, one action | Dynamic state and tool scope may not matter; a short prompt is fine |
| State-dependent (git, environment) | Not reading the state is a real defect |
| Security-sensitive (push, deploy, delete, publish) | Missing tool scope or missing guard is critical |
| Delegating (invokes a skill or subagent) | A thin wrapper with `allowed-tools: Skill(name)` is right; success is that it invoked the target |

Explain why each finding matters for this command. Flag over-engineering (a 100-line command, several outcomes) as well as under-specification.

## Report format

Cite `file:line` for every finding and check the line numbers before reporting.

```
Score: 9/12

Assessment
One or two sentences on whether the command is fit for purpose.

Broken
- C1 (commands/ship.md): the file is in `command/`, not `commands/`; the tool will not see it. Fix: move it.

Weak
- C7 (commands/ship.md:4): `allowed-tools: Bash(git *)` also approves `git push --force`. Fix: list add, status, commit.

Polish
- C4 (commands/ship.md:9): `$ARGUMENTS` is used but the empty case is not described. Fix: add "If empty, use the current branch."

Strengths
- Ends with "Do not push", which makes the side effect explicit.

Context
Type: security-sensitive. Length: 22 lines. Effort to fix: low.
```

Every finding gets a concrete fix. Say "no findings" when there are none. Make no edits during an audit.
