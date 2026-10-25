# Enhance a skill from upstream sources

Improve one existing skill by learning from other skills, repos, pages or docs. The target stays the owner. The sources are read, judged and rewritten. Nothing is copied, and nothing the target already does is removed.

This is not a merge (two skills become one), and not a document import (a book becomes a skill). Here one skill gets better.

Script: `scripts/enhance.mjs`. Template: [enhance-map.md](../../templates/enhance-map.md).

## Inputs

- One target skill folder (it holds `SKILL.md`).
- One or more sources: repo or page URLs, local skill folders, files.
- The user's constraints: what must not be removed, who owns each job, the license and credit policy of the result, the language, the vocabulary bar.

If a constraint is missing, ask once with your recommended answer. Policy questions come first: "Should the result carry any upstream name or license?"

```bash
node scripts/enhance.mjs <skill-dir> --source <url-or-dir> [--source ...] [--scratch <folder>] [--json]
```

The script is read-only. It prints the target's inventory, whether the scratch folder is ignored by git, and the exact commands to fetch each source. It never clones and never writes.

## Steps

### 1. Baseline the target

Read its `SKILL.md`, every reference, data file, template, script and test. Run its lint and its tests now, so you know what was already failing. Write down the parts that must stay (a template, a step order, a command name). Those are the "do not remove" list.

### 2. Make a private place for the sources

Choose a scratch folder that git ignores (for example `scratch/<topic>-sources/`). Confirm with `git check-ignore`, and add the folder to `.gitignore` first if needed. Fetch each source there, shallow (`git clone --depth 1`). For one file, download the raw file. Note the URL and the date next to each source in the map. Never fetch into the catalog.

### 3. Read every source to the end

Read the source's main file, then each reference it points to, until the list of headings is used up. A source that you skimmed gives a map you cannot trust. Note what it does well, what it lacks, and what it assumes (a server, a paid API, a taste).

### 4. Write the keep, drop and replace map

One table per source (see the template). For each method, choose one:

| Choice | When |
|---|---|
| **Keep** | The method serves the target's job. Write it in your own words and put it where it belongs |
| **Replace** | The source has a useful idea, but its form does not fit (needs a server, a paid API, a huge tree, a personal taste). Build a smaller version of your own that does the same job |
| **Drop** | Off the job, owned by another skill, a time-bound trend, or unsafe to ship. Give the reason |

Rules for the map:

- **A drop needs a real reason.** "Too big" or "too much" is not one. Size is a reason to replace, not to skip.
- **A gap the user asked for is never left empty.** If a source covers it and you will not copy, write your own version. Use a different structure, your own data and your own examples.
- **A feature that needs infrastructure becomes a static one.** A live editing mode that needs a dev server can become one page with knobs, as long as it keeps the same promise.
- **Facts are free, wording is not.** Public measurements and standards (a contrast ratio, an OKLCH formula) can stay. Sentences, tables and lists from the source cannot.

### 5. Check ownership

For each kept method, say which skill owns it. If a sibling skill owns it, put it there, or add a call to that skill. One method lives in one skill. Update the sibling's pointers so both skills agree. Do this before you write, not after.

### 6. Show the map and stop

Show the user the target inventory, the do-not-remove list and the map (per source, keep, replace and drop with reasons). Wait for approval or changes. If the user pushes back on a drop, turn it into a replace.

### 7. Write it as additions

- Add. Do not delete or rewrite what the target already does, except to fix a contradiction you found.
- Put depth in `references/`, `data/`, `templates/` and `scripts/`. Keep `SKILL.md` short, and link each new file once from it, one level deep.
- Update the description if the scope grew. It stays one quoted line under 1024 characters and says when to use the skill.
- Write in the target's language and vocabulary bar. For plain, simple English use `polyglot-copywriter`.
- Use your own structure, labels and examples. Do not mirror a source's headings or tables.
- Keep upstream names, license text and credit lines out of the shipped files if the policy says so. Source names live in the private map only.
- Prefer data a script can check (CSV, JSON) over long prose lists.

### 8. Make it testable

- Every new data file gets a validator (columns, ids, allowed values).
- Every new script gets tests, including a bad-input case.
- A test checks that each new reference is linked from `SKILL.md`, and that each command the docs name exists.
- Run the skill's lint and the repo's checks. Open and use anything you built (run the script, open the page). A test that passes is not proof that the output looks right.

### 9. Report

Give the user: what each source contributed (point to the private map), what was replaced and how, what was dropped and why, what you could not verify, and the checks that passed. Say where the private map and the clones are, and that they are not committed. Do not commit unless asked.

## When the sources fight

Two sources can give opposite advice. Do not average them. Pick the one that fits the target's job, say why in the map, and keep the other as a note in the private map only.

## Do not

- Copy a file, a table or a paragraph from a source.
- Add the upstream name, license or credit to the catalog when the policy says none.
- Remove what the target already does to make room.
- Leave a gap because a source was big. Write your own smaller version.
- Fetch into the catalog, or commit the scratch folder or the map.
- Let one method live in two skills.
- Skip a source because it was long. Read to the end or say you did not.
