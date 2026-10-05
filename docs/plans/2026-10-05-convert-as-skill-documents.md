# Convert-as-skill: documents, PDFs, and prior sessions

> **Status:** plan only. Do not implement until this document is approved.
>
> **For agentic workers (after approval):** REQUIRED SUB-SKILL: Use `manage-stack` for the catalog edit. Then implement task-by-task.

**Goal:** Expand `convert-as-skill` so it can turn PDFs, documentation trees, and prior skill-authoring sessions into skills, without breaking verbatim conversion of rules, commands, and subagents, and without the agent guessing the wrong conversion path.

**Architecture:** One published skill. A **thin classifier** (script + SKILL.md step 0) picks exactly one speciality, or asks. Each speciality is a module with its own GUIDE and scripts. The model loads only that GUIDE. Adding a source kind is one classifier row, one speciality folder, and tests — SKILL.md does not grow.

**Tech Stack:** Catalog skill markdown + Node ≥ 20. Optional PATH extractors (`pdftotext`, Docling). No required Python package.

## Global Constraints

- Edit only `skills/`, `agents/`, `rules/`, `commands/`, `hooks/`, and `docs/agents/README.md` (plus this plan). Run `npm run sync`; do not hand-edit generated plugin output.
- Skill `name` equals its folder; `description` is one quoted line, ≤ 1024 characters, and says `Use when ...`.
- `SKILL.md` is a classifier, under ~150 lines (hard cap 500). Depth lives in `specialities/<kind>/GUIDE.md` (router-with-specialities hop). A guide may link to its own `references/`. No reference-to-reference chains.
- File-source conversion remains verbatim. Documents and sessions are extraction.
- Path choice is **deterministic**. If classify cannot prove one kind, it returns `ask`. Never default to conversation, never run two specialities on the same file.
- Node-only repo. Tests must pass with Node alone.
- No employer-owned content, secrets, or personal paths. Generated skills from third-party copyrighted books stay private; the document speciality must say so.
- If book-to-skill procedure or code is copied, record it in `THIRD_PARTY.md`.
- Lint, then `npm run sync && git diff --exit-code`, `npm run validate`, `npm test`.

---

## Why the first shape was wrong

A single SKILL.md with a routing table still lets the model **read every path** and pick by vibe. That is how convert-as-skill would:

- distill a `.mdc` rule as if it were a document
- harvest "this conversation" when the user attached a PDF
- dump a `docs/` folder through `convert.mjs` and mangle it

Wrong path is a **classification** bug, not a missing row in a table. The model must not choose. A script chooses; the model follows.

---

## Grounding (what exists)

| Source | Mechanism today | Copy or extract? |
|---|---|---|
| Rule (`.mdc` / `.md`, not always-on) | `scripts/convert.mjs` | Verbatim |
| Slash command | `scripts/convert.mjs` | Verbatim |
| Subagent | `scripts/convert.mjs` + `--fork` | Verbatim |
| This conversation | Harvest → `create-skill` | Extract |
| Long `CLAUDE.md` / `AGENTS.md` | Hand-off to `create-skill` | Not scripted |

Neighbor: `create-skill` (from scratch). `create-skill` already points conversion at `convert-as-skill`.

Tests cover only `convertSource()` for rule / command / agent.

Pattern to copy: `create-skill`'s **router with specialities**, and `super-architecture`'s "detect the job, then load only that guide."

---

## Research (kept short)

**book-to-skill** (MIT, `master`): extractor + generator. Take distill structure, progressive disclosure, technical vs text, analyze-only / fold-in, scanned-PDF abort, copyright caution. Leave the 862-line spec, host soup, publish flow, and the Python package.

**retro** (mattpocock): read a named session's transcripts, then harvest. Same job as conversation harvest, aimed at other skill-authoring sessions.

**Prior sessions here:** none. The shipped router is the prior session. Finding: a fifth source must be a module, not a second published skill, and path selection must be executable.

---

