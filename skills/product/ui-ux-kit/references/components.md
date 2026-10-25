# Components

How to scope, specify and build one component or a small set.

## Contents
- Is this a component job?
- What stays and what is skipped
- The eight states
- Geometry rules
- Anatomy, variants and sizes
- The inventory
- Native equivalents
- Packaging so it can be re-themed
- What to deliver

## Is this a component job?

Route to the component flow when two or more of these are true:

- The brief names a single element: button, input, select, checkbox, switch, slider, card, modal, drawer, menu, tooltip, tab strip, chip, badge, avatar, toast, list row.
- The brief is short and refers to one thing.
- The target is one component file.
- The user says "just the button" or "only this one".

Stay on the screen flow if the brief names several sections, a layout, a page or a whole surface. If it is unclear, ask once: "One pricing card, or the whole page?" When the user does not answer, default to the component. A single artifact is cheap to redirect.

## What stays and what is skipped

Keep:
- The **register** of the surface the component lives in. A button on a dashboard is product register. A button on a launch page is brand register.
- The **existing tokens**, by name. Invent nothing. A button that brings its own hex into a project with a theme is wrong.
- The craft floor: tinted neutrals, no pure white or black, contrast floors, hue-tinted shadows when shadows exist.
- Reduced motion, if the component animates.

Skip, and say so in one line: page skeletons, hero effects, signature moves and rotation. A project's buttons should all look like siblings. Variety across components inside one product is a defect.

## The eight states

Every interactive component ships all eight. This is the one hard gate.

| State | Requirement |
|---|---|
| default | The resting look |
| hover | Pointer feedback, gated behind a hover media query so it never sticks on touch |
| focus-visible | A visible ring at 3:1 or more against the neighbor surface. Never animate it in. Build it from outline, not border |
| pressed | A scale to 0.97 or a tone step. This is the most often missing state |
| disabled | Three channels together: reduced emphasis, no events, and native disabled semantics. Opacity alone is a faded enabled control |
| loading | Reserve the final width so the label swap does not reflow. Show feedback after about 300 ms |
| error | States cause and fix ("Password needs 8 or more characters"), never "Invalid" |
| success | Often silent. If the effect is already visible, do not celebrate it |

Empty is a view state, not a control state, so it is not on this list. Selected is a ninth where it applies (tab, chip, row). Show it with a tint and a mark.

## Geometry rules

- **Never change border width between states.** State goes to background, border color, outline or shadow. A width change shifts every neighbour.
- **Build the focus ring from outline.** Reserve a transparent outline at rest so focus causes no shift.
- **One base height across a form row.** A 38 px input beside a 44 px button is the usual tell. Pick one height. 44 pt (iOS) or 48 dp (Android) is the floor for touch.
- **Reserve the helper and error slot** (one line of space) even when empty so an error does not push the page.
- **A button label never wraps to two lines.** Make the control wider or shorten the label.
- **Pressed visuals do not move neighbours.** Use color, opacity or a transform on the control only.
- **Expand the hit area** when the visible icon is smaller than the target.

## Anatomy, variants and sizes

- Name the parts (container, label, icon, helper, slot).
- Variants are looks: primary, secondary, ghost, danger. Sizes are small, medium, large. Use named props (`variant`, `size`, `tone`), not ad hoc class lists.
- Only one filled primary per view. A destructive action is quieter until armed, and it names its outcome.
- Icons come from one family with one stroke weight. Filled and outline icons are not mixed at the same level.
- No emoji as icons.

## The inventory

| Group | Components |
|---|---|
| Primitives | Text, Icon, Button, Link, Divider, Surface |
| Forms | Input, Textarea, Select, Checkbox, Radio, Switch, Slider, Date picker, Search, One-time code, File drop |
| Feedback | Badge, Chip, Toast or snackbar, Banner, Progress, Spinner, Skeleton, Empty state, Error state |
| Overlays | Dialog, Sheet, Popover, Tooltip, Menu, Command bar |
| Navigation | Tabs, Nav bar, Side nav, Breadcrumb, Pagination, Stepper, App bar |
| Data display | List row, Table, Card, Avatar, Stat, Chart, Timeline, Accordion |
| Media | Image, Carousel, Player |
| Marketing blocks | Hero, Feature grid, Pricing, Testimonial, FAQ, Call to action |

Build in this order: primitives, forms, feedback, overlays, navigation, data, then blocks.

## Native equivalents

A component spec names what each platform draws. Do not reinvent these for flavor.

| Component | iOS | Android | Web | Desktop | TV | Car |
|---|---|---|---|---|---|---|
| Switch | Switch | Material switch | `input` switch role | OS switch | Focusable toggle | Large toggle |
| Picker | Wheel or inline calendar | Material picker | Native `select` or listbox | Popup menu | List overlay | Voice or short list |
| Confirm destructive | Action sheet | Dialog | Dialog | Dialog | Dialog with focus on Cancel | Avoid. Use voice |
| Menu | Context menu | Exposed dropdown or sheet | Menu button | Menu bar and context menu | Overlay list | Template list |
| Primary action | Filled button | Filled button, one FAB per screen | Button | Button | Focus card | Large button |
| Refresh | Pull to refresh | Pull to refresh | Button or pull | Button | Button | Not applicable |
| Icons | System symbols | Material symbols | One SVG set | OS icons | One set | Host icons |

## Packaging so it can be re-themed

- Components read **semantic variables** or roles (`primary`, `radius-md`, `dur-base`). Retheming replaces values, not components.
- One folder per component: the code, its states, an example, a short spec.
- Ship the theme as one file plus the `DESIGN.md`.
- Export tokens for the stack (CSS, Tailwind, Flutter, Compose, SwiftUI, React Native).
- Use the project's own conventions for compound components. Prefer composition to configuration (`Card.Header`, `Card.Body`).
- Use semantic variants in components, not raw colors.

## What to deliver

1. The component, matching the project's conventions, using tokens by name.
2. A preview that renders all states side by side (a throwaway page, a Storybook story, a Compose preview or a SwiftUI preview). Say it is throwaway.
3. `templates/component-spec.md` filled in.
4. `ux-acceptance.csv` rows for the states and the accessibility behavior.
