# Component spec: <Name>

Purpose: <one line>. Not for: <one line>.
Scope: <single element | pattern of several>. Register: <brand | product | h5>.

## Anatomy

<container, label, icon, helper text, slot names>

## Variants and sizes

| Variant | Use |
|---|---|
| primary | The one main action in a view |
| secondary | Supporting action |
| ghost | Low emphasis |
| danger | Destructive, with a confirm |

Sizes: small <h>, medium <h>, large <h>. One base height is shared across a form row.

## States

| State | Look | Notes |
|---|---|---|
| default | | |
| hover | | pointer only. Gated by a hover media query |
| focus-visible | ring of <n> px in `focus-ring`, 3:1 or more | never animated in, built from outline so geometry does not shift |
| pressed | scale `--press-scale` and the pressed role | |
| disabled | lower emphasis, no events, native disabled semantics | not opacity alone |
| loading | same width, spinner or skeleton, repeat taps blocked | |
| error | danger edge, icon and words | says cause and fix |
| selected | tint and a mark | not color alone |

Geometry rules: the border width never changes between states. Reserve space for helper and error text.

## Tokens

| Part | Role token |
|---|---|
| fill | `primary` |
| label | `on-primary` |
| radius | `radius-md` |
| height | `control-height` |

No raw values.

## Behavior

- Keyboard: <keys>
- Pointer and touch: <press, long press, drag alternative>
- Remote (TV): <focus order, scale, ring>
- Voice or host template (car): <if any>
- Motion: <token and purpose>, reduced motion result

## Accessibility

Role, name, state announcements, focus order, target size, contrast pairs to measure.

## Content

Label length and case, truncation rule, empty and long text.

## Platform notes

| Platform | Native control or pattern it maps to |
|---|---|
| iOS | |
| Android | |
| Web | |
| Desktop | |
| TV | |
| Car | |
