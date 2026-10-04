# Review comments in STE

Write review comments that are short and that the author can act on. Write one line for each finding: the location, the problem, and the fix. Do not add an introduction.

This guide covers bugs and risk. For an over-engineering review, use [../../principles/references/review-over-engineering.md](../../principles/references/review-over-engineering.md).

## Format

`L<line>: <severity>: <problem>. <fix>.`

For a diff with several files, use `<file>:L<line>: ...`.

## Severity words

Use a severity word when the findings are mixed.

| Word | Meaning |
|------|---------|
| `bug` | The behavior is broken. It will cause an incident. |
| `risk` | It works, but it is fragile. Examples: a race, a missing null check, a swallowed error. |
| `nit` | Style, naming, or a small optimization. The author can ignore it. |
| `question` | A real question, not a suggestion. |

Older reviews used the markers 🔴 🟡 🔵 ❓ for the same four levels. Use the words. They do not depend on emoji support.

## Drop

- "I noticed that ...", "It seems like ...", "You might want to consider ...".
- "This is just a suggestion, but ...". Use `nit` instead.
- Praise on every comment. Say it once at the top.
- A restatement of what the line does. The author can read the diff.
- Hedges such as "perhaps", "maybe", and "I think". When you are not sure, use `question`.

## Keep

- The exact line numbers.
- The exact symbol, function, and variable names, in backticks.
- A concrete fix, not "consider refactoring this".
- The reason, when the fix is not obvious from the problem.

## Examples

Wrong: "I noticed that on line 42 you do not check whether the user object is null before you access the email property. This could cause a crash if the user is not found."

Right: `L42: bug: The user can be null after .find(). Add a guard before .email.`

Wrong: "It looks like this function does a lot of things and might benefit from being split into smaller functions."

Right: `L88-140: nit: This 50-line function does four jobs. Extract validate, normalize, and persist.`

Wrong: "Have you considered what happens if the API returns a 429?"

Right: `L23: risk: There is no retry on a 429 response. Wrap the call in withBackoff(3).`

## When to write more

Write full paragraphs, then return to one-line comments, for:

- a security finding (explain it fully and add a reference)
- a disagreement about architecture (the author needs the reasoning)
- a new author who needs the "why"

## Boundaries

Write the review only. Do not write the fix. Do not approve or request changes. Do not run linters. Output the comments ready to paste into the pull request. Say "normal mode" to return to a verbose review style.
