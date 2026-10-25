# Inline docs (the "why" that lives next to the code)

The cheapest source, and often the most exact. Read it before you spawn anything else.

## What this source holds

- Code comments, docstrings, and doc comments (`///`, `@doc`, JSDoc, Javadoc)
- `TODO`, `FIXME`, `HACK`, `XXX`, `NOTE`, and "do not remove" warnings
- README files in the repo and in sub-folders
- `CHANGELOG`, release notes, `UPGRADING` or migration guides
- ADRs in the repo (`docs/adr/`, `docs/decisions/`, `adr/`)
- API contracts with descriptions: OpenAPI, `.proto` comments, GraphQL schema docs, event schemas
- Config comments (YAML, env templates, Terraform variables)
- Test names and test comments, which name the edge case a change was for
- `CONTEXT.md`, `AGENTS.md`, `CLAUDE.md`, and rule files
- Runbooks and playbooks kept in the repo

## How to search it

```bash
# Comments and markers near the target
rg -n -C3 '(TODO|FIXME|HACK|XXX|NOTE|WARNING|do not remove|keep this)' <target_file>

# ADRs and decision records
rg -l -i 'status:\s*(accepted|superseded)|architecture decision|## Decision' --glob '*.md'

# The changelog entry for a symbol or feature
rg -n -i '<feature or symbol>' CHANGELOG* docs/ --glob '*.md'

# Tests that name the edge case
rg -n '<symbol>' --glob '*{test,spec}*'

# Contract descriptions
rg -n -B2 -A4 '<field or endpoint>' --glob '*.{yaml,yml,json,proto,graphql}'
```

## What good evidence looks like

- A comment that gives the reason: `// clamp to 100: the partner API rejects larger pages`
- A test named after a bug: `test "does not double charge when the webhook retries"`
- An ADR with status Accepted and the option it rejected
- A changelog entry that ties a change to a version and a reason

## Pitfalls

- **Stale comments.** A comment can describe code that changed since. Check the comment's blame date against the code's.
- **Code is not its own reason.** A comment that only restates what the code does is not a "why".
- **Generated docs** (API docs built from code) repeat the code. Prefer hand-written text.

## What to return

File and line, the quoted text, its blame commit and date, and whether it still matches the code.
