# The design brief

Use this at the end of **brainstorm** mode. It turns the conversation into a short written design that someone could plan from without going back to the user. Template: `templates/design-brief.md`.

## Contents
- Size the work
- What goes in
- Where it goes
- The fresh-reader check
- The gate
- After approval

## Size the work

Once the user has picked an approach, say how big the work is in plain words. They can override you.

| Size | The brief |
|---|---|
| **A small change** | A short brief: what you already covered, one or two lines per section. It goes straight to the user, with no fresh-reader check. |
| **A project** | The full brief, then the fresh-reader check. |

Both sizes have an **Approaches** part. If the work grows while you write, stop, say so, and step up a size. If it is really several independent projects, say so, agree an order, and do them one at a time.

## What goes in

- Why this exists, and for whom.
- Goals, non-goals, and **anti-goals** (what would make it a failure even if it technically works).
- Constraints.
- Approaches: the one chosen, the ones turned down, and why.
- The decisions the user made, in their own words.
- **Your calls:** every choice you made for them, marked as yours.
- Open questions.
- What is left to the builder.

## Where it goes

In a software repo, save it as `docs/designs/YYYY-MM-DD-<topic>.md`, unless the repo already has a place for designs. Use the user's path if they give one. Outside a repo, ask. Do not commit it unless the user asks.

## The fresh-reader check

For a project, give the brief to a fresh reader before the user sees it. Use a `general-purpose` subagent with no chat history. Tell the user a reviewer will read it first and that you may come back once with a few questions. Do not hand over the brief until the check is back.

Give the reader this:

```
Role: a skilled <domain>, for example a software engineer.
Situation: you were handed the design brief below and must plan the build. You cannot reach the author.
Read: <path to the brief>
Report: only the questions you would still need answered before you could plan well.
  A question counts only if a wrong guess would matter.
  For each, give the question and why its answer would change the plan.
  Rank them by importance.
Skip: anything the brief leaves to the builder, anything you could decide yourself, and wording nitpicks.
If nothing important is left, say "no open questions".
```

Sort the questions into three piles:

| Pile | Meaning | What you do |
|---|---|---|
| **Answered** | The chat or the repo already answers it | Put the answer in the brief |
| **Minor** | A sensible builder could settle it without changing what gets built | Settle it, and mark it "my call" in the brief |
| **Yours** | Only the user can answer, and the answer changes what gets built | Ask the user |

Bring the "yours" pile in one message, most important first. Update the brief with the answers. Then hand it over with a short list of the calls you made, so the user can check them while reading. That is the only round of questions the check makes.

No subagent tool? Read the brief yourself, as that reader would.

## The gate

**Nothing gets built until the user approves the brief.** This holds for the short brief and the full one.

- Building means writing product code, scaffolding, installing dependencies, creating projects, and starting an implementation skill. Reading and exploring are fine.
- **Two exceptions.** The user opted out of the questions: then this mode is finished, and so is the gate. Or the user said yes to a spike: it may be built, it stays labeled throwaway, and keeping what it made is a new request that comes back through this gate.

## After approval

- A backend or API change: `ready-spec`.
- Anything else that needs a step-by-step plan: `write-plan`.
- Work that is too big to see the end of: the huge-work section of the decision map.
