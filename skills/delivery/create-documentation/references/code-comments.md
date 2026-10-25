# Doc comments in code

Use this to add or improve doc comments (docstrings, JSDoc, module docs) in the project's own style.

## Rules

1. **Follow the language's convention** and the repo's existing comments. Do not introduce a new style.
2. **The first line is a summary that stands alone.** Tools show only that line in lists and hovers. Make it a full thought about what the thing does, not "This function is used to...".
3. **Say what the code cannot say:** what it returns on failure, what it assumes, units, ordering, side effects, and what it does not do.
4. **Add an example when the use is not obvious.** Prefer a runnable one (a doctest or a test the docs tool runs). A runnable example cannot go stale without a failing build.
5. **Cross-link** related functions and types with the language's link syntax.
6. **Do not restate the signature.** Names and types are already visible.
7. **Skip trivial things.** A one-line getter needs no comment.

## Shape

```
<One-line summary of what it does.>

<Returns on success, and what comes back on failure.>
<Assumptions, units, side effects. One short paragraph at most.>

Example:
    <a real call and its real result>
```

Bad: "This module contains various functions related to payments."
Good: "Charges a customer's default payment method for an amount in cents."

## Check

Run the project's doc tool or doctest runner. Fix every broken link and every failing example.
