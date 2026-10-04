# Domain: frontend

Components, styles, layout, client-side state, accessibility, and UI performance claims.

## Checklist

- [ ] Components match sibling structure — no over-abstracted wrapper trees for one screen (R-01, R-31).
- [ ] State lives at the lowest owner that needs it — no global store for local UI toggles without reason.
- [ ] a11y: focus, labels, and roles follow repo patterns — not bolt-on `aria-*` theater without behavior.
- [ ] No fabricated Lighthouse/Core Web Vitals numbers in copy or comments (R-17, R-36).
- [ ] Loading/error/empty states are real — not perpetual spinners or silent failure (R-27, C-2).
- [ ] Client fetches use timeouts and error surfaces consistent with the app's API layer (R-27).

## Scope note

Human-facing marketing prose in UI strings still passes API message rules (R-02). Long-form UX copy may also need **polyglot-copywriter** — super-noslop does not replace it.
