# Domain: docs-only exclusions

When the change is **only** markdown/docs with no handlers, migrations, config keys, or executable tests in scope:

- Do **not** run the full delivery gate on code surfaces.
- Use **polyglot-copywriter** (and `noslop-prose` / `noslop-doctrine` for long-form) for human prose.
- Use **write-mr-description** + super-noslop **after** mode when the artifact is an MR description template output.

If the docs change embeds API examples or config snippets, load **api** or **infra-config** for those fenced blocks only.
