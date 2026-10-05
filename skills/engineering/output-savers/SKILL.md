---
name: output-savers
description: "Engineering principles plus plain STE writing in one skill. Writes the smallest working change (YAGNI, minimal scope, DRY, SOLID, noslop backend filter), reviews for over-engineering, and audits repos for bloat. Replies, commit messages, review comments, and memory files use short Simplified Technical English (pilot and astronaut styles). Detects the job and picks the mode. Use for be brief, save tokens, yagni, minimal scope, is this over-engineered, commit message, review this diff, compress CLAUDE.md, shrink context. Not for prose written for human readers."
metadata:
  version: "3.0.0"
---

# Output savers

One skill with two halves. They work together.

- **Principles** keep the work small. Do less. Delete first. Build only what the task needs. See [principles/](principles/SKILL.md).
- **STE style** keeps the words small and clear. It uses Simplified Technical English with the habits of pilots and astronauts. See [concise/](concise/SKILL.md).

The first half shortens the diff. The second half shortens the reply. Both remove waste without removing facts.

## Step 0: detect the job

Do this first and do not announce it. Signals and intensity rules are in [references/auto-detect.md](references/auto-detect.md).

| If the user is doing this | Apply | Load |
|---|---|---|
| Writing or changing code, or choosing a dependency | Minimal scope and YAGNI. Code first, three short lines after. | [engineering-principles.md](principles/references/engineering-principles.md) |
| Deciding on an abstraction, or adding "just in case" code | YAGNI, the deletion test, SOLID | [yagni.md](principles/references/yagni.md), [solid.md](principles/references/solid.md) |
| Cleaning up duplication | Rule of three, then the jscpd workflow | [dry.md](principles/references/dry.md) |
| Touching handlers, services, config, API text, or comments | The super-noslop filter and the delivery gate | [super-noslop/index.md](principles/references/super-noslop/index.md) |
| Asking if code is over-engineered or auditing a repo for bloat | A tagged cut list or ranked audit | [review-over-engineering.md](principles/references/review-over-engineering.md) |
| Asking for a commit message | A short Conventional Commit, message only | [commit.md](concise/references/commit.md) |
| Reviewing a diff or pull request for bugs | One line per finding, with a severity word | [review.md](concise/references/review.md) |
| Compressing a memory or instruction file | Backup, rewrite the prose in STE, validate | [compress.md](concise/references/compress.md) |
| Delegating work to subagents | Pick the subagent and demand a short result | [crew.md](concise/references/crew.md) |
| Facing a huge input (logs, big files, PDFs, screenshots) | Read less: search, filter, convert | [context-hygiene.md](references/context-hygiene.md) |
| Asking a question, debugging, or needing a procedure | STE: pilot style, or astronaut style for steps | [ste-style.md](concise/references/ste-style.md) |
| Needing prose that a person will read (docs, email, README, release notes) | **Do not compress.** Write plain, complete text. | none |

Order of precedence: safety override, explicit user words, detected job. A security warning, an irreversible action, or an unclear sequence always gets full sentences. Never announce the mode.

## How the halves combine

- **Coding chat:** the principles card decides what to build. STE decides how to say it. Code comes first. Three short lines follow at most.
- **Review:** the review format keeps each finding on one line. The principles supply the tags (`delete`, `stdlib`, `native`, `yagni`, `shrink`).
- **Procedures:** astronaut style writes the steps. The principles decide which steps are needed.

When the two halves disagree, the stricter rule wins. Never use brevity or "do less" to skip validation, authorization, tests, or a stated requirement.

## Layout

| Folder | Holds |
|---|---|
| [principles/](principles/SKILL.md) | YAGNI, minimal scope, DRY, SOLID, super-noslop (R-01 to R-38, delivery gate, comment hygiene), over-engineering review |
| [concise/](concise/SKILL.md) | STE style, intensity files (`light/`, `heavy/`), commit, review, compress, crew, and the TypeScript compress scripts |
| [references/](references/) | Job detection and context hygiene |

## Callers

When another skill calls this one, it names the job. Skip detection.

- `glab-code-review`: apply super-noslop in **after** mode to the comment text. Use the review format for each inline comment. Never write one rollup block.
- `write-mr-description`: apply super-noslop in **after** mode to the description. The description is prose for people, so do not compress it.

## Related skills

- `super-refactor`: the change is a behavior-preserving refactor.
- `super-tdd`: the change is a feature or fix that needs a test first.
- `super-noslop`: filter generated backend, UI or test code.
- `polyglot-copywriter`: the text is for human readers, not for agents.
