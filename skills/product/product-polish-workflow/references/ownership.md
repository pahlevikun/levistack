# Who owns what in the product skills

Five skills share the product group. Each has one job. Use this map when a task could go to more than one.

| Skill | Its one job | It does not do |
|---|---|---|
| `product-polish-workflow` (this one) | Audit and change a product that already ships. Keeps scope, evidence, code ownership, the journey tracker and verification | Build palettes, systems or new screens from scratch |
| `design-system-kit` | The token system, `DESIGN.md`, platform sizes, governance, and a critique against the system | Choose colors or craft components and motion |
| `color-kit` | Color strategy, palette, roles, modes, contrast proof, stack binding, color audit | Buttons, layout, motion, the token file |
| `ui-ux-kit` | One screen or component: hierarchy, states, motion, UX, platform behavior including car and TV | Palettes, the token file, the journey tracker |
| `prototype-wireframe` | One throwaway answer to one open question, then stop | `DESIGN.md`, a palette, a QA tracker |

## Where each topic lives

| Topic | Owner | Files |
|---|---|---|
| Evidence, scope, severity, closure | this skill | `architecture.md`, `design-audit.md`, `verification.md`, `minimum-result.md` |
| Journey tracker and failure classes | this skill | `journey-qa.md` |
| Refine or redesign decision | this skill | `design-audit.md` |
| Palette, modes, contrast | `color-kit` | its `references/` and `data/` |
| Token layers, type, space, `DESIGN.md`, governance | `design-system-kit` | its `references/` and `specialities/` |
| Components, states, motion, UX rules, platform guides | `ui-ux-kit` | its `references/` and `data/` |
| Throwaway logic, look, shape and flow answers | `prototype-wireframe` | its `references/` and `templates/` |
| Logo and animated identity | this skill | `branding.md` |
| Next-feature plan and handoff | this skill | `delivery.md`, `minimum-result.md` |

## Rules

- Call the owner. Do not copy its rules into this skill.
- A skill names another skill and reads its files only when that skill is installed. A skill that depends on another skill's script says so and has a manual fallback.
- One tracker per product. Rows written by `ui-ux-kit` use the same columns as `journey-qa.md` and join the same file.
- The shipped product is the evidence. Chat claims and old reports are not.
- Optional project examples under `examples/` are samples. They do not constrain other repositories.

This package is a selected synthesis for refining existing products. It is not a lossless archive of every principle. No source artwork, templates or executable code were copied.
