# Code to diagram

Draw what the code supports. Do not add edges the code does not prove.

## Before you draw

1. Run `codebase-learner` or read the paths yourself until you can cite file anchors for each box and arrow.
2. Fill the evidence guide from `SKILL.md`. Mark confirmed, inferred, unknown, disabled, and proposed.
3. Pick grammar from the Mermaid guide. Use sequence for call chains, flowchart for branching, deployment-style flowchart for hosts.

## Workflow

1. Name the reader and the question (onboarding, incident, review, design review).
2. List actors, stores, and external systems from code and config only.
3. Draft Mermaid with stable IDs. One edge per fact. Label async, retries, and failures when the code shows them.
4. Render with `scripts/mermaid_render.py` or `mmdc`. Pick a presentation theme when the surface needs it.
5. Compare the figure to source. Mark anything you could not verify.

## Patterns

| Source shape | Figure shape |
|---|---|
| HTTP handler to service to DB | `sequenceDiagram` with `alt` for errors |
| Feature flags and branches | `flowchart` with labeled decisions |
| Modules and packages | `flowchart` with subgraph boundaries |
| Schema from migrations | `erDiagram` via the schema guide |

## Examples folder

Use `evals/validation.mmd` for syntax shape only. Do not copy its fictional domain into a real repo.

## Handoffs

- Long prose or API reference pages: `create-documentation` with the `.mmd` and exports attached.
- Spec before build: `ready-spec` owns requirements. This skill owns figure files only.
