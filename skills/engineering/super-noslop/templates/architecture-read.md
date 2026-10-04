# Architecture read (before backend code)

Declare in one line before generating backend code:

```markdown
**Surface:** `<HTTP API | CLI | worker | migration | client>`
**Trust boundary:** `<what is validated where>`
**Repo pattern:** `<handler style / error type / package path from sibling file>`
```

If you cannot name the repo pattern from a sibling, **read one** — do not invent a new stack silently.

Required for [delivery-gate.md](../references/core/delivery-gate.md) Block 3.
