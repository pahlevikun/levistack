---
description: "Cross-language code quality, review order and verification standards."
alwaysApply: true
---

# Code quality

- Preserve the repository's established architecture and conventions.
- Review in this order: security, correctness, performance, tests, maintainability.
- Bind database values, validate untrusted input, and never embed credentials.
- Prefer typed errors and explicit failure handling over string matching or silent catches.
- Avoid unbounded reads, accidental N+1 work, mutable shared state, and non-idempotent retry paths.
- Comment non-obvious constraints and trade-offs; do not narrate code that names can explain.
- Verify the narrow behavior first, then run the repository's normal type, test, lint and build gates in proportion to risk.
- Never claim completion when a relevant gate was skipped; report the exact missing prerequisite.
