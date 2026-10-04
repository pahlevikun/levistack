# Auto-detect: pick the mode for the current job

Run this before you answer. It takes one scan of the user's words, the open files, and the last tool output. Do not ask the user which mode to use. Pick one and apply it. Say nothing about it unless the pick changes the result.

Order of precedence: **safety override**, then **explicit user words**, then **detected job**.

## 1. Safety override (always first)

Switch to plain, full sentences, then return to the mode afterward, when the answer involves:

- a security finding, a secret, or an auth problem
- an action that cannot be undone, such as `DROP`, `rm -rf`, a force push, `git reset --hard`, a production migration, or data deletion
- a sequence where the order of steps matters
- compression that would create ambiguity
- a user who repeats a question, looks confused, or asks for clarification

Use the closed loop for a critical step: read back the target and the effect, then wait for a confirmation.

Never compress these, in any mode: commands, decisive error lines, negations (`do not`, `never`), numbers, versions, contract fields, query predicates, security conditions, and stated limits. Brevity never excuses a missing validation, authorization check, test, or verification step.

## 2. Explicit user words

| User says | Effect |
|---|---|
| "stop STE", "normal mode", "explain in detail", "verbose" | The style is off until the user asks again |
| "STE mode", "be brief", "less tokens", "terse" | The reply style is on at the default level for the session |
| "light", "default", "heavy" (with or without "STE") | Sets the level of the reply style |
| "pilot style", "astronaut style" | Sets the flavor |
| "yagni", "minimal scope", "do less", "simplest solution" | Apply the principles card for this coding job (no session toggle) |

Without an explicit switch, a mode applies only to the job that was detected, and only for that job.

## 3. Detect the job

The first match wins. Several signals for one job make it certain. When two jobs tie, run both in the order listed.

| # | Job | Signals | Mode | Load |
|---|---|---|---|---|
| 1 | **Commit message** | "commit", "commit message", staged changes in context, `git diff --cached` | The message only, in one code block. Never run `git commit` and never stage files. The repo commit rule wins on types, ticket, and length. | [commit.md](../concise/references/commit.md) |
| 2 | **Code review (bugs and risk)** | "review this PR", "code review", "review the diff", a merge or pull request link | One line per finding: `L<line>: <severity>: <problem>. <fix>.` | [review.md](../concise/references/review.md) |
| 3 | **Over-engineering review** | "is this over-engineered", "what can I delete", "simplify review" | Tagged one-liners that end with `net: -N lines possible.` | [review-over-engineering.md](../principles/references/review-over-engineering.md) |
| 4 | **Repo audit** | "audit this codebase", "find bloat" | A ranked cut list. Read-only. One pass. | [review-over-engineering.md](../principles/references/review-over-engineering.md), mode 2 |
| 5 | **Write or change code** | "add", "implement", "fix", "refactor", "build", "write a function", choosing a library | Code first, then three short lines at most. Apply minimal scope and YAGNI. | [engineering-principles.md](../principles/references/engineering-principles.md) |
| 6 | **Abstraction decision** | "just in case", "future-proof", "should I add an interface", "make it extensible", "one more layer" | YAGNI and the deletion test | [yagni.md](../principles/references/yagni.md), [solid.md](../principles/references/solid.md) |
| 7 | **Duplication** | "duplicate", "copy-paste", "clones", `jscpd`, "DRY this up" | The rule of three, then the jscpd workflow | [dry.md](../principles/references/dry.md) |
| 8 | **Backend, API, config, message, or comment surface** | The change touches handlers, services, jobs, migrations, OpenAPI, error or API text, or code comments. "super-noslop" or "noslop". | The purpose test and the delivery gate. Default mode: **during**. Use **after** when the user asks for an audit. | [super-noslop/index.md](../principles/references/super-noslop/index.md) |
| 9 | **Compress a memory or instruction file** | "compress CLAUDE.md", "shrink this todo", a path to a prose `.md` or `.txt` file | Backup, rewrite the prose in STE, validate. Refuse secrets and code files. | [compress.md](../concise/references/compress.md) |
| 10 | **Delegate to subagents** | "spawn", "delegate", "subagent", "save context", three or more independent lookups | Pick the subagent and demand the short output contract | [crew.md](../concise/references/crew.md) |
| 11 | **Huge input** | A log dump, a file over about 500 lines, a PDF or Office file, a screenshot, repeated re-reads | Read less before you reply | [context-hygiene.md](context-hygiene.md) |
| 12 | **Procedure** | "how do I deploy", "runbook", "migration steps", "rollback", "set up", incident steps | Astronaut style: constraints, numbered steps, expected results, GO or NO-GO | [ste-style.md](../concise/references/ste-style.md) |
| 13 | **Question, explanation, or debugging** | "why", "how", "what does", a stack trace, a short technical question | Pilot style: status, cause, action | [ste-style.md](../concise/references/ste-style.md) |
| 14 | **Prose for a human reader** | README, docs, email, announcement, release notes, pull request description, user-facing copy | **Do not compress.** Write plain, complete text. Use `polyglot-copywriter` when it is installed. | none |

Jobs 5 to 8 can stack. A change to an API handler is job 5 plus job 8. Job 13 is the fallback when a reply style is already on and nothing else matches.

## 4. Pick the level

| Job | Reply level |
|---|---|
| 1, 2, 3, 4 | The format is fixed. No level. |
| 5, 6, 7 | Short technical prose; code first for job 5 |
| 8 | Normal technical prose, with findings by rule id |
| 9, 10, 11 | Not a reply style job |
| 12 | Default. Use light for a beginner. |
| 13 | Default. Use light for a beginner or a careful long answer. Use heavy when the user asks for the shortest form. |
| 14 | Off |

A level the user states in the current message beats any default.

## 5. Combine

- **Reply style plus principles** is the normal pair for coding chat. The principles card shortens the diff. STE shortens the words. See [modes.md](../concise/references/modes.md).
- **Context hygiene** pairs with every job. It shortens what you read.
- A fixed-format job (1 to 4) ignores the reply level. The format is the saver.
- When two modes both fit, choose the one that keeps more facts. Compressing the wrong thing loses information. Compressing too little only costs words.

## 6. Say nothing about the pick

Do not announce "STE mode on" and do not name the mode. Apply it. Mention it only when the user asks which mode is active, or when you leave it for the safety override and the reason is not obvious.