## Preferred design: classifier + specialities

One public surface (`convert-as-skill`). Three specialities. One classifier.

```
request (paths + wording)
        │
        ▼
scripts/classify.mjs          ← only this picks the path
        │
        ├── reject  → stop; point at create-skill / create-rule / …
        ├── ask     → one question; do not load a speciality
        └── ok      → load exactly one GUIDE, then its scripts
                ├── verbatim  specialities/verbatim/GUIDE.md   → convert.mjs
                ├── document  specialities/document/GUIDE.md   → extract-document.mjs
                └── session   specialities/session/GUIDE.md    → harvest.md
```

If the user passed several files of **different** kinds, classify returns one result **per file**. Run them sequentially. Never blend a PDF and a `.mdc` into one skill.

### Step 0 (in SKILL.md, first action)

```bash
node scripts/classify.mjs [--text "<user request>"] [--json] [path...]
```

Prints one line per input, then a summary. The agent:

1. Runs classify before opening any speciality GUIDE.
2. States the kind and reason in one line.
3. Loads **only** that GUIDE.
4. On `ask`, asks the listed question and stops.
5. On `reject`, names the other skill and stops.

Do not announce the classifier as a feature. Do not skip it when the request "looks obvious."

### Classifier contract

```
classify({ paths, text }) -> {
  status: 'ok' | 'ask' | 'reject',
  jobs: [{ kind, files, reason }],   // kind is verbatim-rule | verbatim-command | verbatim-agent | document | session
  question?: string,                 // when status is ask
  redirect?: 'create-skill' | 'create-rule' | 'create-command' | 'create-agent'
}
```

**Per-file evidence, in this order. First match wins. Wording never overrides a stronger file signal.**

| Order | Evidence | Kind |
|---|---|---|
| 1 | Request is "from scratch" / "write a new skill" and there is no existing source file | `reject` → `create-skill` |
| 2 | Request is a new rule / command / agent, no existing file to convert | `reject` → that create-* skill |
| 3 | Path segment `agents/` or `--kind agent` | `verbatim-agent` |
| 4 | Path segment `commands/` or `--kind command` | `verbatim-command` |
| 5 | Path segment `rules/`, or extension `.mdc`, or `--kind rule` | `verbatim-rule` |
| 6 | Extension `.pdf` `.epub` `.docx` `.html` `.htm` `.rtf` `.mobi` `.azw` `.azw3` | `document` |
| 7 | A directory of prose (e.g. `docs/` of `.md`/`.txt`/`.rst`) with **no** `rules/` `commands/` `agents/` layout | `document` |
| 8 | Explicit session words ("this conversation", "this session", "what we just did", "last time we wrote skills", a transcript path) **and no convertible files** | `session` |
| 9 | Bare `.md` / `.txt` not in a known layout, or mixed session-words + files, or empty request | `ask` |

Hard rules:

- **Files beat chat.** If any convertible file is present, never pick `session`.
- **Layout beats extension.** `rules/foo.md` is a rule, not a document, even if the user said "docs."
- **No default.** Conversation is not the fallback.
- **One kind per file.** A PDF is never passed to `convert.mjs`.
- **Ambiguity is `ask`.** One question: "Convert the PDF as a document skill, or also capture this conversation?" Not a menu of five.

Examples the tests must lock:

| Input | Result |
|---|---|
| `.cursor/rules/api.mdc` | `verbatim-rule` |
| `commands/commit.md` | `verbatim-command` |
| `agents/reviewer.md` | `verbatim-agent` |
| `book.pdf` | `document` |
| `docs/` with markdown, no rules layout | `document` |
| "save this session as a skill" (no files) | `session` |
| "convert this" + no files | `ask` |
| `book.pdf` + "and this conversation" | `ask` (two jobs named; do not merge) |
| `rules/a.mdc` + `chapter.pdf` | two `ok` jobs, run in sequence |
| "write a skill from scratch" | `reject` → `create-skill` |
| `CLAUDE.md` / `AGENTS.md` | `ask` (document distill vs hand-extract) |

