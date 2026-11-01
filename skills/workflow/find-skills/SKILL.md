---
name: find-skills
description: "Find, install and run skills in a fixed order: really search the levistack catalog (routing map plus scripts/catalog.mjs over the shipped catalog and this machine), browse skills.sh only when the catalog has no fit (skills.sh is the only external source allowed), install the pick on this machine with npx skills add -g, verify it landed, then invoke it. Step 4 (hunt) of use-levistack, on every use-levistack run. Use when the user asks to find, list, compare or install a skill, asks 'is there a skill for X', or when use-levistack is routing a task. Not the start point for a general task (use-levistack)."
metadata:
  version: 1.2.0
  author: levistack
  license: MIT
  group: workflow
  category: workflow
  department: workflow
  related_skills:
    - use-levistack
    - create-skill
    - help-levistack
  invokes:
    - skill: use-levistack
      when: User needs full catalog routing
  tags:
    - catalog
    - install
    - discover
  capabilities:
    - skill_discovery
    - playbook_chain_confirmation
  languages:
    - en

---

# Find skills, then run them

Step 4 (hunt) of `use-levistack`, on every run of that router. When called from there, prime already ran and deliver runs after you: skip your own report shape and hand the chain back. If step 3 already picked a skill, keep that pick. Search to confirm it and to add a missing companion (`handoff`, `rumbling`, `loopy`, `evidence`) when [the combination table](../../foundation/use-levistack/SKILL.md#workflow-combinations) matches. Do not replace a skill the user named.

Do not stop at a recommendation. Gather what is missing, map the job to skills, run them, and go upstream only for a real gap.

## Source order (never skip a tier)

1. **Levistack catalog.** [references/routing.md](references/routing.md) plus `scripts/catalog.mjs` over the catalog this skill ships in and the skills on this machine. A catalog hit always wins over an outside skill that does the same job.
2. **skills.sh, and nowhere else.** External browsing for skills happens only on https://skills.sh/ (leaderboard, domain and search pages, a skill's own page) and through `npx skills find`, which reads the same index. Do not browse GitHub repos, npm, blogs, docs, or any other registry to discover or judge a skill, and do not follow a skills.sh page's repo link to evaluate it: judge from the skills.sh page, its SKILL.md preview, install count and owner. If the preview is missing or truncated, say the check is incomplete instead of going to the repo.
3. **This machine, then invoke.** An outside pick is not done when it is found: after the user's yes, install it user-level on this machine, prove it landed, and invoke it in this session (step 5 of [Upstream](#upstream)). The `npx skills add` fetch of the source repo is the install, not browsing.

## Flow

1. **Gather context.** Skip every question the user already answered or the workspace can answer.
   - Read first: the cwd, `git status` and branch, any file, link or ticket the user named.
   - Missing after that? Ask at most three questions in one round, with a recommended answer for each. Use the host's question tool when it has one, otherwise plain text. Ask only what changes the routing:
     - **Outcome**: what exists when this is done?
     - **Target**: which repo, file, MR, ticket or doc?
     - **Stage and limits**: idea, plan, code, review or ship? Stack, deadline, anything not to touch?
   - Outcome and target both known? Do not ask. Go to step 2. Never run a second round of questions; state an assumption and go on.
   - Restate the job in one line: verb, object, target.
2. **Search the levistack catalog, really search it.** All three passes, every time; a host skill list alone is not a catalog search.
   - Read [references/routing.md](references/routing.md), the job-to-skill map of every catalog skill. It is the catalog of record even when the files are not on this machine.
   - Run the search script twice with different words (verb, then object or domain):
     ```bash
     node <this-skill-dir>/scripts/catalog.mjs <2-4 keywords> [--limit 8]
     ```
     It scans `./skills`, `./.cursor/skills`, `./.claude/skills`, `./.agents/skills`, `~/.claude/skills`, `~/.agents/skills`, and the catalog this skill ships in, so a clone or plugin install finds its sibling skills whatever the cwd is. A hit shows `loaded` or `file-only`; `--json` adds an `invoke` field.
   - Both passes empty? Run it once with no query and scan the full list of names and descriptions before saying the catalog has no fit. Score is a keyword count, so read descriptions before trusting the order.
   - Cross-check the hits against the skill list the host already shows.
   - A skill in the map but not on disk is still ours and still beats anything outside: install it on this machine with `npx skills add pahlevikun/levistack@<skill> -g -y` after a yes, verify and invoke it exactly like an outside install ([Upstream](#upstream) steps 4-6). A `file-only` hit in a cloned catalog needs no install to run now (step 4); offer the install only when the user wants it available outside this repo.
3. **Compose the chain.** Pick the fewest skills that cover the job, at most four. Give each a role: **Prepare** (gather facts, plan), **Do** (produce the result), **Verify** (`verify`, review, lint). Skip a role the job does not need. Prefer a skill that already names its next skill; its `Related skills` section lists the hand-offs. State the plan in one to four lines, `skill: why`. If every step is local and nothing is destructive or outward-facing, go on without asking. When `use-levistack` matched a situational playbook, its table is the chain: confirm each skill exists and add only a companion the playbook lacks. A question about how to use the catalog, with no task, goes to `help-levistack`.
4. **Run the chain.** Load each skill when its step starts, not all up front.
   - `loaded`: start it with the Skill tool by name.
   - `file-only`, or the hit says model invocation is disabled: read its `SKILL.md` and follow it, resolving relative links against that folder. If the user will reuse it, offer to install or link it so it becomes `loaded`.
   - No Skill tool in this host: treat every hit as `file-only`.

   Pass each result to the next step in a sentence. When a skill has a "Done when" list or names a next skill, follow that. If a step fails or does not fit, say so and re-plan. Do not skip silently.
5. **Check the user is happy.** After the first usable result, or when the user pushes back, ask if it is what they wanted. A "no", or a role with no good local skill, is a gap: go to [Upstream](#upstream).
6. **Report.** List the skills that ran, what each did, and what is left or was not done. If the user only asked to find or list skills, stop after step 2 and report.

## Upstream: skills.sh only, then install and invoke

Use when the catalog search (all three passes) has no good match, the user is not satisfied with it, or the user asks for skills.sh. skills.sh is the only external source: browse nothing else (see [Source order](#source-order-never-skip-a-tier)).

1. **Browse skills.sh.** Start at the leaderboard at https://skills.sh/ for the domain, follow its domain and search pages, and run `npx skills find <query>` (`--owner <owner>` to narrow) against the same index. Try alternate terms (`deploy`, `deployment`, `ci-cd`).
2. **Shortlist up to three.** Keep only skills that pass the checks, judged from their skills.sh pages alone. Rank by installs, then official owner.
   - Installs: prefer 1K or more. Be wary under 100.
   - Source: official owners (`vercel-labs`, `anthropics`, `microsoft`) over unknown authors.
   - Repo stars, when the page shows them: under 100 is a warning sign.
3. **Ask which to install.** Present each option with its name, what it does, installs, source, the page `https://skills.sh/<owner>/<repo>/<skill>` and the install command. Always include "none, do it directly". Never install without an answer. The `-y` in the install command only skips the CLI's own prompts; it never replaces this yes.
4. **Check before install.** Read the chosen skill's full `SKILL.md` preview on its skills.sh page. A skill runs with your permissions. No preview, or a truncated one? Say the check is incomplete and let the user choose: proceed anyway, or skip it. Do not open the repo to complete the check.
5. **Install on this machine.** Run:
   ```bash
   npx skills add <owner/repo@skill> -g -y
   ```
   `-g` installs user-level on this machine, so the skill is available in every project. Do not install project-level, and do not retry a failed install with different flags, `sudo`, or `--copy` without asking.
6. **Verify, then invoke it.** Prove the install landed, then run the skill in this session; "installed" is not the deliverable.
   ```bash
   npx skills list -g --json          # the skill is listed
   node <this-skill-dir>/scripts/catalog.mjs <skill-name> --json   # its path and invoke mode
   ```
   Then put it into the chain (step 4 of the flow): start it with the Skill tool when it shows `loaded`. A skill installed mid-session usually does not register until the next session, so when the Skill tool cannot find it, read the installed `SKILL.md` at the path `catalog.mjs` reports and follow it now; say it will be `loaded` next session. `npx skills update` keeps installed skills current.

If nothing fits, say so and offer to do the task directly. If the task will repeat, offer to author a skill with `create-skill`.

## Editing a skill that is already installed

Find where it lives before changing it. A symlink in `~/.claude/skills` points at the source, so edit the source. A copy installed with `npx skills add` is overwritten by `npx skills update`, so change the upstream repo or fork it. In a catalog repo, follow that repo's own maintenance skill before touching generated files.

## Keep the catalog connected

After you add, rename or remove a catalog skill, run `node <this-skill-dir>/scripts/links.mjs`. It fails when a skill has no `## Related skills` section, names a skill that does not exist, or is missing from `routing.md`. It also lists one-way links and skills nothing points at. Fix the errors, add the new skill to `routing.md`, and link it from the skills it hands work to.

## Related skills

- `use-levistack`: the router that calls this skill at step 4.
- `create-skill`: no skill fits and the task will repeat.
- `help-levistack`: the user asks how to use the catalog, not for a task.
- `handoff`: the chain spans sessions.
