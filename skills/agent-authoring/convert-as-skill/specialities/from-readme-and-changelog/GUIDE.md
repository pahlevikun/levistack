# From a README and a changelog

Turn a project README and a changelog into a skill, or revise a skill that already exists using those two files. Distill what the project is, how to install it, how to run it, and what changed. Do not paste the files into `SKILL.md`.

## Preconditions

Classify already returned `from-readme-and-changelog`. If it did not, stop.

The inputs are `README.md` and `CHANGELOG.md` in the project, or the paths the user named. When they name one skill folder as well, revise that skill. The folder stays.

## Steps

1. Read the README and the changelog. Note the commands, the versions, and the sections that are procedures.
2. If a skill folder was named, read its `SKILL.md` and list only the changes that belong to that skill.
3. Show an outline before you write:
   - proposed `name` and `description` (`Use when ...`) when this is a new skill
   - which README sections become steps, and which changelog entries become a short "what changed" note
   - what you will drop (marketing lines, license text, credit lines, long examples)
4. Wait for a yes. Then write in your own words. Do not copy a license, a copyright line, or a credit notice.
5. A new skill goes through `create-skill`. A revision stays in the same folder.
6. Lint the skill.

## Do not

- Treat the README as the whole skill body.
- Invent commands or versions that are not in the files.
- Put secret values from the changelog into the skill.

## Done when

- The outline was shown before anything was written.
- License text and credit lines were left out.
- Lint reports no errors.
