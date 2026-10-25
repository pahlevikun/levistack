# Catch up

Use this when the user comes back to a long chat or an unattended run. They say things like "catch me up", "what did I miss", "where are we", or "what is waiting on me". You tell them what changed since their last message, and which decisions are theirs to make.

This mode is read-only. Do not change code, start jobs or post anything while you catch someone up.

## Contents
- Collect
- Write three blocks
- Pictures
- Do not

## Collect

Gather these first:

- What you did since the user's last message.
- Reports from subagents, and messages from other people in the chat.
- The live state of anything you will name: PRs, branches, jobs. Check it with a read-only command (`git`, `gh`, `glab`) before you say where it stands.
- Every **open ask**: a decision, an approval, an irreversible step, or access that only the user has. Include asks from before their last message if they are still open. Work you can still do yourself is not an open ask. Do it, or say you will.

## Write three blocks

Write like you are talking to a coworker. Use `polyglot-copywriter` for the wording. Say what changed for the user, not how you did it. Write "the tests pass", not "CI is green". Skip hashes, paths and commands unless the user needs them to act.

### 1. Headline
One sentence. Either what needs the user, or "nothing needs you right now". If nothing happened and nothing waits, say that and stop.

### 2. Since you left
A short list, one line per outcome. Mark each as done, still running, failed or not checked. Every line must make sense on its own. Keep it near 100 words, less if little happened. Skip work that changed nothing for the user. Never mark something done if it still waits on the user.

### 3. Needs you
One entry per open ask:

```
Decision: <the question, in one line>
My pick: <your choice, and the reason>
What changes: <what users or the project will see>
Risk: <low, medium or high, and why>
```

- Name each PR or issue by its number or link.
- Several items share one decision? Write the decision and your pick once. Then give one line per item, riskiest first.
- A choice between options? List each option with what it gives and what it costs. Those costs are the risk, so skip the Risk line.
- Mention the cost of waiting only when it is more than a delay, for example a deadline.
- If a step must happen first, or cannot be undone, put it inside your pick.

## Pictures

Draw only when a picture explains faster than words. Good cases: how parts connect, a stack of PRs with the state of each, a before and after, options side by side. Use a Mermaid diagram or a screenshot the work already made.

- At most six boxes, and at most eight words per box.
- No status lists and no loose boxes with nothing connecting them.
- Never invent a number. Never draw a screen you did not capture.
- A visible change with no screenshot gets the note "no screenshot yet" and a line on what changed on screen.

## Do not

- Retell the whole session. The user asked what changed and what waits.
- Ask for a decision without giving a pick.
- Start work, post, or change anything while catching up.
