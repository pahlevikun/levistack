# Convert-as-skill: documents, PDFs, and prior sessions

> **Status:** plan only. Do not implement until this document is approved.
>
> **For agentic workers (after approval):** REQUIRED SUB-SKILL: Use `manage-stack` for the catalog edit. Then implement task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand `convert-as-skill` so it can turn PDFs, documentation trees, and prior skill-authoring sessions into skills, without breaking verbatim conversion of rules, commands, and subagents.

**Architecture:** Keep `convert-as-skill` as the single public router. File sources (rule / command / agent) stay a verbatim Node script. Documents and PDFs take a new distill path adapted from [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) (extract → analyze → progressive-disclosure skill). Prior sessions take a retro-style harvest path that extends the existing conversation mechanism. Do not vendor book-to-skill wholesale and do not add a second published converter skill.

**Tech Stack:** Catalog skill markdown + Node ≥ 20 scripts (existing `convert.mjs` style). Optional local extractors (`pdftotext`, Python `docling`) when present; never a required Python package in this Node catalog.

## Global Constraints

- Edit only `skills/`, `agents/`, `rules/`, `commands/`, `hooks/`, and `docs/agents/README.md` (plus this plan). Run `npm run sync`; do not hand-edit generated plugin output.
- Skill `name` equals its folder; `description` is one quoted line, ≤ 1024 characters, and says `Use when ...`.
- `SKILL.md` stays a router under ~200 lines (hard cap 500). Depth goes in `references/`, one level deep.
- File-source conversion remains verbatim. Improvements are a separate change. Documents and sessions are extraction, like today's conversation path.
- Node-only repo (`engines.node: ">=20"`, `npm test` on `tests/*.test.mjs`). No Python runtime as a required dependency.
- No employer-owned content, secrets, or personal paths. Generated skills from third-party copyrighted books stay private; the skill must say so.
- If any book-to-skill code or substantial procedure is copied, record it in `THIRD_PARTY.md` (referenced by `AGENTS.md` but missing in this tree today).
- Lint with `node skills/agent-authoring/create-agent/scripts/lint.mjs skills/agent-authoring/convert-as-skill`. Then `npm run sync && git diff --exit-code`, `npm run validate`, `npm test`.

---

## Grounding (what exists)

`convert-as-skill` already is a router with four mechanisms:

| Source | Mechanism | Copy or extract? |
|---|---|---|
| Rule (`.mdc` / `.md`, not always-on) | `scripts/convert.mjs` | Verbatim body |
| Slash command | `scripts/convert.mjs` | Verbatim body |
| Subagent | `scripts/convert.mjs` + `--fork` | Verbatim body; isolation optional |
| This conversation | Harvest worksheet → `create-skill` | Extract |
| Long `CLAUDE.md` / `AGENTS.md` | Hand-off to `create-skill` | Not scripted |

Principles that must survive:

1. Copy file-based sources verbatim.
2. Convert only what fits a skill (always-on rules stay rules).
3. The description is the part to write well.
4. Preview before writing; never delete originals on your own.
5. A conversation is evidence, not a spec.

Neighbor skills: `create-skill` (write from scratch, lint, progressive disclosure), `create-rule` / `create-command` / `create-agent` (new artifacts). `create-skill` already points conversion work at `convert-as-skill`.

Tests today cover only `convertSource()` for rule / command / agent. Conversation harvest is unscripted.

---

## Research

### book-to-skill (source of the document path)

Repo: https://github.com/virgiliojr94/book-to-skill (default branch `master`, MIT). Docs: https://booktoskill.is-a.dev/guide/

Two halves:

1. **Deterministic extractor** (Python): PDF / EPUB / DOCX / HTML / RTF / MOBI / Markdown / text → `full_text.txt` + `metadata.json`. Graceful fallbacks; one bad source is skipped.
2. **Spec-driven generator** (agent follows an 862-line `SKILL.md`): analyze ToC → chapter files → glossary / patterns / cheatsheet → small front-loaded `SKILL.md`.

What to take (as material, not a fork):

- Distill structure, not dump text. Named frameworks, decision rules, anti-patterns. Practitioner voice: `Use X when Y`.
- Progressive disclosure: `SKILL.md` ~4k tokens with indexes; `chapters/*.md` load on demand.
- Modes: full convert, analyze-only, generate-from-analysis, fold-in / update.
- Content type: technical (tables/code, Docling) vs text-heavy (fast `pdftotext` / pypdf).
- Depth: `reference` vs `study` (worked examples only at study depth).
- Security: strip zero-width / tag-block Unicode; do not copy raw passages of copyrighted books; scan generated skills for instruction-override phrases.
- Inputs beyond books: docs folders, ADRs, runbooks, specs, research clusters.

What not to take:

