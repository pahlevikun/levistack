---
name: convert-as-skill
description: "Convert existing material into a skill, or merge existing skills into one. Use when asked to convert a rule, command or agent to a skill, save a conversation as a skill, turn a PDF or docs folder into a skill, or merge two skills into one. Not for writing a skill from scratch (`create-skill`)."
---

# Convert as skill

One skill, five use cases. A classifier picks exactly one, or asks. Load only that use case's GUIDE. Copy, extract, distill and compose are different jobs.

For a new skill with no source file use `create-skill`. For a new rule, command or agent use `create-rule`, `create-command` or `create-agent`.

## Principles

1. **Classify first.** Run `scripts/classify.mjs` before opening a GUIDE. File layout beats wording. Never default to conversation.
2. **One use case per input.** A PDF is never copied as a rule. Mixed kinds are sequential jobs, or `ask` — not one blended skill.
3. **Copy vs extract vs distill vs compose.** Rules and agents copy the body. A conversation extracts what worked. A document distills structure. Merge composes a new skill and leaves the sources.
4. **Preview, then write. Never delete on your own.** Dry-run first. Remove originals only after the user has reviewed the result and asked.
5. **Third-party books stay private.** Do not commit a generated book skill to this catalog.

## Step 0 — classify

```bash
node scripts/classify.mjs [--text "<user request>"] [--json] [path...]
```

| Status | Do |
|---|---|
| `ok` | State the kind and reason. Load **only** that GUIDE. |
| `ask` | Ask the printed question. Load no GUIDE. |
| `reject` | Stop. Use the named create-* skill instead. |

`from-command` uses the from-rule GUIDE; the kind stays distinct in logs.

## Use cases

| Kind | Source | What happens | GUIDE |
|---|---|---|---|
| `from-rule` / `from-command` | `.mdc`, `rules/`, `commands/` | **Copy** the body | [from-rule](specialities/from-rule/GUIDE.md) |
| `from-agent` | `agents/*.md` | Keep / wrap / convert, then **copy** | [from-agent](specialities/from-agent/GUIDE.md) |
| `from-conversation` | Chat / transcript, no files | **Extract** what worked | [from-conversation](specialities/from-conversation/GUIDE.md) |
| `from-document` | PDF, docs folder, HTML, URL | **Distill** structure | [from-document](specialities/from-document/GUIDE.md) |
| `merge-skills` | Two or more skill folders | **Compose** one new skill | [merge-skills](specialities/merge-skills/GUIDE.md) |

Scripts: `scripts/classify.mjs`, `scripts/convert.mjs` (rules/agents only), `scripts/extract_document.py`, `scripts/merge.mjs`. Document parsers live in `scripts/extractor/` (`pdf.py`, `html.py`, `docx.py`, `epub.py`, `text.py`, `rtf.py`, `sanitize.py`, `dependencies.py`, `config.py`, `exceptions.py`, `scan_generated_skill.py`). Templates: [harvest.md](templates/harvest.md), [merge-outline.md](templates/merge-outline.md).

## Do not

- Open a GUIDE before classify, or load two GUIDEs for one input.
- Treat "verbatim" as a use case. It is only how from-rule / from-agent copy the body.
- Default "convert this" with no files to a conversation.
- Run `convert.mjs` on a PDF or a skill folder, or `extract_document.py` on `rules/` / `commands/` / `agents/`.
- Delete sources, or commit a third-party book dump to this catalog.

## Related skills

- `create-skill`: write a new skill, or fix one.
- `create-rule`: keep a rule as a rule.
- `create-command`: keep a command as a command.
- `create-agent`: keep a subagent as a subagent.

## Done when

- Classify printed one kind (or asked / redirected) and only that GUIDE ran.
- The new skill lints clean. Skipped or refused inputs have a stated reason.
- The user knows which originals remain and how to remove or restore them.
