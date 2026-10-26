# Design doc figures

Add figures to a design doc. This skill does not write the full document.

## Templates

Copy from `templates/` in this skill:

| Template | Use |
|---|---|
| `design-doc-skeleton.md` | Title, context, goals, constraints, figure list, open questions |
| `architecture-figure-outline.md` | Checklist for system, deployment, and sequence figures |

Fill placeholders. Keep figure sources as `.mmd`, draw.io, or Excalidraw beside the doc.

## Who owns what

| Piece | Owner |
|---|---|
| Requirements, scope, acceptance | `ready-spec` |
| Narrative, publishing, doc site | `create-documentation` |
| Diagram source, exports, evidence ledger | `diagram` (this skill) |

## Typical system design figure set

1. Context (actors and systems).
2. Container or deployment view (where it runs).
3. One sequence for the main success path.
4. Optional state or ER view when behavior or data needs it.

Each figure gets its own source file, theme, and receipt line.

## Review

Before merge, every edge must map to evidence or be labeled proposed. Link each figure from the doc with alt text and the source path.
