# DRY: principle and refactoring workflow

Rules for removing duplication: the principle, the iron laws, the anti-patterns, and a refactoring workflow that uses `jscpd`.

## Instructions

When reviewing or writing code, apply these guidelines:

- Follow the DRY (Don't Repeat Yourself) Principle and Avoid Duplicating Code or Logic.
- Avoid writing the same code more than once. Instead, reuse your code using functions, classes, modules, libraries, or other abstractions.
- Modify code in one place if you need to change or update it.

## Iron Laws

1. **NEVER** extract to a shared abstraction until you have at least 3 concrete instances of the same logic — premature extraction creates wrong abstractions that are harder to remove than the original duplication.
2. **ALWAYS** maintain a single source of truth for configuration values — the same constant or config value defined in two places will diverge and cause bugs.
3. **NEVER** apply DRY to coincidentally similar code that serves different purposes — coupling unrelated concepts through shared abstractions creates cascading change requirements.
4. **ALWAYS** prefer readability over DRY when the abstraction requires indirection that obscures what the code does — a small amount of duplication is often better than an obscure helper.
5. **NEVER** use copy-paste as a first resort for new similar functionality — always check whether an existing abstraction can be extended or parameterized first.

## Anti-Patterns

| Anti-Pattern                                            | Why It Fails                                                                             | Correct Approach                                                                |
| ------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Extracting on the second occurrence (Rule of Two)       | Two instances may be coincidentally similar; wrong abstraction is worse than duplication | Wait for the third occurrence before extracting; use the Rule of Three          |
| Coupling unrelated concepts through shared helpers      | Changes to one domain break the other; creates unexpected dependencies                   | Only extract when the shared logic genuinely represents the same domain concept |
| Over-abstracting to eliminate all apparent duplication  | Creates complex indirection that requires reading 3 files to understand 1 operation      | Prefer 3 readable duplicate lines over 1 inscrutable abstraction                |
| Same constant defined in multiple configuration files   | Values diverge silently; one-off changes cause hard-to-trace bugs                        | Single config module or environment variable; import everywhere                 |
| DRY applied to test code (reducing fixture duplication) | Test setup that's too DRY becomes hard to read in isolation                              | Tests should be self-contained; some duplication in test setup is acceptable    |

## Refactoring workflow (jscpd)

Guided workflow to eliminate copy-paste duplication in source code. Use after running `jscpd` to detect clones.

### Prerequisites

First, run jscpd to identify duplications:

```bash
npx jscpd --reporters ai <path>
```

See the jscpd project for the full option reference.

### Workflow

1. Run jscpd with `--reporters ai` on the target path
2. Parse each clone line to identify the two duplicated locations (file + line range)
3. Read both code fragments from the source files
4. Understand what the duplicated code does
5. Design a refactoring: extract a shared function, class, module, or constant
6. Apply the refactoring — update both locations and all other usages
7. Re-run jscpd to confirm the clone is eliminated
8. Repeat for remaining clones, highest-impact first

### Refactoring Strategies

**Extract function** — when the duplicate is a block of logic:
```ts
// Before: same block in two places
// After: shared function called from both places
```

**Extract module/utility** — when the duplicate spans multiple files in different domains:
```ts
// Move shared logic to a shared utility file and import it
```

**Extract constant or config** — when the duplicate is repeated data or configuration.

**Template/base class** — when the duplicate is structural (e.g., repeated class shape).

Always ensure:
- All call sites are updated, not just the two reported by jscpd
- Tests still pass after refactoring
- The extracted abstraction has a clear, descriptive name

### Tips

- Start with clones that have the highest line count — they have the most impact
- A clone between test files may indicate a missing test helper
- Clones across unrelated modules may signal a missing shared utility
- Use `--min-lines 10` to filter noise and focus on meaningful duplications
