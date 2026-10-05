# Convert-as-skill: use cases, documents, and merge

> **Status:** plan only. Do not implement until this document is approved.
>
> **For agentic workers (after approval):** REQUIRED SUB-SKILL: Use `manage-stack`. Then implement task-by-task.

**Goal:** One published skill, `convert-as-skill`, with **named use cases**. A classifier picks exactly one use case, or asks. The agent loads only that use case's GUIDE. The word "verbatim" is not a use case; it is only how the from-rule / from-agent path treats the file body (copy it, do not rewrite).

**Architecture:** Classifier script + one speciality folder per use case. Adding a use case is one classifier branch, one `specialities/<use-case>/`, and tests.

**Tech Stack:** Node ≥ 20. Optional PATH extractors for PDFs. No required Python package.

## What "verbatim" meant (and why we drop it as a name)

In the current skill, **verbatim** means: take a rule, command, or agent **file** and copy its body into `SKILL.md` unchanged. Only the frontmatter is rewritten (`name`, `description`). Improvements to the body are a later, reviewed change.

That is a copy mode, not a use case. Users do not say "verbatim." They say "convert this rule," "convert this agent," "save this conversation," "turn this PDF into a skill," "merge these two skills."

The plan now names **use cases**, not copy modes.

| Use case | What you start with | What happens to the text |
|---|---|---|
| From a rule or command | `.mdc` / `rules/` / `commands/` | **Copy the body.** Do not rewrite. |
| From an agent | `agents/*.md` | **Copy the body**, after keep / wrap / convert. Isolation may be lost. |
| From a conversation or prior session | Chat / transcript | **Extract** what worked. Dead ends out. |
| From a document | PDF, docs folder, HTML, … | **Distill** structure (frameworks, indexes). Not a dump. |
| Merge skills | Two or more existing skill folders | **Compose** one new skill. Sources stay until you ask to delete them. |

Copy vs extract vs distill vs compose are different on purpose. That is why they are different use cases, not one "verbatim" bucket plus extras.

---

## Global Constraints

- Catalog write surface only (`skills/`, …) plus this plan. `npm run sync`; no hand-edits of generated plugin files.
- `SKILL.md` is a classifier, under ~150 lines. Each use case lives in `specialities/<use-case>/GUIDE.md`.
- Path choice is deterministic. `ask` when unproven. Never default to conversation.
- One use case per input. A PDF is never copied as a rule. A conversation is never merged with a skill folder unless the user asked to merge.
- Node-only tests. Optional `pdftotext` / Docling on PATH.
- No secrets, employer names, or copyrighted book dumps in this catalog. Document use case: keep generated book skills private.
- Provenance in `THIRD_PARTY.md` if book-to-skill or retro procedure is copied.

---

## Use cases (modules)

One public skill. Five use cases. One classifier.

```
request (paths + wording)
        │
        ▼
scripts/classify.mjs
        │
        ├── reject  → create-skill / create-rule / create-command / create-agent
        ├── ask     → one question; load no GUIDE
        └── ok      → load exactly one GUIDE
              ├── from-rule         copy body via convert.mjs
              ├── from-agent        keep / wrap / convert, then convert.mjs
              ├── from-conversation extract via harvest.md
              ├── from-document     distill via extract-document.mjs
              └── merge-skills      compose via merge.mjs + outline
```

### 1. From a rule or command (`specialities/from-rule/`)

Today's rule + command path. User: "convert this rule," "turn `/commit` into a skill," "migrate `.cursor/rules`."

- Script copies the body. Always-on rules stay rules. File-scoped rules need `--paths`.
- Commands keep `disable-model-invocation: true`.
- Do not run harvest or document distill.

### 2. From an agent (`specialities/from-agent/`)

Separate from rules. User: "convert this subagent," "make reviewer a skill."

- First decide keep, wrap (`context: fork`), or convert. Isolation and `tools` are lost on convert.
- Then copy the body; list any "you are a separate agent" line edits.
- A different GUIDE so the model cannot skip the keep/wrap/convert question and treat an agent like a rule.

### 3. From a conversation (`specialities/from-conversation/`)

