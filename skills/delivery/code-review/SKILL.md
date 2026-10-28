---
name: code-review
description: "Review local diffs, committed ranges, and GitLab merge requests; verify feedback before applying fixes and prepare inline comments for explicit publication. Use when asked to review code, review an MR, check a branch before merge, address review threads, or draft review feedback. Not for an adversarial two-reviewer verdict (second-opinion) or remote GitHub PR posting."
context: fork
metadata:
  version: 1.1.1
  author: levistack
  license: MIT
  group: delivery
  category: delivery
  department: delivery
  related_skills:
    - noslop
    - polyglot-copywriter
    - verify
    - write-mr-description
  invokes:
    - skill: noslop
      when: Comment bodies need slop pass on code surfaces
    - skill: polyglot-copywriter
      when: Review comment prose needs polish
    - skill: verify
      when: Acting on each review comment
  tags:
    - code-review
    - gitlab
    - mr
    - local-diff
    - review-feedback
  capabilities:
    - local_diff_review
    - merge_request_review
    - review_feedback
    - draft_inline_comments
  languages:
    - en

---

# Code review

Pick the mode from the user's goal. A review request starts read-only. Local fixes, draft notes, public comments, approvals, commits, pushes, and thread resolution are separate actions. Do only the actions the user authorized.

| Goal | Mode | Detail |
|------|------|--------|
| Review **uncommitted / staged** changes before a PR | **Diff** | [references/review-diff.md](references/review-diff.md) |
| Review **your** commits before merge / next task | **Request** | [references/requesting-review.md](references/requesting-review.md), template [references/code-reviewer.md](references/code-reviewer.md) |
| **Implement** feedback from a human or external reviewer | **Receive** | [references/receiving-review.md](references/receiving-review.md) |
| Review a GitLab MR or its open threads | **GitLab MR** | Below + [references/draft-review-flow.md](references/draft-review-flow.md) |

For comment text, use [`noslop`](../../engineering/noslop/SKILL.md) and `polyglot-copywriter` while preserving code and exact line anchors.

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

## GitLab MR review

Three phases: **preview** (read-only), **draft to MR** (unpublished GitLab draft notes, explicitly requested), then **publish** (explicitly requested). A request to fix findings locally goes through the [feedback workflow](references/receiving-review.md) after preview; it does not imply posting or pushing.

**Default write path:** GitLab **draft notes** (`draft_notes` API / bundled scripts). Author sees nothing until publish.

**Comment shape:** inline findings with **code suggestions** on diff lines — not a wall-of-text MR summary.

Operator reference: [references/gitlab-mechanics.md](references/gitlab-mechanics.md), [references/draft-review-flow.md](references/draft-review-flow.md), [references/review-dimensions.md](references/review-dimensions.md), [references/comment-body-format.md](references/comment-body-format.md). For a risky change or requested deeper pass, use [references/deep-review.md](references/deep-review.md). Use [references/detailed-report.md](references/detailed-report.md) only when a longer report is requested.

Before using a bundled helper, set `REVIEW_SKILL_DIR` to the absolute directory containing this `SKILL.md`. Call `"$REVIEW_SKILL_DIR/scripts/<helper>.sh"`; a bare `scripts/` path in the target repository may execute the wrong file.

### Phase 1: Deep read-only preview

1. Resolve the MR by URL, project and IID, or current branch. If several MRs match, show the choices instead of guessing. Fetch its metadata, entire diff, open discussions, pipeline status, and failing job traces.
2. Read relevant source, tests, and contracts at the MR head SHA. Avoid switching branches over unrelated work. Verify each finding against the target file and diff line. Run focused tests when a safe checkout or equivalent is available; separate CI evidence from local runs.
3. Apply [references/review-dimensions.md](references/review-dimensions.md). For changed behavior, map the branch to a test example and an observable assertion, or mark the gap. Use the optional deep pass for risk that needs another review lens.
4. Write findings by severity with file and line, impact, evidence, and a proposed fix. Add a GitLab suggestion fence only when the replacement exactly fits the diff range. List existing open threads so the preview does not duplicate them. State CI evidence and what was not verified.
5. Present the preview. If the user asked only for review, stop. If the user already requested a local fix or selected draft notes, continue with that authorized action. Even a clean preview does not authorize approval or publication.

### Phase 2: Draft to MR (explicit request)

Draft only the selected, reviewable findings. Use [GitLab mechanics](references/gitlab-mechanics.md) to refresh diff SHAs and write comment bodies to files. Prefer inline drafts; a finding outside the diff becomes a general draft note. Verify pending draft notes after posting. Tell the user these notes remain unpublished. Do not treat a generic "ok" as approval to post, publish, or approve.

### Phase 3: Publish drafts (explicit request)

Only after the user explicitly requests publication of the identified drafts:

```bash
export REVIEWER_STATE=requested_changes   # or reviewed for comment-only
export SUMMARY_FILE=
"$REVIEW_SKILL_DIR/scripts/publish-draft-notes.sh" <repo> "$PROJECT_ID" <number>
```

Never set `reviewer_state=approved` from automation. Publish only the intended drafts. Immediate public inline comments require an explicit request identifying the selected findings and public posting. A clean review remains a read-only result unless the user separately authorizes a forge action.

### GitLab quick routing

| User says | Phase |
|-----------|-------|
| "review MR", "review !123" | 1 |
| "draft 1,3", "post as draft" | 2, after the preview |
| "publish drafts", "submit review" | 3 |
| "fix finding 2 locally" | Local feedback workflow after preview |
| "review and draft all" | 1 then 2 |

For "fix all open threads", inspect each thread and current code, then apply only supported fixes. Verify before marking a thread addressed. A commit link must resolve on the remote before posting it; a local commit is insufficient. Keep advisory or blocked threads open. See [GitLab mechanics](references/gitlab-mechanics.md). A GitHub PR URL does not use the GitLab adapter.

## Related skills

- `noslop`: run the noslop pass on the diff.
- `second-opinion`: the user wants an adversarial, two-reviewer verdict rather than the review loop.
- `verify`: check a review comment before you act on it.
- `safe-refactor`: apply a requested change without changing behavior.
- `write-mr-description`: the diff is clean and you need the MR text.
- `polyglot-copywriter`: polish review comments.
