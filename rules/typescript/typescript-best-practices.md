---
description: "Keep TypeScript states valid and parse external values before trusting their types."
globs: "**/*.ts,**/*.tsx"
alwaysApply: false
---

# TypeScript types

- Give each variant a literal tag and its own fields. Use a discriminated union when fields depend on the state.
- Choose shapes that enforce the needed rule. Use a tuple for a fixed pair. Require a nonempty array only where an empty array would make an operation unsafe.
- Give distinct meanings distinct types. Create branded values through a parser or a guard that checks the full claim. Never manufacture a brand with `as`.
- Accept external values as `unknown`. Parse them at entry points with the project's schema library and derive types from that schema. Write a custom guard only when a schema does not fit. Avoid `any`.
- Narrow with a tag switch first, then `in`, then `typeof` or `instanceof`, then a guard whose checks prove its claim.
- Check each union case. Assign the remaining value to `never` in the fallback so a new variant causes a compile error.
- Use `satisfies` to check a value's shape while keeping its inferred type. Do not use assertions to hide missing validation or type errors. Any necessary assertion must have a clear proof.
- Derive types from the source that owns the shape. Reuse schema output and standard type helpers before declaring a second interface.
