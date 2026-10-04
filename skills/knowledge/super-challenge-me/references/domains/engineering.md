# Domain: engineering

Load after the mode when the subject is a system, API, module shape, or architecture *decision* (not a current-state inventory).

## Artifacts

Design notes, RFC, module sketch, sequence the user described. Current facts come from `super-codebase-learner`. In-place deepening after diagnose uses **grill-docs**.

## Lenses

- What already exists (cite files; do not re-invent the tree)
- Seam: what must stay stable if internals move
- Failure, retry, idempotency, data ownership
- What is hard to reverse (store, public API, event contract)
- Tests that would survive the change
- Complexity you can cut and still prove the idea

## Do not

- Diagnose the whole repo here (learner **diagnose**).
- Pick a next framework or cloud (`super-tech-blueprint`).
- Execute the refactor (`super-refactor`).
