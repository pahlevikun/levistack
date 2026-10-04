# Delegating to subagents with short results

A subagent result goes into the main context as it is. A long result costs context every time. Ask each subagent for a short, structured result. Across 20 delegations in one session, this is the difference between a full context and a finished task.

Three roles cover most work: an **investigator** (finds code), a **builder** (makes a small edit), and a **reviewer** (reads a diff).

## When to delegate

| Task | Use |
|---|---|
| "Where is X defined? What calls Y? List the uses of Z." | Investigator |
| The same question, with suggestions or architecture comments | A normal explorer, in prose |
| A small edit in 1 or 2 files, with an obvious scope | Builder |
| A new feature, 3 or more files, or a cross-cutting refactor | The main thread, or a planner |
| A diff, branch, or file to check for bugs | Reviewer |
| A deep review with reasons and alternatives | A normal reviewer, in prose |
| A one-line answer you already know | The main thread. No subagent. |

Rule of thumb: when you want the result in one third of the words, ask for the short contract. When you want prose, ask for prose.

## Output contracts

The main thread can rely on these shapes.

**Investigator**

```
<Header>:
- path:line | `symbol` | short note
totals: <counts>.
```

The answer is `No match.` when nothing is found. Each line starts with the file path and has a line number. Symbols are in backticks. You can search the result with `path:\d+`.

**Builder**

```
<path:line-range> | <change in 10 words or fewer>.
verified: <re-read OK | mismatch at path:line>.
```

The first word of a refusal is one of these: `too-big.`, `needs-confirm.`, `ambiguous.`, `regressed.`

**Reviewer**

```
path:line: <severity>: <problem>. <fix>.
totals: N bug, N risk, N nit, N question
```

The answer is `No issues.` when nothing is found. Findings are sorted by file, then by line. Severity words are defined in [review.md](review.md).

## Map to generic subagents

Use the generic subagents of your setup, and put the contract in the prompt.

| Role | Generic subagent | The prompt must say |
|---|---|---|
| Investigator | `explorer` | Read only. Reply in the investigator contract. No architecture comments. |
| Builder | `implementer` | Scope is 1 or 2 files. Reply in the builder contract. Refuse 3 or more files with `too-big.` |
| Reviewer | `reviewer` | Reply in the reviewer contract. Findings only. |

Pick a small, fast model for the investigator and the reviewer when your runner lets you set a model for each subagent. Keep the session default for the builder.

## Chains

**Locate, fix, verify** (the most common chain):

1. The investigator returns the list of sites.
2. The main thread picks 1 or 2 sites and gives the paths to the builder.
3. The reviewer checks the diff.

**Parallel scout** (a broad search): start 2 or 3 investigators in one message, each with a different angle (definitions, callers, tests). Merge the results in the main thread.

**Single edit** (the site is known): skip the investigator. Give the exact `path:line` to the builder.

## Do not

- Do not use the builder when you do not know the file. Run the investigator first.
- Do not chain investigator and builder for a refactor of 5 files. The builder returns `too-big.` and you lose a turn.
- Do not ask the reviewer for general feedback. It returns findings only. Use a normal reviewer for architecture opinions.
- Do not expect prose. The contracts are short and sometimes terse. When a person will read the result directly, rewrite it in plain sentences.

## Safety

Subagents leave the short format for a security warning, an irreversible action, or any result where a short form could be misread. They return to the short format after that part.
