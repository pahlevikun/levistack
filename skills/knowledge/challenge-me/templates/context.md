# CONTEXT.md (lazy snippet)

Create only when a term has been resolved and the repo has no `CONTEXT.md` yet. Domain language only — no implementation details.

```markdown
# Domain context

Terms meaningful to domain experts. Update when a grilling session resolves a name.

## Glossary

| Term | Means | Does not mean |
|---|---|---|
| <Term> | <one line> | <nearby confusion> |

## Notes

- <relationship or invariant in domain language>
```

Monorepo: if `CONTEXT-MAP.md` exists at the root, put this file in the bounded context it names, not at the repo root.
