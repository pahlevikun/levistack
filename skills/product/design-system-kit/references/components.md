# Components in the design system

Component craft (states, geometry, motion, UX, platform behavior) is owned by the `ui-ux-kit` skill. This guide says how the design system records components so they stay consistent. Tokens come first (Step 2), so a component only ever uses tokens.

For token file structure (primitive, semantic, component layers), see `specialities/design-system/references/token-architecture.md` and the neighbours `component-tokens.md`, `component-specs.md` and `states-and-variants.md`.

## Required call

At Step 4, load `ui-ux-kit`. It specifies each component with its eight states, geometry rules, variants and native equivalents. Take its `component-spec.md` output and record it here in the system format below.

## What the system records

| Part | Rule |
|---|---|
| Name and purpose | One line, and when not to use it |
| Variants and sizes | Named props: `variant`, `size`, `tone` |
| States supported | The list from the craft spec. A state with no look is a gap |
| Component tokens | Each one **aliases a semantic token** (`button-bg` points to `primary`). A component token never holds a raw value |
| Platform mapping | The native control it maps to on each platform |
| Accessibility | Role, name, announcements, target size, the contrast pairs to measure |
| Owner and status | Who changes it, and whether it is stable, beta or deprecated |

A component token only exists where a component truly departs from the system. One is an exception. Twenty means roles are missing from the semantic layer. Add the role instead.

## The inventory

Build in this order.

| Group | Components |
|---|---|
| Primitives | Text, Icon, Button, Link, Divider, Surface |
| Forms | Input, Textarea, Select, Checkbox, Radio, Switch, Slider, Date picker, Search, One-time code |
| Feedback | Badge, Chip, Toast, Banner, Progress, Spinner, Skeleton, Empty state, Error state |
| Overlays | Dialog, Sheet, Popover, Tooltip, Menu, Command bar |
| Navigation | Tabs, Nav bar, Side nav, Breadcrumb, Pagination, Stepper, App bar |
| Data display | List row, Table, Card, Avatar, Stat, Chart, Timeline, Accordion |
| Marketing blocks | Hero, Feature grid, Pricing, Testimonial, FAQ, Call to action |

Per platform, add what that platform needs (tab bar and swipe actions on mobile, menu bar and split view on desktop, rail and focus card on TV, template list row in a car). The craft skill lists them.

## Packaging so it can be re-themed

- Components read semantic variables or roles. Retheming replaces values, never components.
- One folder per component with its code, its states, an example and its spec.
- Ship the theme as one file and a `DESIGN.md`.
- Export tokens for the stack: CSS variables, Tailwind, W3C design tokens JSON and the platform theme files made by `theme.py bind`.
- For Tailwind v4 map variables with `@theme inline` (the builder writes `tailwind-theme.css`).

## Per platform

Platform sizes come from the builder (`control-height`, spacing and text per platform) and the rules from `references/platforms.md`. The component behavior per platform comes from the platform guides in `ui-ux-kit`.

## Spec record template

```markdown
# <Component>
Purpose: <one line>. Not for: <one line>.
Variants: <list>. Sizes: <list>.
States: <default, hover, focus-visible, pressed, disabled, loading, error, selected>
Tokens: bg `primary`, label `on-primary`, radius `radius-md`, height `control-height`
Platforms: iOS <native control>, Android <native control>, Web <element>, Desktop <>, TV <>, Car <>
Accessibility: <role, name, keys, pairs to measure>
Status: <stable | beta | deprecated>
```