Separate from files. User: "save this session as a skill," "what we just did," "last time we wrote skills" (retro: read that session's transcripts first).

- Evidence, not a spec. Harvest worksheet. Outline, then `create-skill`.
- No files attached → this use case only when the words name a conversation/session. "Convert this" with no files is `ask`, not conversation.

### 4. From a document (`specialities/from-document/`)

User: "turn this PDF into a skill," "convert the docs folder."

- Extract → fingerprint check → outline → distill (indexes + on-demand chapters). book-to-skill as material, not a vendored Python package.
- Scanned PDF abort. Copyright: do not commit third-party book skills to this catalog.

### 5. Merge skills (`specialities/merge-skills/`) — new

User: "merge these skills into one," "combine `foo` and `bar`," two or more folders that each contain `SKILL.md`.

Not a convert-from-files job and not create-from-scratch. `create-skill` already says "if two skills overlap, merge them"; this use case is the procedure that does it.

**Inputs:** two or more skill directories (each has `SKILL.md`). Optional target name.

**Classifier:** wording `merge` / `combine` / `into one skill`, or two-plus skill folders and no other kind. One skill folder + a rule file → `ask`. Merge + a PDF → `ask` (do not silently distill).

**Procedure:**

1. Read each `SKILL.md` (name, description, body, linked `references/` `scripts/` `templates/`).
2. Classify overlap: **same job** vs **distinct jobs**.
3. Outline (stop for the user):
   - proposed new `name` and `description` (`Use when ...`, trigger words from all sources, no "and" if it is really two jobs)
   - keep / drop / rewrite per source
   - shape: one `SKILL.md` if same job; **router** (`templates/skill-router.md`) if three or more distinct tasks
   - where it will be written; sources will not be deleted
4. After approval, write the new skill. Copy supporting files that are still referenced; do not copy dead references.
5. Lint. Do not overwrite an existing skill unless asked. Do not delete the source skills unless asked.

**Same job:** one procedure, combined steps, one description. Deduplicate. Prefer the clearer wording.

**Distinct jobs:** do not smash into one narrative. Make a router SKILL.md that dispatches to `references/<old-name>.md` (or keep specialities). If the honest name would need "and," say so in the outline and offer to keep them separate.

**Do not:** rewrite source skills in place as the merge; invent overlap that is not in the files; merge a skill with a rule/PDF/conversation in the same job.

---

## Classifier

```
classify({ paths, text }) -> {
  status: 'ok' | 'ask' | 'reject',
  jobs: [{ kind, files, reason }],
  question?: string,
  redirect?: 'create-skill' | 'create-rule' | 'create-command' | 'create-agent'
}
```

`kind`: `from-rule` | `from-command` | `from-agent` | `from-document` | `from-conversation` | `merge-skills`

(`from-command` shares the from-rule GUIDE; the kind is distinct so tests and logs stay precise.)

**Order. First match wins. File layout beats wording. Merge wording beats "convert" when two-plus skill folders are present.**

| Order | Evidence | Kind |
|---|---|---|
| 1 | From scratch / new skill, no source file | `reject` → `create-skill` |
| 2 | New rule / command / agent, no file to convert | `reject` → that create-* skill |
| 3 | Two or more directories each containing `SKILL.md`, or merge/combine wording with skill folders | `merge-skills` |
| 4 | Path `agents/` | `from-agent` |
| 5 | Path `commands/` | `from-command` (from-rule GUIDE) |
| 6 | Path `rules/` or `.mdc` | `from-rule` |
| 7 | `.pdf` `.epub` `.docx` `.html` `.rtf` `.mobi` … | `from-document` |
| 8 | `docs/` (or similar) of prose, no rules/commands/agents layout | `from-document` |
| 9 | Conversation/session words **and no convertible files** | `from-conversation` |
| 10 | Else | `ask` |

Hard rules:

- Files beat chat. Skill folders beat "save this conversation."
- Two skill folders without merge wording → `ask` ("merge into one skill, or convert each?").
- `book.pdf` + "and this conversation" → `ask`.
- Mixed kinds in one request → separate jobs, run in sequence, never one blended skill unless the use case is `merge-skills`.

Examples:

| Input | Result |
|---|---|
| `.cursor/rules/api.mdc` | `from-rule` |
| `agents/reviewer.md` | `from-agent` |
| "save this conversation as a skill" (no files) | `from-conversation` |
| `book.pdf` | `from-document` |
| `skills/foo` + `skills/bar` (both have SKILL.md) + "merge" | `merge-skills` |
| `skills/foo` + `skills/bar` (no merge wording) | `ask` |
| "convert this" (no files) | `ask` |
| "write a skill from scratch" | `reject` → `create-skill` |
| `rules/a.mdc` + `chapter.pdf` | two jobs: from-rule, then from-document |

### Step 0

```bash
node scripts/classify.mjs [--text "<user request>"] [--json] [path...]
```

Run before opening any GUIDE. State kind and reason. Load only that GUIDE. On `ask` / `reject`, stop.

---

## Description (skill load, not path load)

> Convert existing material into a skill, or merge existing skills into one. Use when asked to convert a rule, command or agent to a skill, save a conversation as a skill, turn a PDF or docs folder into a skill, or merge two skills into one. Not for writing a skill from scratch (`create-skill`).

---

## File map

```
skills/agent-authoring/convert-as-skill/
├── SKILL.md
├── scripts/
│   ├── classify.mjs
│   ├── convert.mjs              # from-rule / from-command / from-agent bodies
│   ├── extract-document.mjs
│   └── merge.mjs                # list sources, detect skill folders, draft tree
├── specialities/
│   ├── from-rule/GUIDE.md       # + mapping.md
│   ├── from-agent/GUIDE.md      # + subagent.md
│   ├── from-conversation/GUIDE.md
│   ├── from-document/GUIDE.md
│   └── merge-skills/GUIDE.md
└── templates/
    ├── harvest.md
    └── merge-outline.md
```

Script guards: `convert.mjs` refuses PDFs and skill-folder merges. `extract-document.mjs` refuses `rules/` `commands/` `agents/`. `merge.mjs` refuses unless every input is a skill directory.

---

## Implementation tasks (after approval)

1. **Classifier** — tests for the example table, including merge vs ask vs conversation.
2. **from-rule + from-agent** — split today's convert path into two GUIDEs; `convert.mjs` stays the copy engine.
3. **from-conversation** — harvest + retro of a named prior session.
4. **from-document** — extract + distill GUIDE.
5. **merge-skills** — outline template, same-job vs router, lint, do not delete sources.
6. **Gate** — lint, sync, validate, test. `THIRD_PARTY.md` if needed.

---

## Done when

- "Verbatim" does not appear as a use-case name in SKILL.md.
- Conversation and from-rule/from-agent cannot load each other's GUIDEs for one input.
- Merge requires two-plus skill folders (or an explicit merge ask); it does not run on a PDF or a chat.
- Classify tests lock the example table.
- No second published converter skill.

---

## Checkpoint

- Five use cases (from-rule, from-agent, from-conversation, from-document, merge-skills) behind one classifier?
- Merge in v1 with the rest, or after from-rule / from-conversation / from-document?
- Third-party book PDFs: private-only warning, or refuse to write them into this catalog?
