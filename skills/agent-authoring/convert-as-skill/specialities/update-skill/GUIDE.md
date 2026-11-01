# Update one skill

Revise a skill that already exists. The folder stays. The words are ours. A changelog, a diff, or a short note of what changed is the input. This is not a merge, and not a from-scratch write.

## Inputs

- One skill folder that contains `SKILL.md`.
- What changed: a changelog, a diff, or the user's note.
- What must stay: a step order, a command, or a name they will not give up.

If the folder is missing, ask once for its path. Recommend the skill they named.

## Steps

1. Read `SKILL.md` and the references it links. Note the job the description already claims.
2. Read the changelog or the diff. List only the changes that belong to this skill.
3. Show the edits you would make: description triggers, steps, and references. Wait for a yes before you write.
4. Write the revision in your own words. Do not copy a license, a copyright line, or a credit notice. Do not replace the folder.
5. Lint the skill. If the description grew past 1024 characters, cut it before you report done.

## Do not

- Delete the skill or rename the folder unless they ask.
- Treat a changelog as a new skill.
- Paste secret values, personal paths, or employer names from the changelog into the skill.

## Done when

- The same folder holds the revision.
- They saw the edit list before anything was written.
- Lint reports no errors.
