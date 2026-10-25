# Logic playground

Use this when the question is "how should this behave?": a state machine, a checkout flow, a permission rule, a retry policy, a pricing rule, a data shape. The user should be able to click through it and see what happens. The person who clicks is often not a developer, so the page speaks their language.

## Shape

One HTML file. No libraries, no build, no server. Everything is inline, so it opens by double-click and survives being emailed. The page has these parts, top to bottom:

1. **The question**, in plain words, at the top of the page (not only in a comment).
2. **State:** the current state, big, with a readable panel of fields. Use labels, not a raw JSON dump. Mark what just changed.
3. **Free play:** one button per event. A button is disabled when the rule does not allow that event now.
4. **Walkthroughs:** one tab per scenario. A tab holds a short story (the situation and what to watch for) and the ordered buttons to press. Starting a tab resets to a clean state, so it runs the same way every time.
5. **What happened:** every move, newest first, with the reason for any refused event.

Add a **Reset** button. Nothing is saved.

## Keep the rule apart from the page

The rule is the part worth keeping. The page is throwaway.

- Put the rule in one `RULE` block that holds data (states, events, who may move where, what each move changes) and a small `step(state, ctx, event)` function.
- `step` is pure. It returns the next state, the next context and a note. It never touches the page, a button or a timer.
- The page calls the rule. The rule never calls the page. Test: could you paste the `RULE` block into the real code with no edits? If not, it is tangled.
- Pick the shape that fits the question: a table of moves (when "which events are legal now" is part of the question), a reducer `(state, action) => state` (when events are plain actions), or a few pure functions (when there is no current state, only transformations).

## Steps

1. Write the question and the rule as data first, at the top of the file.
2. Write `step`. Render the whole page from the data, so changing the table changes the playground.
3. Add plain words for every state, event and field in a `words` table. People click the words, not the code names.
4. Add walkthroughs for the awkward cases: the happy path, one tricky edge case and one move that must be refused. Cases that are easy to reason about on paper do not need a walkthrough.
5. Open it, run every walkthrough, and write down anything surprising. Surprises are the answer. The best ones come as "wait, that should not be possible".

## Skeleton

Start from `templates/playground.html`. Replace the `RULE` block (question, table, words, walkthroughs). Keep the page shell.

## Check

- Click every event in every state once. Look for a state with no way out, an event that is never allowed, and two events that give the same result.
- Run each walkthrough from a clean start. The illegal one must be refused, and the refusal must say why.
- Say the rule in one sentence. If you cannot, the rule is not clear yet.
- Every state, event and field has a plain word.

## Do not

- Add tests. A prototype that needs tests has stopped being one.
- Connect it to a real database. Memory is enough, unless persistence is the question.
- Generalize for "later". One question only.
- Reach for a framework, a bundler or a server. That defeats "double-click and share".
- Ship the page. Only the rule moves on.

## Hand back

Show the rule table, the surprises, and the rule in one sentence. Then ask the user to confirm or change the rule. Only then does a real implementation start. The rule block, once confirmed, is what you lift into the real module.