### Specialities (modules)

Each speciality owns its procedure, scripts, and "do not." SKILL.md does not repeat them.

**`specialities/verbatim/GUIDE.md`**

Move today's mapping, subagent keep/wrap/convert, and convert.mjs steps here. `references/mapping.md` and `references/subagent.md` become this speciality's references (or stay top-level if shared — prefer speciality-local so document/session agents never read them).

**`specialities/document/GUIDE.md`**

book-to-skill as material: extract → confirm fingerprint → outline → user gate → `create-skill` shape (indexes + on-demand chapters) → lint. Copyright warning. Scanned PDF abort. Analyze-only / fold-in as the one escape hatch.

Extractor: `scripts/extract-document.mjs`

| Format | Default | Fallback |
|---|---|---|
| `.md` `.txt` `.rst` `.adoc` | `fs.readFile` | — |
| `.html` `.htm` | strip tags | — |
| `.pdf` | `pdftotext` if on PATH | skip with hint; optional Docling if technical and present |
| `.docx` | unzip `word/document.xml` | skip with hint |
| `.epub` | zip + HTML strip | skip with hint |

`--check` reports available extractors. Out of v1: MOBI/Calibre, GitHub publish, vendoring `book_to_skill/`.

**`specialities/session/GUIDE.md`**

Today's `conversation.md` plus retro: if the user named another session, read its transcripts first; state what you could not see; harvest with `templates/harvest.md`; extra Watch-for from navigation / checks / traps; outline; `create-skill`. Do not write `AGENTS.md` from a retro.

### Description (skill load, not path load)

The description only has to beat `create-skill` and name the source kinds. It must not be a second classifier.

Draft:

> Convert existing material into a skill: rules, slash commands, subagents, a conversation or prior session, or documents (PDF, HTML, Markdown, a docs folder). Use when asked to migrate a rule, command or agent to a skill, turn a PDF or docs folder into a skill, or save this session as a skill. Not for writing a skill from scratch (`create-skill`).

Front-load convert/migrate/PDF/session. "Not for from scratch" is the anti-collision with `create-skill`.

### File map

```
skills/agent-authoring/convert-as-skill/
├── SKILL.md                          # principles + classify step 0 + dispatch table
├── scripts/
│   ├── classify.mjs                  # path picker (tested)
│   ├── convert.mjs                   # verbatim only (unchanged API)
│   └── extract-document.mjs          # document extract + --check
├── specialities/
│   ├── verbatim/GUIDE.md             # + mapping.md, subagent.md
│   ├── document/GUIDE.md             # distill procedure
│   └── session/GUIDE.md              # conversation + retro
└── templates/harvest.md              # shared by session
```

| File | Responsibility |
|---|---|
| `SKILL.md` | Classifier instructions only. No convert steps. |
| `scripts/classify.mjs` | Source of truth for kind. |
| `scripts/convert.mjs` | File sources; refuses document extensions. |
| `scripts/extract-document.mjs` | Document extract; refuses rules/commands/agents paths. |
| `specialities/*/GUIDE.md` | One path's procedure. |
| `create-skill/SKILL.md` | Point PDF/docs/session conversion here. |
| `tests/authoring-scripts.test.mjs` | classify + extract + existing convertSource. |
| `THIRD_PARTY.md` | book-to-skill MIT and retro, if copied. |

**Refuse at the script boundary** so a confused agent still cannot take the wrong path: `convert.mjs` errors on `.pdf`; `extract-document.mjs` errors on `rules/` `commands/` `agents/` and `.mdc`.

### Scalability

| Change | Touch |
|---|---|
| New source kind (e.g. Notion export, URL corpus) | One `specialities/<kind>/`, one classifier branch, tests. SKILL.md adds one dispatch row. |
| Better PDF engine | `extract-document.mjs` only. |
| Verbatim mapping tweak | `specialities/verbatim/` only. |
| Retro sources (cloud transcripts) | `specialities/session/` only. |

