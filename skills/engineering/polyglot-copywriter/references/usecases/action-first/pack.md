# action-first — use case pack

**Status:** `validated`

Use cases are orthogonal to language. This file teaches **structure**, not vocabulary.

## When to load

Only when the user asks for it by name: "ADHD mode", "ADHD-friendly", "action first", "just tell me what to do", "make this easy to act on". Never apply it to ordinary prose on your own.

Two scopes:

- One piece. A reply, checklist, status note or doc the user wants in this shape.
- Session mode. The user says "adhd mode on" or "stay in action-first mode". Keep the shape on every reply in the session. A new topic does not end it. It ends only on "stop adhd mode", "normal mode" or "stop action-first". Confirm in one line, then go back to the default style.

## Why the shape matters

The reader loses what is off screen, stalls between "I understand" and "I did it", and finds the first step hardest. Time estimates feel flat to them, and a win buried in a recap does not register. So the text must be actionable on first glance, not only short.

1. Do not ask the reader to hold anything in mind. Say it again where they need it.
2. Shrink the gap between knowing and doing. Give the command, path or click.
3. Make the first action small and doable now.
4. Put a number and its basis on every time claim.
5. Show progress where they will see it.

## Sentence 1 job

Something the reader can do right now: a command, a path, a click, or one decision. If a command, path or snippet is the answer, it goes first and prose follows only when it adds something.

## Section order

1. The action, one line
2. Numbered steps, only when there is more than one (one bounded action each, fewest that work)
3. What works now, one concrete line, only when work was done
4. Next: one thing doable in about two minutes

Drop any part that does not apply.

## The ten moves

| # | Move | Weak | Better |
|---|---|---|---|
| 1 | Action first | "CORS is a browser policy that restricts cross-origin requests, so..." | "Set `origin` to `https://app.example.com` in `server/cors.ts:12`, then restart." |
| 2 | Number steps, fewest that work | "Open the config, find the origin, change it, restart, retry." | "1. Edit `server/cors.ts:12`. 2. Run `npm run dev`. 3. Reload `/login`." |
| 3 | End on one next step | "Tell me if you want more." | "Next: reload `/login` and paste the first console error." |
| 4 | Hold tangents | "Also, your lockfile is stale, and the README is old, and..." | Finish the fix. Then: "Separate issue: stale lockfile. Handle it next?" |
| 5 | Restate state every turn | "Done. Ready to continue?" | "Step 2 of 4 done: schema changed. Next: backfill. Run it?" |
| 6 | Time with a basis | "This will take a while." | "About 10 minutes if tests cover it. Unknown if they do not. Check `npm test` first." |
| 7 | Show the win | "I made some auth changes." | "Magic-link login works. Try `npm run dev`, open `/login`." |
| 8 | Errors: place, cause, fix | "Uh oh, something went wrong." | "`build.ts:88` fails: `config/app.json` is missing. Create it from `config/app.example.json`." |
| 9 | Show at most five per group | A flat list of fourteen options | Group them, rank by fit, show the top five, keep the rest for when they ask |
| 10 | No wrapper | "Sure! Let me look. ... Hope that helps!" | Start on the answer. Stop when it is done. |

Notes on the table:

- Tangents. A question that comes up mid-work is not a tangent. Answer it yourself if you can and fold the answer in. If it needs the reader, ask once at the end.
- State. If the harness has a task or plan tool, let it carry the state. Do not also narrate the whole plan.
- Estimates. Never invent a number. Give a basis, give "unknown" with the one thing that would settle it, or mark `[TK: estimate]`.
- Lists. The cap is about what you show. Do not drop relevant items from analysis, search or tool results. When completeness matters, say how many more exist.
- Ranges. Write "lines 42 to 58", not a dash.

## Break the shape when

1. The user asks for an explanation or a walkthrough. Explain fully, with headings so they can skim back. Keep the first-line action only if there is one. No wrapper.
2. The next step is destructive (force push, drop table, delete files). Confirm first. Safety beats brevity.
3. Three turns in a row ended in "still broken". Stop changing code. Name the assumption most likely to be wrong and ask one diagnostic question.
4. The request is truly ambiguous. One short question beats a wrong guess.
5. A rule would delete the answer. "What are my options" gets two to four ranked options with a one-line trade-off each and a recommendation first. The options are the answer.
6. The harness says otherwise. A system prompt outranks this pack. Announce a tool call if it requires that, do the work instead of asking "want me to", and aim time estimates at whoever will run the steps.

## Pre-send check

Delete:

1. The first sentence if it says what you are about to do.
2. The last sentence if it offers more help or recaps.
3. Any "by the way" side note.
4. A hedge that adds no information. Keep a hedge that carries real doubt.
5. An idiom. Say the literal thing.

Then read only the first and last lines. Do they say what to do next, and what just happened? If yes, send.

## Medical boundary

This is a formatting choice. It cannot show whether anyone has ADHD, and it makes no medical claim. If asked, say that in one line and answer the rest.

## With the other polyglot rules

- Preamble, recap and closer are the same tells as §4, §2 and §22 in [humanizer-patterns.md](../../humanizer-patterns.md). This pack never adds back what those remove.
- The no-dash and no-semicolon rule still holds in the final text.
- A reply in a thread still leads with the decision (§26). Here the decision is the action.
- Facts stay true. Estimates need a basis. A gap becomes `[TK: …]` per [substance.md](../../substance.md).

## Default register

`santai` + [simple-prose.md](../../simple-prose.md). Keep `profesional` when the user's context is formal.

## Do not steal from other formats

- Not an essay. A walkthrough keeps its length, and this shape adds a first-line action and headings.
- Not a status report for a manager. The reader is the person who has to act.
- Not a license to cut safety warnings or required detail.

## Aliases (registry)

`adhd`, `adhd mode`, `adhd-friendly`, `action first`, `next step first`, `easy to act on`
