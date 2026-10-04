# Jira story description template

Use this shape in the **description body**. The **summary** (Jira title) is separate: one short line, verb-first, no period.

## Sections (lean)

| Section | Required | Content |
|---------|----------|---------|
| Context / Background | yes | 1–3 sentences. Who needs what and why now. No jargon unless the source doc uses it. |
| Goal | yes | One sentence. What changes for the user or system when this is done. |
| Definition of Done | yes | Bullet list. Testable acceptance criteria. Each bullet starts with a verb. |
| Out of scope | no | Bullets only if confusion is likely. Skip when obvious. |
| Technical notes | no | Implementation hints, `file:line` refs, API names, flags. Not a task dump. |

## Markdown layout (one story)

```markdown
## Context / Background

<plain prose>

## Goal

<one sentence>

## Definition of Done

- <criterion>
- <criterion>

## Out of scope

- <optional>

## Technical notes

- <optional>
```

## Multiple stories

- One story per top-level `## <short title>` block in agent output, or one Jira issue per create call.
- Shared background: say so once in chat, then keep each story self-contained (reader may open only one ticket).

## Summary (title) rules

- Imperative or outcome phrase: "Add retry to payment webhook", not "Payment webhook retry story".
- ≤ 80 characters when possible.
- Match team prefix conventions if the user gave them (e.g. ticket key in branch only, not duplicated in title unless they ask).

## Labels and links

- Do not invent epic keys, project keys, or parent links. Use placeholders `[EPIC-KEY]` only when the user has not supplied them.
- Link related docs or MRs when the user provided URLs.
