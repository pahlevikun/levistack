# Scaffold files from the original package

The `elixir-expert` skill shipped with generated placeholder files. They contain no Elixir guidance and nothing in this skill uses them. They are kept so that nothing from the original package is lost.

| File | What it is |
|---|---|
| `commands/elixir-expert.md` | A one-line command stub that invoked the original skill |
| `hooks/pre-execute.cjs`, `hooks/post-execute.cjs` | Empty pre and post execution hooks from the packaging tool |
| `rules/elixir-expert.md` | A generic rules stub |
| `schemas/input.schema.json`, `schemas/output.schema.json` | Placeholder JSON schemas |
| `scripts/main.cjs` | A generated command-line stub |
| `templates/implementation-template.md` | A short goal, TDD and verification outline |

Safe to delete if you do not need an exact copy of the original package.
