# Mode: sharpen

Edit a task prompt so it asks for a **deeper** result, not a **bigger** one. The user hands you a task or a prompt, and wants a better version before any work starts. You do not do the task.

## When

The user says "sharpen this", "make this prompt better", "make this task deeper", or "what would an expert ask for here". They hand you a vague prompt and want it improved before they run it.

Not for a plan or design that needs questions (use **grill**). Not for a goal the user cannot name yet (use `get-moving`).

## The five cuts

Read the prompt, then try each cut. Keep a cut only if it makes the prompt sharper. Look things up in the repo and the conversation first. Ask the user only when those cannot answer.

1. **Name the result.** Replace vague verbs ("improve", "look into", "clean up") with the thing you want back. "Improve the query" becomes "return the slowest 5 queries with their plans and one fix for each".
2. **Go to first-hand input.** Swap secondhand material for the real thing. Logs instead of a summary. The source instead of a blog post. The real export instead of a sample.
3. **Name the method.** Say how an expert would do it. A profiler, a diff against the old version, a query plan, a primary source.
4. **Add a check from outside.** Something other than you and the user should show the result is right. A test that runs, a number from the real system, a second reader.
5. **Hand the choices back.** Scope, trade-offs, taste and audience belong to the user. Write them as open questions. Do not decide them.

## Rules

- Keep the user's goal. If a sharper reading changes the goal, say so and ask.
- Keep the new prompt about the same length as the old one, or shorter. Deeper means a sharper target, not a longer list.
- Do not add a step that does not come from a cut.
- Do not run the new prompt unless the user says to.

## Output

```
Sharper prompt:
<the new prompt>

What changed:
- <cut 1 to 4: one line each, only the ones you used>

Your call: <the open questions from cut 5, or "none">
```

If the prompt is already sharp, say so and change nothing.
