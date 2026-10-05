---
name: find-skills
description: "Gateway to every skill. Takes a vague or unknown task, asks only the questions it needs, picks the best chain of skills from the catalog, runs them, and installs from skills.sh only when the catalog does not fit. Use when the user does not know how to start, says 'help me with', 'where do I start', 'what should I use' or 'how do I do X', asks to find, pick or install a skill, or states a task that more than one skill could serve, such as modify a skill, write and review a doc, or ship a change."
---

# Find skills, then run them

Do not stop at a recommendation. Gather what is missing, map the job to skills, run them, and go upstream only for a real gap.

## Flow

1. **Gather context.** Skip every question the user already answered or the workspace can answer.
   - Read first: the cwd, `git status` and branch, any file, link or ticket the user named.
   - Missing after that? Ask at most three questions in one round, with a recommended answer for each. Use the host's question tool when it has one, otherwise plain text. Ask only what changes the routing:
     - **Outcome**: what exists when this is done?
     - **Target**: which repo, file, MR, ticket or doc?
     - **Stage and limits**: idea, plan, code, review or ship? Stack, deadline, anything not to touch?
   - Outcome and target both known? Do not ask. Go to step 2. Never run a second round of questions; state an assumption and go on.
   - Restate the job in one line: verb, object, target.
2. **Search the catalog.** Read [references/routing.md](references/routing.md) for the job-to-skill map, then confirm what is installed:
   ```bash
   node <this-skill-dir>/scripts/catalog.mjs <2-4 keywords> [--limit 8]
   ```
   Run it twice with different words (verb, then object or domain), and check the skill list the host already shows. It scans `./skills`, `./.cursor/skills`, `./.claude/skills`, `./.agents/skills`, `~/.claude/skills`, `~/.agents/skills`, and the catalog this skill ships in. A hit shows `loaded` or `file-only`; `--json` adds an `invoke` field. Score is a keyword count, so read descriptions before trusting the order. A skill in the map but not on disk is still ours: offer its install line from `routing.md`.
3. **Compose the chain.** Pick the fewest skills that cover the job, at most four. Give each a role: **Prepare** (gather facts, plan), **Do** (produce the result), **Verify** (`super-verify`, review, lint). Skip a role the job does not need. Prefer a skill that already names its next skill; its `Related skills` section lists the hand-offs. State the plan in one to four lines, `skill: why`. If every step is local and nothing is destructive or outward-facing, go on without asking.
4. **Run the chain.** Load each skill when its step starts, not all up front.
   - `loaded`: start it with the Skill tool by name.
   - `file-only`, or the hit says model invocation is disabled: read its `SKILL.md` and follow it, resolving relative links against that folder. If the user will reuse it, offer to install or link it so it becomes `loaded`.
   - No Skill tool in this host: treat every hit as `file-only`.

   Pass each result to the next step in a sentence. When a skill has a "Done when" list or names a next skill, follow that. If a step fails or does not fit, say so and re-plan. Do not skip silently.
5. **Check the user is happy.** After the first usable result, or when the user pushes back, ask if it is what they wanted. A "no", or a role with no good local skill, is a gap: go to [Upstream](#upstream).
6. **Report.** List the skills that ran, what each did, and what is left or was not done. If the user only asked to find or list skills, stop after step 2 and report.

## Upstream

Use when the catalog has no good match, the user is not satisfied with it, or the user asks for skills.sh.

1. **Search, top tier first.** Check the leaderboard at https://skills.sh/ for the domain, then run `npx skills find <query>` (`--owner <owner>` to narrow). Try alternate terms (`deploy`, `deployment`, `ci-cd`).
2. **Shortlist up to three.** Keep only skills that pass the checks. Rank by installs, then official owner.
   - Installs: prefer 1K or more. Be wary under 100.
   - Source: official owners (`vercel-labs`, `anthropics`, `microsoft`) over unknown authors.
   - Repo stars: under 100 is a warning sign.
3. **Ask which to install.** Present each option with its name, what it does, installs, source, the page `https://skills.sh/<owner>/<repo>/<skill>` and the install command. Always include "none, do it directly". Never install without an answer.
4. **Check before install.** Read the chosen skill's `SKILL.md` (its skills.sh page or the repo). A skill runs with your permissions.
5. **Install and continue.** `npx skills add <owner/repo@skill> -g -y` (`-g` user level, `-y` skip prompts). Then put it into the chain. A new skill may not show up in this session: if the Skill tool cannot find it, read the installed `SKILL.md` and follow it. `npx skills check` and `npx skills update` keep it current.

If nothing fits, say so and offer to do the task directly. If the task will repeat, offer to author a skill with `create-skill`.

## Editing a skill that is already installed

Find where it lives before changing it. A symlink in `~/.claude/skills` points at the source, so edit the source. A copy installed with `npx skills add` is overwritten by `npx skills update`, so change the upstream repo or fork it. In a catalog repo, follow that repo's own maintenance skill before touching generated files.

## Keep the catalog connected

After you add, rename or remove a catalog skill, run `node <this-skill-dir>/scripts/links.mjs`. It fails when a skill has no `## Related skills` section, names a skill that does not exist, or is missing from `routing.md`. It also lists one-way links and skills nothing points at. Fix the errors, add the new skill to `routing.md`, and link it from the skills it hands work to.

## Related skills

- `create-skill`: no skill fits and the task will repeat.
- `handoff`: the chain spans sessions.
