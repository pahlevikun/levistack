# Worked chains

Examples only, not the full map. `playbooks/invoke.md` picks the first skill, and `find-skills/references/routing.md` is the full catalog map.

| User says | Steps 3 to 7 |
|---|---|
| "How does auth work in this service?" | `codebase-learner` (explain) → (no proof step) → deliver as pilot-style answer |
| "Why do we retry this three times?" | `trace` (rationale) → deliver with confidence per claim |
| "Checkout broke last night, why?" | `trace` (root-cause, with `verify` for Why 1 if still failing) → deliver the chain, checks and fixes |
| "I'm new to this repo" | `codebase-learner` → deliver |
| "Plan the new export endpoint" | `codebase-learner` (current flow) → `ready-spec` → `write-plan` → deliver |
| "Add a filter to the list API" | `tdd` → `verify` → deliver with the test command and result |
| "Clean up this module, don't break it" | `safe-refactor` (with `tdd` if no tests) → `verify` → deliver |
| "Is my branch ready?" | `second-opinion` → fix Act on items with `tdd` → `verify` → deliver |
| "Ship this" | `verify` → `atomic-semantic-commit` → `write-mr-description` → gate before push and MR → deliver |
| "Make this app feel polished" | `product-polish-workflow` (it calls `color-kit`, `ui-ux-kit` and `design-system-kit` for their parts) → `verify` on the real UI → deliver |
| "Design a calm meditation app for phone and TV" | `design-system-kit` (it calls `color-kit` for colors and `ui-ux-kit` for screens) → `prototype-wireframe` for any open question → `verify` → deliver |
| "Give me a palette and dark mode for this app" | `color-kit` → hand tokens to `design-system-kit` if a whole system is wanted → `verify` |
| "Build the checkout screen for iOS and Android" | `ui-ux-kit` (calls `color-kit` only if a new palette is needed) → `tdd` for behavior → `verify` on a device |
| "Grill my plan" | `challenge-me` → deliver |
| "Teach me how X works" | `codebase-learner` (explain) and `trace` (rationale) in parallel → blend into one plain account → deliver |
| "Catch me up, I was away" | `handoff` (catch up) → deliver the headline, what changed and what needs the user |
| "Is this refactor safe?" | `verify` (prove it is safe) → `second-opinion` if the change is wide → deliver |
| "Our benchmark says 2x faster" | `verify` (vet a number) → deliver the verdict word first |
| "Write a skill that does X" | step 4: `find-skills` (does one exist?) → `create-skill` → lint → deliver |
| "Too much to do, no idea where to start" | `get-moving` → deliver one next action |
| "Use levistack: second-opinion on src/payments" | one-shot: `second-opinion`, skip step 4 → deliver |
