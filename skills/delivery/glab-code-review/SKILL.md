---
name: glab-code-review
description: "Use when reviewing your local git diff before opening a PR, requesting a git-range code review before merge, receiving and acting on review feedback with verify-first discipline, or reviewing a GitLab merge request via glab with draft inline notes."
context: fork
metadata:
  version: "4.1.0"
---

# glab-code-review

Four modes. Pick one from the user goal — do not mix GitLab draft posting with local review unless they ask.

| Goal | Mode | Detail |
|------|------|--------|
| Review **uncommitted / staged** changes before a PR | **Diff** | [references/review-diff.md](references/review-diff.md) |
| Review **your** commits before merge / next task | **Request** | [references/requesting-review.md](references/requesting-review.md), template [references/code-reviewer.md](references/code-reviewer.md) |
| **Implement** feedback from a human or external reviewer | **Receive** | [references/receiving-review.md](references/receiving-review.md) |
| **Review someone else's GitLab MR** (glab, draft notes) | **GitLab MR** | Below + [references/draft-review-flow.md](references/draft-review-flow.md) |

Peer skills for GitLab MR mode: [`super-noslop`](../../engineering/super-noslop/SKILL.md) (alias: `noslop`), [`polyglot-copywriter`](../../engineering/polyglot-copywriter/SKILL.md) (`glab-code-review` use case).

**Arguments (`$ARGUMENTS`):** MR URL, MR number for current repo, or empty (current branch MR) — GitLab MR mode only.

---

## Diff review (pre-PR)

Self-review the working tree: full diff read, edge cases, tests for behavior changes, scope creep, findings as **Must fix** / **Should fix** / **Nit**. Full procedure: [references/review-diff.md](references/review-diff.md).

When: before opening a PR; after a large local edit without dispatching a reviewer. For committed range review, use **Request** mode.

---

## Requesting review

Review early; give the reviewer **git range + requirements**, not your session history.

1. Resolve SHAs: `BASE_SHA` (e.g. `origin/main` or task start), `HEAD_SHA` (`git rev-parse HEAD`).
2. Dispatch a read-only reviewer using [references/code-reviewer.md](references/code-reviewer.md) (`{DESCRIPTION}`, `{PLAN_OR_REQUIREMENTS}`, SHAs).
3. Triage: fix **Critical** immediately, **Important** before proceeding, **Minor** later; push back with reasoning when wrong.

When: after each subagent task, major features, before merge — see [references/requesting-review.md](references/requesting-review.md).

---

## Receiving review

Verify before implementing. No performative agreement; technical acknowledgment or reasoned pushback.

Pattern: read fully → understand (restate or ask) → verify against codebase → evaluate → respond → implement one item at a time with tests.

If anything is unclear, **stop** and clarify all items before partial fixes. Full rules, YAGNI checks, GitHub thread replies: [references/receiving-review.md](references/receiving-review.md).

---

## GitLab MR review (glab)

Three phases: **preview** (read-only) → **draft to MR** (unpublished GitLab draft notes) → **publish** (explicit only).

**Default write path:** GitLab **draft notes** (`draft_notes` API / bundled scripts). Author sees nothing until publish.

**Comment shape:** inline findings with **code suggestions** on diff lines — not a wall-of-text MR summary.

Operator reference: [references/gitlab-mechanics.md](references/gitlab-mechanics.md), [references/draft-review-flow.md](references/draft-review-flow.md), [references/review-dimensions.md](references/review-dimensions.md), [references/comment-body-format.md](references/comment-body-format.md).

### Phase 1: Deep read-only preview

1. Harvest context (`context-harvester` or docs), playbook checklist, then `glab mr view` / `glab mr diff`.
2. Read beyond hunks; optional `codebase-memory`; run focused tests on source branch when possible.
3. Apply [references/review-dimensions.md](references/review-dimensions.md) (compatibility → security → correctness → tests → perf → principles → **noslop** → hygiene). Optional subagents: `security-reviewer`, `tdd-runner`, `reviewer`.
4. Prose pipeline for user-facing comment bodies: draft → **super-noslop** (after) → **polyglot-copywriter** (`glab-code-review`, `register: santai`, [simple-prose.md](../../engineering/polyglot-copywriter/references/simple-prose.md)).
5. Chat table of findings (`file:line`, dimension, impact, short inline draft). Report CI, verdict, draft-ready count. **Stop and wait** for which numbers to draft, fix locally, or skip.

### Phase 2: Draft to MR (explicit confirmation)

Draft only — never publish. `eval "$(scripts/mr-context.sh <repo> <number>)"` then prefer `scripts/post-draft-inline-comment.sh`; MR-wide items → `scripts/post-draft-note.sh`; list with `scripts/list-draft-notes.sh`. Tell user drafts are hidden until GitLab publish or **"publish drafts"**. Never `#<number>` in GitLab prose.

### Phase 3: Publish drafts (explicit confirmation)

Only after user says **publish** / **publish drafts**:

```bash
export REVIEWER_STATE=requested_changes   # or reviewed for comment-only
export SUMMARY_FILE=
scripts/publish-draft-notes.sh <repo> "$PROJECT_ID" <number>
```

Never set `reviewer_state=approved` from automation. Immediate publish via `scripts/post-inline-comment.sh` only if user explicitly skips drafts.

### GitLab quick routing

| User says | Phase |
|-----------|-------|
| "review MR", "review !123" | 1 |
| "draft 1,3", "post as draft" | 2 |
| "publish drafts", "submit review" | 3 |
| "fix finding 2 locally" | 2 — local fix |
| "review and draft all" | 1 then 2 |

If ambiguous, ask: preview only, draft selected findings, or publish existing drafts.

## Related skills

- `super-noslop`: run the noslop pass on the diff.
- `super-verify`: check a review comment before you act on it.
- `super-refactor`: apply a requested change without changing behavior.
- `write-mr-description`: the diff is clean and you need the MR text.
- `polyglot-copywriter`: polish review comments.
