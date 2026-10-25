# Web apps and sites

For responsive sites and web apps in React, Next, Vue, Nuxt, Svelte or plain HTML, with Tailwind or any CSS. The user may have touch, a pointer, a keyboard or a screen reader, and the window can be any size.

## Principles

- **Semantic HTML first.** Real headings, links, buttons and labels. Use ARIA only to fill a gap.
- **Mobile first** at about 360 px, then widen at 480, 768, 1024, 1280 and 1536. Use fluid type and space (`clamp`).
- **Support zoom to 400 percent, text spacing changes, `prefers-color-scheme`, `prefers-reduced-motion`, `prefers-contrast` and forced colors.**
- **Targets** at least 24 px (WCAG 2.2) and about 44 px for touch.
- **Reading lines** of 45 to 75 characters.
- The URL is state. Back and forward work. Deep links land correctly.

## Mobile web floor

Six things that break a phone layout:

1. Use `overflow-x: clip` at the root and not `hidden`, because `hidden` breaks sticky positioning.
2. Image grid tracks use `minmax(0, 1fr)`, or images force sideways scroll.
3. Clickable text never wraps to two lines at any width.
4. Display headings get `overflow-wrap: anywhere` and `min-width: 0`.
5. Only one element sticks to the top.
6. All-caps display text needs a line height of at least 1.0.

Also: use `100svh` for a hero and `100dvh` for an app shell, never a bare `100vh`. Inputs are at least 16 px so iOS does not zoom. Hide desktop flourishes (hover marks, crop marks) below the breakpoint so they do not become touch targets. Add safe-area insets for notched phones.

## Component habits

- Hover styles sit behind a hover media query so they never stick on touch.
- Focus ring from `outline`, with an offset, never removed.
- Disabled uses the native attribute and not only a faded look.
- Forms: visible labels, errors tied to fields with an accessible description, a focusable error summary for several errors.
- Dialogs trap focus and return it on close. Sticky bars never hide the focused control.
- Skeletons keep layout. Images have dimensions so nothing jumps.

## Motion

CSS first. Animate transform and opacity. Use View Transitions for shared state change when supported. Gate movement behind the reduced-motion query. Keep content visible by default so a failed script does not hide the page.

## Stack notes

- **React:** small components, effects with cleanup, derived values not stored in state, virtualize long lists, manage focus.
- **Next:** Server Components by default and client components at the leaves, fetch on the server, `next/image` and `next/font`, validate Server Action input.
- **Vue:** script setup and the Composition API, typed props and emits, `v-for` keys.
- **Nuxt:** `useFetch` or `useAsyncData`, route rules for rendering, never read `window` during server render.
- **Svelte:** runes for state, keyed each blocks, built-in transitions with a reduced-motion path.
- **Tailwind:** map the theme variables with `@theme inline` and use role utilities. No per-color `dark:` variants.
- **shadcn style libraries:** use variants and compose with `className`. Do not fork a primitive for one color.

Details per stack are in `data/stack-notes.csv`.

## Verify

Open the real page at several widths. Keyboard only. Zoom to 400 percent. Reduced motion on. Dark mode. Run an automated accessibility check, then the manual pass. A screenshot does not prove keyboard or screen reader behavior.