- The 862-line generator spec, host-probing candidate soup, GitHub publish flow, discovery-tax tooling, or the Python package as a catalog dependency.
- Writing generated book skills into `~/.agents/skills` by default when this catalog already has destination rules (project skills folder, user skills, or `skills/<group>/`).
- Shipping copyrighted book content in levistack.

### retro (source of the session path)

Skill: [mattpocock/skills retro](https://www.skills.sh/mattpocock/skills/retro) (`npx skills add https://github.com/mattpocock/skills --skill retro`).

Behavior to clone: when asked to look at a previous session, read that session's primary sources (transcripts / logs; current session if unspecified), then extract reusable improvements. Categories: navigation pointers, automated checks, coding standards vs mechanical lints, AGENTS.md bloat, tool economy, no-op steering, information access.

This is the same job as `references/conversation.md` (harvest what worked), aimed at **other** skill-authoring sessions, not only the current chat.

### Prior skill-creation sessions (this retro pass)

| Probe | Result |
|---|---|
| Cloud agents on this repo with code changes | None besides this planning run |
| Git history of `skills/agent-authoring/convert-as-skill` | Single commit: initial levistack import |
| GitHub issues / PRs mentioning convert-as-skill | None found |
| `THIRD_PARTY.md` | Referenced in `AGENTS.md` / `README.md`, file absent |

So there is no earlier convert-as-skill implementation transcript to mine. The previous "session" is the shipped skill itself. Findings from that artifact:

- **Navigation:** the router + `references/{mapping,subagent,conversation}.md` shape is the right module split. A fifth source should be another row and another reference file, not a new published skill.
- **Automated checks:** `convert.mjs` is tested; any new extractor must be too. Conversation harvest has no executable check today — keep session harvest as a worksheet, not a second untested script, unless listing transcripts is deterministic.
- **Two ways to do one task:** adding a sibling `book-to-skill` skill next to `convert-as-skill` would give agents two converters. Reject that.
- **Information access:** conversation harvest cannot see compacted or other-session transcripts. A session source that knows where to look (Cursor cloud transcripts, local session logs) closes that gap.
- **Tool economy:** do not pull book-to-skill's SKILL.md into context as the generator. A short `references/document.md` with budgets and output templates is enough.
- **Missing provenance file:** restoring `THIRD_PARTY.md` belongs in the implementation change if we copy procedure or code.

---

## Problem restated

Users already say "convert this into a skill" for rules, commands, agents, and chats. They also say it for a PDF, a `docs/` tree, or "what we learned last time we wrote skills." Today those last requests fall through to `create-skill` by hand, or the agent dumps the document into one oversized `SKILL.md`.

The gap is a **distill** mechanism that still lives behind the same skill, with the same preview / lint / destination rules.

---

## Candidates

Two structurally distinct shapes. Architect rule: pick one public surface; hide the rest.

### A. Expand the existing router (preferred)

`convert-as-skill` gains two source rows. Verbatim conversion is unchanged. Documents get `references/document.md` + a small Node extract script. Sessions extend `references/conversation.md` (or a sibling `session.md`) with retro's "read the named session first" step.

```
"convert this into a skill"
        │
        ▼
convert-as-skill (SKILL.md router)
        │
        ├── rule / command / agent  → convert.mjs (verbatim)
        ├── conversation            → harvest.md → create-skill
        ├── prior session(s)        → retro read → harvest.md → create-skill
        └── pdf / docs / html / …   → extract-document → outline → create-skill
```

**Because**

- One trigger description. Agents already load this skill for "convert … to a skill."
- Conversation already proved that not every source is verbatim. Documents and sessions are the same class: evidence in, skill out.
- Matches `create-skill`'s router pattern and the 200-line body budget.
- book-to-skill's value is the pipeline and output shape, not its packaging.

**Costs**

- The description must name PDFs, docs, and sessions without blowing the 1024-character cap.
- Document extraction quality will be weaker than book-to-skill's Docling path unless optional tools are present.
- Session listing depends on host (Cursor cloud vs local logs) and will be incomplete; the skill must say what it could not see.

**Would change if** document conversion grew its own scripts, evals, and formats past what a reference file can hold. Then split the distill path into a sibling skill and leave convert-as-skill as a one-line route.

### B. Publish a sibling `document-to-skill` (rejected)

Vendor or rewrite book-to-skill as `skills/agent-authoring/document-to-skill` (or `book-to-skill`). `convert-as-skill` stays file-only and maybe links out.

**Because it looks attractive:** book-to-skill is already a complete product; isolation keeps verbatim conversion simple.

**Rejected because**

- Two published skills for one user phrase ("convert this PDF into a skill"). Agents copy whichever they find first (design red flag: two ways to do one task).
- Python package + 862-line spec does not fit this Node catalog or `create-skill`'s size rules.
- Host-location soup (`~/.copilot`, Hermes, OpenClaw, …) fights levistack's destination table.
- The user asked to enhance convert-as-skill, not to add a parallel converter.

A later split is allowed if the distill path outgrows the router. It is not the first shape.

---

## Preferred design

**Recommendation:** Candidate A. In-process: existing router + two new mechanisms. Modeling: keep convert-as-skill's source-kind language (`rule`, `command`, `agent`, `conversation`, add `document` and `session`). Deployable shape: one catalog skill folder.

### Public surface

Description (draft, to be tightened against the 1024-char cap):

> Convert existing material into a skill: agent-requested rules, slash commands, subagents, the current or a previous conversation, or documents (PDF, EPUB, HTML, Markdown, a docs folder). Use when asked to migrate rules, commands or agents to skills, turn a PDF or documentation into a skill, save this session as a skill, or capture what we just did as a reusable skill.

Router table gains:

| Source | Mechanism | Go to |
|---|---|---|
| PDF, EPUB, DOCX, HTML, Markdown, docs folder, URL of a doc | Extract, then distill | `references/document.md` |
| A previous agent session (named, or "last time we wrote skills") | Retro read, then harvest | `references/session.md` (or a section of `conversation.md`) |

### Document path (adapted from book-to-skill)

Not implemented bodies — the contract:

```
extractDocument(inputs, { mode: 'technical' | 'text' }) -> {
  workdir, fullTextPath, metadataPath, warnings
}

metadata: {
  title?, pages?, words?, tokens?, sources: [{ path, kind, sha256, extractor }],
  chapters?: [{ title, start }],
  extractionMode
}
```

Agent procedure (in `references/document.md`), after extract:

1. Confirm the extraction is the requested files (source names + fingerprint).
2. Show a short outline: proposed skill name, `description`, chapter/section list, what will be dropped, destination, copyright warning. Stop for the user (same as conversation harvest).
3. Write with `create-skill` shape: `SKILL.md` (core frameworks + indexes), `references/` or `chapters/` for on-demand sections, optional `glossary.md` / `patterns.md` / `cheatsheet.md` when the source is book-like. For a small docs folder, one `SKILL.md` plus one reference file is enough.
4. Lint. Refuse to overwrite unless `--force` / user asked.
5. Report originals; do not delete them.

Quality rules to copy in short form:

- Structure, not a dump. No raw passages of third-party books.
- Front-load `SKILL.md`. Indexes point at on-demand files.
- Technical vs text-heavy extractor choice. Scanned PDFs: abort and tell the user to OCR.
- Analyze-only and fold-in are the escape hatches (one default: full convert).

Extractor implementation (Node, in `scripts/`):

| Format | Default | Fallback |
|---|---|---|
| `.md` `.txt` `.rst` `.adoc` | `fs.readFile` | — |
| `.html` `.htm` | strip tags in Node | — |
| `.pdf` | `pdftotext` if on PATH | skip with install hint; optional `python3 -m docling` if user chose technical and it exists |
| `.docx` | unzip `word/document.xml` in Node | skip with hint |
| `.epub` | zip + HTML strip | skip with hint |

Do not add npm dependencies unless tests cannot be honest without one. Prefer PATH tools and stdlib. `--check` prints which extractors are available, same idea as book-to-skill, implemented in Node.

Out of v1: MOBI/AZW/Calibre, GitHub publish of generated skills, discovery-tax benchmarks, copying `book_to_skill/` into this repo.

### Session path (cloned from retro)

When the user says "use last time we created skills", "retro the previous convert session", or names a session:

1. Read that session's primary sources (Cursor cloud transcripts when the tools exist; local session logs if provided; otherwise the current conversation). State what you could not see.
2. Harvest with `templates/harvest.md` — same fields as conversation conversion.
3. Extra retro pass: if the session was skill-authoring, also pull navigation pointers, missing checks, and traps into the new skill's Watch-for / Principles, not into `AGENTS.md`.
4. Outline → user confirm → `create-skill`.

Do not auto-write environment files (`AGENTS.md`, new always-on rules) from a retro. That is retro's original job and stays opt-in.

### What stays unchanged

- `scripts/convert.mjs` public API and verbatim behavior.
- Skip rules for always-on and file-scoped rules.
- Destinations: project skills folder, user skills, or catalog `skills/<group>/`.
- Dry-run, no delete, lint, try the trigger.

### File map (implementation, after approval)

| File | Responsibility |
|---|---|
| `skills/agent-authoring/convert-as-skill/SKILL.md` | Router: add document + session rows; keep principles; mention copyright for book PDFs |
| `skills/agent-authoring/convert-as-skill/references/document.md` | Distill procedure, budgets, output templates, extractor invocation |
| `skills/agent-authoring/convert-as-skill/references/session.md` | Retro read + harvest; where transcripts live |
| `skills/agent-authoring/convert-as-skill/templates/harvest.md` | Unchanged, reused by session |
| `skills/agent-authoring/convert-as-skill/scripts/extract-document.mjs` | Deterministic extract + `--check` + metadata JSON |
| `skills/agent-authoring/convert-as-skill/scripts/convert.mjs` | No document kinds. File sources only |
| `tests/authoring-scripts.test.mjs` | Tests for extract-document (and existing convertSource tests) |
| `skills/agent-authoring/create-skill/SKILL.md` | Point "PDF / docs / previous session" at convert-as-skill |
| `THIRD_PARTY.md` | Create if we copy procedure/code; cite virgiliojr94/book-to-skill MIT and mattpocock retro as inspiration |

---

## Risks

| Risk | Mitigation |
|---|---|
| Router `SKILL.md` grows past 200 lines | Keep document and session steps out of the body; link only |
| Weak PDF extraction without Docling | `--check`, technical/text prompt, abort on empty/scanned PDFs |
| Copyrighted book skills published in this catalog | Explicit do-not-commit / keep-private rule in `document.md` |
| Session transcripts unavailable in this environment | Say so; fall back to current conversation; never invent a prior session |
| Dual runtime creep (Python package) | Optional PATH/python only; tests must pass with Node alone |
| Description collision with `create-skill` | create-skill keeps "from scratch"; convert-as-skill keeps "from existing material" and names PDF/docs/session |

---

## Implementation tasks (after approval)

### Task 1: Document extractor (red → green)

**Files:** `skills/agent-authoring/convert-as-skill/scripts/extract-document.mjs`, `tests/authoring-scripts.test.mjs`

- [ ] Write failing tests for: markdown/text concat with source markers; HTML strip; missing file error; `--check` JSON/text report; empty PDF / no extractor → skip with reason; fingerprint in metadata.
- [ ] Run `node --test tests/authoring-scripts.test.mjs` and confirm the new tests fail.
- [ ] Implement the minimal extractor (stdlib + optional `pdftotext`).
- [ ] Re-run tests until they pass.
- [ ] Commit: `feat(convert-as-skill): extract documents into text and metadata`

### Task 2: Document procedure in the router

**Files:** `SKILL.md`, `references/document.md`, `create-skill/SKILL.md`

- [ ] Add the document row to the router tables ("What do you want to convert?" / "What converts").
- [ ] Write `references/document.md`: steps, technical vs text, outline-before-write, output shape, copyright, scanned-PDF abort, analyze-only and fold-in as the one escape hatch.
- [ ] Update `create-skill` to send PDF/docs conversion here.
- [ ] Lint the skill folder.
- [ ] Commit: `docs(convert-as-skill): add document distill path`

### Task 3: Session / retro harvest

**Files:** `references/session.md` or `references/conversation.md`, `SKILL.md`

- [ ] Add the session row and a short procedure: find sources, harvest, extra retro categories, outline, write via `create-skill`.
- [ ] Document incomplete visibility (compacted chats, missing cloud transcripts).
- [ ] Lint.
- [ ] Commit: `docs(convert-as-skill): harvest prior sessions like retro`

### Task 4: Provenance, sync, gate

**Files:** `THIRD_PARTY.md` (if needed), generated plugin tables via `npm run sync`

- [ ] Record book-to-skill / retro inspiration or copied fragments.
- [ ] `npm run sync && git diff --exit-code` (stage generated output with the source edit).
- [ ] `node skills/agent-authoring/create-agent/scripts/lint.mjs skills/agent-authoring/convert-as-skill`
- [ ] `npm run validate && npm test`
- [ ] Commit generated sync output with the last source change, not as a separate purpose if it is the same change.

---

## Done when (after implementation)

- Asking to convert a rule still produces a verbatim body (existing tests green).
- Asking to convert a PDF or `docs/` folder produces an outline, then a skill with indexes and on-demand files, lint-clean.
- Asking to convert a previous skill-authoring session reads available transcripts, harvests, and does not invent sessions it could not see.
- `pdftotext` / Docling absence is a skip with an install hint, not a crash.
- No second published converter skill. No Python package in `package.json`.

---

## Checkpoint

The approach is fixed from here: one router, two new mechanisms, book-to-skill as material not a vendored sibling.

Before you approve, check:

- Is expanding `convert-as-skill` (not adding `document-to-skill`) the shape you want?
- Is v1's Node extractor + optional `pdftotext` / Docling enough, or do you want the Python package vendored despite the Node catalog?
- Should prior-session harvest be a first-class source in v1, or conversation-only until transcripts are reliable in this environment?
- Generated skills from third-party books: private-only warning, or refuse to write them into this catalog entirely?
