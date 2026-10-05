# Skill format, structure and iteration

Verified on 2026-10-04 against https://agentskills.io/specification, https://code.claude.com/docs/en/skills and https://cursor.com/docs/skills.

## The format (Agent Skills spec)

```
skill-name/
├── SKILL.md          required: frontmatter + instructions
├── scripts/          optional: executable code
├── references/       optional: docs loaded on demand
└── assets/           optional: templates, data, images
```

| Field | Rule |
|---|---|
| `name` | Required. 1 to 64 chars, lowercase letters, digits, hyphens; no leading, trailing or doubled hyphen; **equals the folder name** |
| `description` | Required. 1 to 1024 chars. What it does and when to use it |
| `license`, `compatibility` (max 500), `metadata` (string map), `allowed-tools` (experimental) | Optional |

**Name conventions.** Prefer a verb phrase that says the job: `create-*` (authoring tools), `manage-*` (an external service), `setup-*` (configuration), `generate-*`, `build-*`, `review-*`. Avoid vague names (`helper`, `utils`, `tools`) and generic nouns (`documents`, `data`). Anthropic's skill authoring guidance reserves `anthropic` and `claude` in names, so keep them out of a skill name (as of the guidance reviewed 2026-10-05). Keep the folder, the `name` field and any wrapper command in agreement (`manage-stripe` in all three, not `stripe` in one).

**Description limits.** No XML tags in `name` or `description`. Third person only.

**Claude Code adds:** `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `disallowed-tools`, `model`, `effort`, `context: fork`, `agent`, `background`, `hooks`, `paths`, `shell`. The skill listing budget is about 1,536 characters for `description` plus `when_to_use`.
**Cursor adds:** `paths`, `disable-model-invocation`, `icon`, `color`.

## Where skills live

| Tool | Locations |
|---|---|
| Claude Code | `~/.claude/skills/`, `.claude/skills/` (and parent directories up to the repo root), nested `<subdir>/.claude/skills/`, plugin `skills/` |
| Cursor | `.agents/skills/`, `.cursor/skills/`, `~/.agents/skills/`, `~/.cursor/skills/`, plus `.claude/skills/` and `.codex/skills/` for compatibility |
| Anywhere | `npx skills add <owner>/<repo>` installs into the right place for each agent |

## Loading model

1. **Metadata** (name and description, about 100 tokens) is always loaded.
2. **The SKILL.md body** loads when the skill activates. Aim for under 5,000 tokens and 500 lines.
3. **Everything else** loads only when the body points to it.

Claude Code does not re-read the file on later turns, so write guidance for the whole task. After compaction only the first part of each skill is kept.

## The description

- State what it does, then `Use when ...` with the words a user would say ("write", "audit", "migrate", the file names, the error messages).
- Front-load keywords. Long descriptions are truncated when there are many skills.
- Write in the third person.
- Make it specific enough to separate it from its neighbors. "Helps with PDFs" fails; "Extracts text and tables from PDFs, fills forms, merges files. Use when the user mentions PDFs or forms" works.

## The body

- Instructions in the order the agent acts. Imperative mood.
- **Principles inside `SKILL.md`**, not in a file the agent may skip.
- **Default plus one escape hatch.** Recommend one approach and name the single alternative for an edge case. A menu of five options stalls the agent.
- **One term per concept.** Do not alternate "endpoint", "route" and "URL".
- **Match freedom to risk.** Fragile steps (migrations, deploys) get exact commands. Judgment calls (review, design) get principles and criteria.
- **Show, do not describe.** For output quality that depends on format, include one input and output pair, or a template to fill.
- **Checklists** for multi-step work, so progress can be resumed.
- **Verification steps and success criteria** so "done" is observable.

## Structure

- **Simple skill:** one task, one file, under about 150 lines.
- **Router skill:** an intake question ("What do you want to do?") and a table that sends each answer to one section or reference. Use it when there are three or more distinct tasks. Intent in the request ("audit this skill") should route directly without asking.
- **Folders by purpose:** `references/` for knowledge, `templates/` or `assets/` for output shapes, `scripts/` for deterministic code the agent runs rather than rewrites.
- **One level deep.** `SKILL.md` links to references; references do not link to more references.
- **Router with specialities.** A skill that merges several topics may add one more hop: `SKILL.md` (router) links to `specialities/<name>/GUIDE.md`, and a guide links to its own `references/`. Keep it to those two hops, put shared material in the skill's top-level `references/`, and never chain reference to reference. The linter allows this shape.
- **Scripts:** self-contained, clear errors, handle edge cases, no secrets. Prefer a script over asking the model to regenerate the same code each time.

## Invocation control

| Setting | Effect |
|---|---|
| default | The model may load it when relevant, and the user may type `/name` |
| `disable-model-invocation: true` | Only the user can run it. Use for side effects, deploys, commits, meta tools |
| `user-invocable: false` (Claude) | Only the model; background knowledge |
| `context: fork`, `agent: Explore` (Claude) | Runs in an isolated subagent; the instructions must stand alone |
| `allowed-tools` | Pre-approves tools for the skill's turn only |

Be careful with Claude's dynamic context injection (a backticked command prefixed with `!`): it runs before the model sees the skill and aborts the whole skill if the command fails. Keep it out of public skills, or guard it with `|| true`.

## Test and iterate

1. **Write the tests first.** Pick 3 to 5 real requests, including one that should *not* trigger the skill. Note what the agent does without the skill.
2. **Write the minimum** that fixes the observed gap.
3. **Run the requests** and watch: which files did it open, where did it hesitate, what did it do that you did not intend?
4. **Test on more than one model size.** Small models need explicit steps and examples; large models do well with principles. Aim for a skill that works on both.
5. **Fix by symptom:**

| Symptom | Fix |
|---|---|
| Never triggers | Rewrite the description with the user's words |
| Triggers on the wrong task | Narrow the description; add a "do not use for" clause |
| Ignores a step | Move it into `SKILL.md`, make it a numbered step, add a check |
| Too verbose output | Cut explanations; show an example instead |
| Misses edge cases | Add the failing case as an example |
| Context bloat | Move detail into `references/` and link it |

6. **Small, frequent edits.** One change per iteration, so cause and effect stay visible.

## Anti-patterns

- A vague or first-person description.
- A giant `SKILL.md` that holds reference material.
- Deeply nested reference chains.
- Windows-style paths.
- Unclosed or mixed structure that makes the body hard to scan.
- Instructions that only restate what the model already knows.
- Time-sensitive facts with no date.
- Several overlapping skills instead of one that routes.
