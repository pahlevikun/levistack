# Merge skills

Compose two or more existing skills into one new skill. Sources stay until the user asks to delete them. This is not convert-from-files and not create-from-scratch.

Script: `scripts/merge.mjs`. Outline: [merge-outline.md](../../templates/merge-outline.md). Write the result with `create-skill` (router template when the jobs are distinct).

## Inputs

Two or more directories that each contain `SKILL.md`. Optional target name. Classify already returned `merge-skills`; if it did not, stop.

```bash
node scripts/merge.mjs <skill-dir...> [--name <name>] [--out <skills-dir>] [--json]
```

The script refuses anything that is not a skill directory. It prints names, descriptions, linked files, and a proposed folder name. It does not write or delete.

## Steps

1. Read each `SKILL.md` (name, description, body, linked `references/` `scripts/` `templates/`). Use the merge.mjs dump; open the files it lists.
2. Classify overlap: **same job** vs **distinct jobs**.
3. Fill [merge-outline.md](../../templates/merge-outline.md) and **stop for the user**:
   - proposed new `name` and `description` (`Use when ...`, trigger words from all sources; no "and" if it is really two jobs)
   - keep / drop / rewrite per source
   - shape: one `SKILL.md` if same job; **router** (`create-skill` `templates/skill-router.md`) if three or more distinct tasks
   - where it will be written; sources will not be deleted
4. After approval, write the new skill. Copy supporting files that are still referenced; do not copy dead references.
5. **Check nothing was lost.** List every principle, procedure, command and fact in the sources, then find each one in the merged skill: principles still inline in `SKILL.md`, procedures in a workflow or the body, facts in a reference. Anything dropped must be on the "Dropped from the merge" line of the outline, with a reason. Fix orphans before linting.
6. Lint, then run one real request per source skill against the merged one and compare behavior with the original. Do not overwrite an existing skill unless asked. Do not delete the source skills unless asked.

If the merged skill grows past about 200 lines or covers several intents, use the router shape. `create-skill` (`references/grow.md`) covers upgrading a simple skill to a router later.

## Same job vs distinct jobs

**Same job:** one procedure, combined steps, one description. Deduplicate. Prefer the clearer wording.

**Distinct jobs:** do not smash into one narrative. Make a router `SKILL.md` that dispatches to `references/<old-name>.md` (or keep specialities). If the honest name would need "and," say so in the outline and offer to keep them separate.

## Do not

- Rewrite source skills in place as the merge.
- Invent overlap that is not in the files.
- Merge a skill with a rule, PDF, or conversation in the same job.
- Run `convert.mjs` or `extract_document.py` on skill folders.
