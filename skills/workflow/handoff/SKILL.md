---
name: handoff
description: "Use when ending, pausing, or switching a session, or when resuming one: write a dated handoff note (goals, context, state, checklist, decisions, resume steps) that a fresh session can act on with no chat history, or read the latest one and verify it before continuing."
---

# Handoff

Leave a note that lets a fresh session (or a teammate) continue without re-deriving anything. The reader has zero memory of this session. Write for that reader.

A good handoff answers four questions:

- **Goals:** what are we trying to achieve, and when is it done?
- **Context:** why does this work exist, and what must the reader know first?
- **State:** where did we stop, and what is verified?
- **Checklist:** what is done, and what comes next, in order?

## Write a handoff

1. **Collect facts from the machine, not from memory.**
   - Date: run `date +%F`. Never guess it.
   - Git: `git branch --show-current`, `git rev-parse --short HEAD`, `git status --short`.
   - Tests: use the last result from this session. If you did not run them, write "not run".
   - Links: the issue, the pull request or merge request, and any doc the work depends on.
2. **Pick the file name and place.**
   - Name: `YYYY-MM-DD-handoff-<topic-slug>.md`, for example `2026-10-04-handoff-auth-refactor.md`. The date prefix makes files sort in time order and shows at a glance how old a note is.
   - Place: a `handoffs/` folder at the project root. Use the project's own notes folder instead when it has one (for example `docs/handoffs/`). Use the exact path when the user gives one, even a fixed name such as `HANDOFF.md`.
   - Same topic, same day: update the existing file. Same topic, a later day: write a new file and add `Supersedes: <old path>`.
3. **Fill in [YYYY-MM-DD-handoff-template.md](YYYY-MM-DD-handoff-template.md).** See [2026-10-04-handoff-example-export-limit.md](2026-10-04-handoff-example-export-limit.md) for a filled note. Both file names show the convention. Keep it short. Leave out a section only when it is truly empty, and then write "None."
4. **Run the cold-start check.** Read the note as if you had never seen this session:
   - Does the first screen say what this is, where work stopped, and what to do next?
   - Is every command copy-pasteable, and every path relative to the project root?
   - Is there any "as discussed", "see above", or "the bug we found"? Replace each with the actual fact.
   - Are decisions recorded with a reason, and are unverified claims marked?
5. **Check for secrets.** Write the names of environment variables, never their values. Never paste tokens, keys, cookies, or customer data.
6. **Do not commit the note** unless the user asks.
7. **Reply with** the path, the three-line summary, and a ready prompt for the next session:

   > Read `<path>`. Verify the state it describes. Then continue from the first unchecked item in the checklist.

## Resume from a handoff

Use this when the user says "continue", "resume", "pick up", or names a handoff file.

1. Find the note. The user's path wins. Otherwise take the newest dated file: `find handoffs -name '*-handoff-*.md' 2>/dev/null | sort | tail -1`. The date prefix makes the last name the newest. If it prints nothing, ask the user where the note is.
2. Read all of it before you act.
3. **Verify the state. Do not trust it.** Compare with reality:
   - Branch, `HEAD` commit, and `git status` against the "State" section.
   - Run the test or build command from "Resume" and compare the result.
   - Check that the files and ids it names still exist.
4. Report any drift in two or three lines (for example "HEAD moved by 2 commits", or "the tests fail now"). Ask before you continue if the drift changes the goal.
5. Continue from the first unchecked checklist item. Tick items as you finish them.
6. When you stop, update the note (status, checklist, state), or write a new dated note that supersedes it.

## Pitfalls

- Record decisions and their reasons, not a play-by-play of the session.
- Say what is unverified. "Tests not run" is useful information. A guess written as a fact is harmful.
- Use absolute dates ("2026-10-04"), not "today" or "yesterday".
- Link to long logs, diffs, and docs. Quote only the one decisive line.
- A handoff is not a status report for a manager. Write what the next session needs to act.
- Do not keep stale notes as truth. If you find a note that is wrong, correct it or mark it `Status: superseded`.
