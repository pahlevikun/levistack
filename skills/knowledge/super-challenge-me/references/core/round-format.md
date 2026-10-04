# Round format

Emit questions in this shape every time (any language). Copy `templates/round.md`.

## Rules

- **Number** every question (`Q1`, `Q2`, …). Never bury a decision in prose.
- Each item is **one** decision. Split "what and how" into two numbers.
- **Recommended answer** on the same item, one or two lines, with a why. "I don't know, you pick" is not a rec; if truly open, rec the reversible default.
- **Wait** after one question (default) or after the frontier round.
- Mark **Fact** vs **Decision** when it could be confused (`facts-vs-decisions.md`).
- If you looked something up, add `Source: path` instead of asking.

## Anti-patterns

- Five unnumbered bullets.
- A rec with no question, or a question with no rec.
- Asking the user to paste file contents you can read.
- Changing numbering mid-thread (keep a monotonic Qn).
