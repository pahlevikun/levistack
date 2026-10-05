# From a conversation

Turn a session where something worked into a skill the next session can reuse. There is no source file, so the work is extraction and judgment, not copying. Do not run this GUIDE when files were classified as another kind.

Worksheet: [harvest.md](../../templates/harvest.md). Write the skill with `create-skill`.

## Is it worth a skill?

Make a skill when at least one holds:
- The task will come back (the user did it twice, or said "we do this every time").
- It took trial and error, and the working path is not obvious.
- The user corrected the agent, and the corrections encode a standard.

Do not make a skill for a one-off, for a fact that is simply true of the repo (that is a rule or `AGENTS.md`), or for something that must be enforced (that is a hook). If the lesson is one sentence, suggest a rule and stop.

## Get the material

1. Use the conversation in context. Re-read it from the start; do not rely on the last few turns.
2. If the user named a **prior session** ("last time we wrote skills", "the previous convert-as-skill session"), find that session's transcripts first and harvest from those, not from a guess. State the transcript path you used. If you cannot see it, ask once.
3. If the current thread is long or was compacted, ask for the transcript path or a pasted summary of the middle. State what you could not see.
4. Ask one question only if the intent is unclear: "Which part should become the skill?" A session often holds several tasks; convert one skill per task.

## Harvest

Fill [harvest.md](../../templates/harvest.md). Pull from the conversation, in this order:

| Extract | From | Becomes |
|---|---|---|
| The goal | The user's first request and the final accepted result | Opening sentence and `description` |
| Trigger words | The user's own phrasing, including how they asked again | `Use when ...` in the description |
| Inputs | What the agent had to ask for or look up | A "before you start" step |
| The working steps | The path that succeeded, with dead ends removed | Numbered steps, each with an observable result |
| Exact commands, paths and flags | Tool calls that worked | Commands in the steps, with variable parts parameterized |
| Corrections and preferences | Every "no, do it like this" and every approved choice | Principles or "Do not" lines, with the reason |
| Traps | Errors hit and how they were fixed | A short "Watch for" list |
| Done criteria | How the user judged it finished | "Done when" |
| Output shape | The format the user accepted | A template or an example |

Keep the user's exact wording for any instruction they dictated. Generalize values that were specific to that session (a ticket id, a branch, a file name) into placeholders such as `<ticket>`.

## Draft and review

1. Pick the shape: one task goes in a single `SKILL.md`; several distinct tasks use a router (see `create-skill`).
2. Show the user a short outline before writing files: proposed name, the full `description`, the step list in one line each, what you dropped, and where it will be saved.
3. Let the user change the scope. Cut anything they did not confirm as a lasting preference.

## Write and test

Write the minimum first. A first version needs the goal, the working steps, the corrections and the done criteria; add examples, edge cases and references when a test shows the need.

1. Write the skill with `create-skill` (template, location, description rules, lint).
2. Test the way the skill will be used: in a fresh session, give the original first request in the user's words. It should trigger and reach the same result without the back-and-forth. Then give one near-miss request that should not trigger it.
3. Adjust by symptom (never triggers: add the user's words; skipped a step: move it into a numbered step). One change per round.
   If you can, also note what a fresh session does with no skill on the same request, so you can tell whether the skill improved anything (`create-skill` `references/maintain.md`).
4. Report the path and say that the conversation is the only test so far.

## What to leave out

- Dead ends, retries and the agent's reasoning narration.
- Secrets, tokens, personal paths, employer-owned names, customer data, pasted tool output.
- Facts that were true only that day (versions, counts, a ticket's status).
- One-time user preferences the user did not generalize.
- Steps the model already knows. Keep what it got wrong or had to be told.

## Example

Conversation: the user asked three times for "a standup note from yesterday's commits", rejected a bullet-heavy format, and approved a three-line format.

Harvest: goal = a standup note from recent commits; triggers = "standup", "yesterday's commits"; correction = no bullets, three lines (done, doing, blocked); command = `git log --since=yesterday --author=<me> --oneline`.

Result:

```markdown
---
name: standup-note
description: "Writes a three-line standup note (done, doing, blocked) from yesterday's commits. Use when the user asks for a standup note or an update from yesterday's commits."
---

# Standup note
1. Run `git log --since=yesterday --author="$(git config user.name)" --oneline`.
2. Write exactly three lines: `Done:`, `Doing:`, `Blocked:`. No bullets. Say "none" when empty.
3. Reply with only the note.
```
