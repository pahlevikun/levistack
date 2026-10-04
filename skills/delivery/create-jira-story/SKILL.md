---
name: create-jira-story
description: "Draft or create Jira stories and tasks with a lean Context/Goal/DoD template and plain-language prose via polyglot-copywriter. Use when breaking work into Jira tickets, writing story text, pasting ticket markdown, or creating issues under an epic (markdown only, acli, or Atlassian MCP)."
---

# Create Jira story

Peer skill: [`polyglot-copywriter`](../../engineering/polyglot-copywriter/SKILL.md) (simple vocabulary, `create-jira-story` use case, default register `santai`).

References: [references/story-template.md](references/story-template.md), [references/jira-create.md](references/jira-create.md).

## Routing

Pick one route from intent. If unclear, ask once:

```
"What should I do with the Jira story?"
Options:
- "Markdown only (I'll paste into Jira)"
- "Create the ticket in Jira (MCP or acli)"
```

| User says | Route |
|-----------|--------|
| paste, markdown only, draft, template, describe the story, no Jira | **A — Markdown only** |
| create in Jira, file the ticket, acli, MCP, add to epic, push to backlog | **B — Create ticket** |

Route **B** still shows the markdown draft for sign-off when the work is non-trivial or the user has not pre-approved the text.

## Clarify first

Ask only for missing facts (skip what the user or repo already gave):

| Topic | Why |
|-------|-----|
| Output route | A vs B (table above) |
| Source material | Spec, doc, MR, chat, or codebase area |
| Count | One story vs breakdown into several |
| Project key and issue type | Story, Task, Bug, etc. |
| Parent epic / link | Required for B when the team uses epics |
| Language | Default English; Indonesian or other if they ask |
| Labels, components | Only if the team uses them |

Do not invent epic keys, dates, or acceptance criteria. Mark unknown facts `[TK]` and ask.

## Workflow (both routes)

1. **Break down** — If the source is large, propose a story list (title + one line each). Confirm before writing full bodies.
2. **Draft structure** — Fill [story-template.md](references/story-template.md). Keep sections lean; merge fluff into Context or drop it.
3. **Polyglot pass** — Load [`polyglot-copywriter`](../../engineering/polyglot-copywriter/SKILL.md) in **rewrite** mode:
   - Use case id: `create-jira-story` (registry pack: section order and ticket tone).
   - Register: `santai` unless the user asked for formal (`profesional` / `baku`).
   - Always load `simple-prose.md` with the core pipeline. Run the humanize pass on section prose, not on code paths or issue keys.
4. **Deliver** — Route A or B below.

## Route A — Markdown only

Emit a single copy-paste ready block per story:

````markdown
### Summary
<imperative title line>

### Description
<full body with ## section headings from the template>
````

For multiple stories, separate blocks with a horizontal rule `---` or numbered headings. Do not call Jira. Tell the user they can paste the **Description** into Jira (wiki/markdown editor depending on site settings).

## Route B — Create ticket

1. Confirm project, type, parent epic (if any), and summary lines.
2. Follow [references/jira-create.md](references/jira-create.md): Atlassian MCP first, then `acli`, then REST, else fall back to Route A with a clear blocker message.
3. Return issue key(s), summary, and browse URL when the site is known.

## Checklist before done

- [ ] Every DoD bullet is testable (QA or reviewer can verify without guessing).
- [ ] Prose passed polyglot simple-vocab rules (short sentences, no AI tell closers).
- [ ] No secrets, employer-only names, or personal paths in ticket text.
- [ ] Route A: user received paste-ready markdown. Route B: create confirmed or fallback explained.
