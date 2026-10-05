# Decide, grow and split skills

## Contents
- Is a skill the right tool?
- Map the jobs before choosing a shape
- Add a component to an existing skill
- Upgrade a simple skill to a router
- Domain-expertise skills

## Is a skill the right tool?

Ask these before writing anything.

| Make a skill when | Do not when |
|---|---|
| The task repeats across sessions | It is a one-off: just do it |
| The knowledge changes slowly | It changes weekly and will be stale (link to the source instead) |
| It is complex enough that structure saves time | It is one sentence: that is a rule |
| The model gets it wrong without help | The model already does it correctly |
| It should load only when relevant | It must apply to every task (rule) or must be enforced (hook) |
| | It is a prompt you type and nothing else (command) |

Assess aloud, briefly, and give the user the recommendation: simple skill, router, command, rule, or nothing.

## Map the jobs before choosing a shape

1. List what a user might want from it: create / edit / debug, build / test / ship, setup / use / troubleshoot, import / process / export. Each distinct intent is a candidate workflow.
2. List the knowledge needed whichever intent they pick. That becomes `references/`.
3. List the rules that must hold for every intent ("verify before reporting success", "never store credentials in code", "ask before a destructive change"). Those stay inline in `SKILL.md`, because the body is the only part that is always read.

| Result | Shape |
|---|---|
| One intent, little shared knowledge | Simple skill, one file |
| Two or more intents, shared knowledge | Router `SKILL.md` plus a file per intent plus shared references |
| Many intents in one domain | Router, specialities per intent, shared references |

A workflow file holds the procedure to follow. A reference holds knowledge to read. Do not mix them: "how to do X" next to "what X means" confuses both.

## Add a component to an existing skill

Read the skill first and report its current structure. Then:

| Adding | Do | Then update |
|---|---|---|
| **A workflow** (a new intent) | Write `references/<intent>.md` or `specialities/<intent>/GUIDE.md` with what to read, the steps, and a done condition. A simple skill with no router must be upgraded first (below) | The intake table and routing rows in `SKILL.md` |
| **A reference** (shared knowledge) | Write `references/<topic>.md` with a contents list if it is over 100 lines. If only one workflow needs it, put it inside that workflow | The link in `SKILL.md`; the workflows that must read it |
| **A template** (an output shape) | Put it in `templates/`, with placeholders and inline guidance | The step that says when to copy it |
| **A script** (deterministic work) | Confirm it is repeated, fragile or must be consistent, then follow `references/scripts.md`. Make it executable | The step that runs it, and the verify step after |

After each change run the lint and trigger one request that should reach the new part. Every file must be linked from somewhere, and the files must stay one level from `SKILL.md`.

## Upgrade a simple skill to a router

Upgrade when the body passes about 200 lines, covers several intents, or has rules that keep being skipped. Do not upgrade a short single-job skill.

1. Read the skill. Mark each part as **principle** (applies to every use), **procedure** (one intent), or **knowledge** (facts, patterns, examples).
2. Show the user the split and wait for a yes: principles that stay, workflows to extract, references to extract.
3. Create the folders. Move each procedure to its own file, each block of knowledge to a reference, with a contents list on long ones.
4. Rewrite `SKILL.md` from `templates/skill-router.md`: principles inline, a "What do you want to do?" table, shared tools, done-when. Keep the original `name` and `description`.
5. Check nothing was lost: every principle is still inline, every procedure sits in a workflow, every fact sits in a reference, and no paragraph is orphaned. Diff the old body against the new files if in doubt.
6. Lint, then run one request per route and compare behavior with the original skill.

## Domain-expertise skills

Some skills must hold a whole practice, not one task: build, debug, test, optimize and ship in a domain. Build one only when the domain is stable enough to document and the user will return to it.

**Shape.** A router `SKILL.md` with the principles that always apply and a short "what do you want to do" table; a workflow per lifecycle stage (build new, add a feature, debug, write tests, optimize, ship); `references/` organized by the concerns of the domain, not by document type.

**Research before writing.** Do not write from memory. For each library, tool or pattern:
- check when it was last released and whether it is maintained (no commits for a year is a red flag);
- check what replaced it, and what is deprecated;
- prefer official documentation over tutorials, and cross-check a critical claim against a second source;
- note the date you checked.

**Each reference** states its options with when to use each, a decision rule ("if X use A, if Y use B"), the working patterns, the anti-patterns with the correction, and platform differences. Say when not to use something.

**Each workflow** begins with what to read, contains real steps that do work (not "read the references"), ends with a verification command, and lists the mistakes to avoid.

**Load selectively.** The body plus the references for the current stage should fit comfortably; a skill that makes the agent read everything defeats progressive disclosure. If a planning skill consumes the domain skill, give the body a short index that maps each kind of work to the references it needs.

**Completeness test.** Could a competent newcomer take a project from nothing to shipped using only this skill? If not, list the missing stage. Run it both ways: invoked directly for a task, and read as knowledge by another skill.

Do not copy tutorial text without checking it, stop at "getting started", or leave out the "when not to use" guidance.