Do not add a second published converter skill. That is two ways to do one task.

---

## Candidates (for the record)

**A. Classifier + specialities (this plan).** One skill, executable path pick, isolated modules.

**B. Sibling `document-to-skill`.** Rejected: two converters for one phrase; Python package; host soup.

**C. Fatter SKILL.md routing table (first draft).** Rejected: the model still reads every path and can pick wrong.

---

## Risks

| Risk | Mitigation |
|---|---|
| Model skips classify | SKILL.md: first action is the script; specialities say "if you did not run classify, go back" |
| Model loads every GUIDE anyway | Dispatch table is the only link from SKILL.md; specialities do not link to each other |
| `.md` in `docs/` vs a stray command | Classifier `ask`; layout beats extension |
| Weak PDF extraction | `--check`, technical/text, abort on empty/scanned |
| Copyrighted books in this catalog | Document GUIDE: keep private / do not commit |
| Session transcripts missing | Say so; never invent; never steal the path from attached files |
| Dual runtime | Optional PATH only |

---

## Implementation tasks (after approval)

### Task 1: Classifier (red → green)

- [ ] Failing tests for every row in the examples table, including `ask` and `reject`.
- [ ] Implement `scripts/classify.mjs` (`classify()` exported; CLI `--json`).
- [ ] Tests pass.
- [ ] Commit: `feat(convert-as-skill): classify conversion kind from paths and wording`

### Task 2: Guard the existing converter

- [ ] `convert.mjs` rejects document extensions and `docs/` batches with a "use document speciality" error.
- [ ] Tests for the reject.
- [ ] Commit: `fix(convert-as-skill): refuse document files in verbatim convert`

### Task 3: Split verbatim into a speciality

- [ ] Move mapping + subagent + current SKILL.md steps into `specialities/verbatim/GUIDE.md`.
- [ ] SKILL.md becomes principles + classify + dispatch.
- [ ] Lint. Existing convertSource tests still pass.
- [ ] Commit: `refactor(convert-as-skill): isolate verbatim conversion as a speciality`

### Task 4: Document speciality

- [ ] Failing extract tests (markdown concat, HTML strip, missing file, `--check`, empty PDF skip, fingerprint).
- [ ] `extract-document.mjs`; refuses rules/commands/agents paths.
- [ ] `specialities/document/GUIDE.md` (outline gate, copyright, scanned abort).
- [ ] Update `create-skill` pointer.
- [ ] Commit: `feat(convert-as-skill): distill documents through the document speciality`

### Task 5: Session speciality

- [ ] Move conversation harvest; add retro read of a named prior session; incomplete visibility.
- [ ] Dispatch row only; session GUIDE does not mention PDFs.
- [ ] Commit: `feat(convert-as-skill): harvest sessions in their own speciality`

### Task 6: Provenance and gate

- [ ] `THIRD_PARTY.md` if needed.
- [ ] Lint, `npm run sync && git diff --exit-code`, `npm run validate`, `npm test`.

---

## Done when

- Classify tests cover the example table; a PDF never returns `session` or `verbatim-*`.
- `convert.mjs` cannot convert a PDF; `extract-document.mjs` cannot convert a rule.
- SKILL.md has no convert steps, only classify + dispatch.
- Adding a kind does not require editing another speciality's GUIDE.
- Rule conversion is still verbatim. Document conversion outlines first. Session conversion does not invent transcripts.
- No second published converter. No Python package in `package.json`.

---

## Checkpoint

Path selection is a script. Specialities do not share procedure. The model does not guess.

Before you approve:

- Classifier + specialities (not a fatter SKILL.md, not a sibling skill)?
- v1 Node extractor + optional `pdftotext` / Docling, or vendor Python?
- Session speciality in v1, or verbatim + document only until transcripts are reliable?
- Third-party book PDFs: private-only warning, or refuse to write them into this catalog?
