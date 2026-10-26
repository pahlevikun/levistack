---
name: convert-as-skill
description: "Convert existing material into a skill, merge existing skills into one, or enhance one skill by learning from upstream skills, repos and pages. Use when asked to convert a rule, command or agent to a skill, save a conversation as a skill, turn a PDF or docs folder into a skill, merge two skills into one, or improve a skill from other sources (keep, replace and drop each method, rewrite in our own words, test it). Not for writing a skill from scratch (`create-skill`)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: agent-authoring
  category: agent-authoring
  department: agent-authoring
  related_skills:
    - create-skill
    - polyglot-copywriter
  invokes:
    - skill: create-skill
      when: Polish or lint the converted skill
    - skill: polyglot-copywriter
      when: Rewriting harvested prose
  tags:
    - convert
    - skill
    - extract
  capabilities:
    - skill_conversion
  languages:
    - en

---

# Convert as skill

One skill, six use cases. A classifier picks exactly one, or asks. Load only that use case's GUIDE. Copy, extract, distill and compose are different jobs.

For a new skill with no source file use `create-skill`. For a new rule, command or agent use `create-rule`, `create-command` or `create-agent`.

## Principles

1. **Classify first.** Run `scripts/classify.mjs` before opening a GUIDE. File layout beats wording. Never default to conversation.
2. **One use case per input.** A PDF is never copied as a rule. Mixed kinds are sequential jobs, or `ask` — not one blended skill.
3. **Copy vs extract vs distill vs compose.** Rules and agents copy the body. A conversation extracts what worked. A document distills structure. Merge composes a new skill and leaves the sources. Enhance adds to one skill from other sources, in our own words.
4. **Preview, then write. Never delete on your own.** Dry-run first. Remove originals only after the user has reviewed the result and asked.
5. **Third-party material stays private.** Do not commit a generated book skill, a clone of an upstream repo or a source map to this catalog. They live in an ignored scratch folder.

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
| `enhance-skill` | One skill folder plus upstream skills, repos or pages | **Add to** the skill: keep, replace or drop each method, write it ourselves | [enhance-skill](specialities/enhance-skill/GUIDE.md) |

Scripts: `scripts/classify.mjs`, `scripts/convert.mjs` (rules/agents only), `scripts/extract_document.py`, `scripts/merge.mjs`, `scripts/enhance.mjs` (read-only inventory and fetch plan). Document parsers live in `scripts/extractor/` (`pdf.py`, `html.py`, `docx.py`, `epub.py`, `text.py`, `rtf.py`, `sanitize.py`, `dependencies.py`, `config.py`, `exceptions.py`, `scan_generated_skill.py`). Templates: [harvest.md](templates/harvest.md), [merge-outline.md](templates/merge-outline.md), [enhance-map.md](templates/enhance-map.md).

## Do not

- Open a GUIDE before classify, or load two GUIDEs for one input.
- Treat "verbatim" as a use case. It is only how from-rule / from-agent copy the body.
- Default "convert this" with no files to a conversation.
- Run `convert.mjs` on a PDF or a skill folder, or `extract_document.py` on `rules/` / `commands/` / `agents/`.
- Use `enhance-skill` to combine two skills (that is merge), or to turn a book into a skill (that is from-document).
- Drop a useful source idea only because it was big. Replace it with a smaller version of your own.
- Delete sources, or commit a third-party book dump to this catalog.

## Related skills

- `create-skill`: write a skill from scratch, or fix the result after conversion.
- `polyglot-copywriter`: rewrite the harvested methods in simple, plain words.
- `second-opinion`: have a second reviewer check an enhancement before you report it.
- `create-rule`: the source is a rule and it should stay a rule.
- `create-command`: the source is a saved prompt and it should stay a command.
- `create-agent`: the source is a subagent and it should stay one.

## Done when

- Classify printed one kind (or asked / redirected) and only that GUIDE ran.
- The new skill lints clean. Skipped or refused inputs have a stated reason.
- The user knows which originals remain and how to remove or restore them.
