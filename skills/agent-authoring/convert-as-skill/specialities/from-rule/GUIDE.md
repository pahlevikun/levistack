# From a rule or command

Copy a rule or slash command into a skill. The body is copied as-is; only frontmatter is rewritten. Do not harvest a conversation or distill a document on this path.

Mapping detail: [mapping.md](mapping.md). Script: `scripts/convert.mjs`.

## Does it convert?

| Source | Converts? | Result |
|---|---|---|
| Rule with `description`, no globs, not always-on | Yes | `name` + `description`, body copied |
| Rule with `globs` or `paths` | Only with `--paths` | Scope kept as `paths`; behavior changes |
| Rule with `alwaysApply: true`, or no frontmatter | No | Stays a rule |
| Command, with or without frontmatter | Yes | `name`, `description`, `disable-model-invocation: true`, other keys kept |

Always-on rules stay rules. File-scoped rules need `--paths` and a warning that a skill is chosen by description, not by the open file. Commands keep `disable-model-invocation: true`.

## Steps

1. **Find the sources** using the locations in [mapping.md](mapping.md). Skip anything in a tool's built-in folder (for example Cursor's `skills-cursor`).
2. **Choose the destination:** the project's skills folder (`.claude/skills/`, `.cursor/skills/` or `.agents/skills/`), the user's, or a catalog's `skills/<group>/`. Match what the project already uses. In a catalog repo follow its maintenance instructions and add the group's `DESCRIPTION.md` if the group is new.
3. **Preview:**

   ```bash
   node scripts/convert.mjs <source...> --out <skills-dir> --dry-run
   ```

   `--kind rule|command` is inferred from the path (`rules/`, `commands/`); pass it for a file elsewhere. `--name` and `--description` apply to one source. The script refuses PDFs and skill folders.
4. **Write the descriptions.** For each warning about an inferred description, rewrite it as what the skill does plus `Use when ...` with the words a user would say, then re-run with `--description "..."` for that file.
5. **Convert:** run again without `--dry-run`. It refuses to overwrite an existing skill unless you pass `--force`.
6. **Verify:** diff each body against its source (the text after the frontmatter must be identical). Lint with the `create-skill` linter (`<create-agent>/scripts/lint.mjs <skill-dir>`). In a catalog repo run its sync and validate commands.
7. **Try it:** run `/name` for a command, or ask for something the description should match. Confirm it loads.
8. **Originals:** report the source paths and what replaced them. Delete them only when the user asks; offer to restore from version control if the conversion is rejected.

## Do not

- Rewrite the body. Improvements are a later, reviewed change.
- Convert an always-on or file-scoped rule unless the user wants on-demand loading.
- Write into a tool's built-in skills folder.
- Run harvest or `extract_document.py` on these files.
