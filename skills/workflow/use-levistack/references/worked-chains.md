# Worked chains

Examples only, not the full map. `playbooks/invoke.md` picks the first skill, and `find-skills/references/routing.md` is the full catalog map.

| User says | Steps 3 to 7 |
|---|---|
| "How does auth work in this service?" | `codebase-learner` (explain) → (no proof step) → deliver as pilot-style answer |
| "Why do we retry this three times?" | `trace` (rationale) → deliver with confidence per claim |
| "Checkout broke last night, why?" | `trace` (root-cause, with `verify` for Why 1 if still failing) → deliver the chain, checks and fixes |
| "I'm new to this repo" | `codebase-learner` → deliver |
| "Plan the new export endpoint" | `codebase-learner` (current flow) → `execution-ready-spec-plan` → `write-plan` → deliver |
| "Add a filter to the list API" | `tdd` → `verify` → deliver with the test command and result |
| "Clean up this module, don't break it" | `safe-refactor` (with `tdd` if no tests) → `verify` → deliver |
| "Is my branch ready?" | `second-opinion` → fix Act on items with `tdd` → `verify` → deliver |
| "Ship this" | `verify` → `atomic-semantic-commit` → `write-mr-description` → gate before push and MR → deliver |
| "Make this app feel polished" | `product-polish-workflow` (it calls `design-system-kit` when needed) → `verify` on the real UI → deliver |
| "Grill my plan" | `challenge-me` → deliver |
| "Write a skill that does X" | step 4: `find-skills` (does one exist?) → `create-skill` → lint → deliver |
| "Too much to do, no idea where to start" | `get-moving` → deliver one next action |
| "Use levistack: second-opinion on src/payments" | one-shot: `second-opinion`, skip step 4 → deliver |
