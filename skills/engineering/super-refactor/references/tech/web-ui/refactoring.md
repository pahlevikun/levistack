# UI refactor mode

Use **only** when the user asks about visual design, spacing, hierarchy, Tailwind polish, or "UI looks off" — not for backend or logic refactors.

## Core workflow

1. **Grayscale first** — fix hierarchy with size, weight, spacing before leaning on color.
2. **Constrained scales** — spacing (4, 8, 16, 24, 32, 48, 64), modular type steps.
3. **De-emphasize secondary** — labels, metadata, table headers support primary content.
4. **Quick diagnostic** — score hierarchy, spacing, type, contrast; state gaps to reach 10/10.

## Out of scope

- Changing business logic or API calls under the guise of UI cleanup
- Accessibility audit alone (use a11y skills when asked)

Behavior-preserving: layout and styles may change visually but must not remove required information or break interaction contracts the user did not scope.
