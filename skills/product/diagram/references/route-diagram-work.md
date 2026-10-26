# Route diagram work

Pick one main path before you draw. Load only the guide named in `SKILL.md` for that path.

| User intent (signals) | Primary guide | Notation |
|---|---|---|
| How this code path works, what calls what | Code to diagram | Mermaid sequence or flowchart after evidence |
| Full design doc, ADR, or RFC with figures | Design doc figures | Templates plus `ready-spec` or `create-documentation` |
| GitHub wiki, internal wiki, or Confluence | Wiki and Confluence | Mermaid fence plus PNG or SVG attach |
| Pretty README, slides, or dark doc site | Mermaid presentation | Themed render |
| Terminal, log excerpt, or chat paste | Mermaid presentation (terminal section) | ASCII or Unicode |
| Wardley, journey, Sankey, or editorial poster | Visual type atlas | Often `infographic` or branded figure kit |
| Brand tokens or first diagram in a product | Branded figure kit | SVG or HTML plus `color-kit` |
| Code facts still missing | Evidence plus `codebase-learner` | Any |

When two rows fit, pick the one that names where the diagram will live. A wiki job beats a generic Mermaid task.

If the job is only palette or mode tokens with no figure, stop and use `color-kit`.
