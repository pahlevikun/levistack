---
name: refresh-pr
description: "Decide what an aging pull request or merge request should become: refresh it onto the current base, rework it because the intent stands and the diff does not, or close it because the change is obsolete. Shows the classification and a before/after comparison, then stops for a yes before rewriting history, pushing, or closing. After a refresh, hands the review loop to code-review watch or prep. Use when asked to refresh a stale PR or MR, rebase an old request, or decide whether an aging request should still exist. Not for a first review of a current branch (code-review) or for merging."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: delivery
  category: delivery
  department: delivery
  related_skills:
    - code-review
    - verify
    - use-levistack
    - write-mr-description
  invokes:
    - skill: code-review
      when: A refresh the user accepted needs watch or prep
  tags:
    - pull-request
    - merge-request
    - stale
    - rebase
  capabilities:
    - stale_request_decision
    - refresh_then_review
  languages:
    - en

---

# Refresh a request

An old pull request or merge request is not automatically still the right change. Decide what it should become, show the evidence, and stop before any rewrite, push, or close.

## Steps

1. **Read both sides.** Identify the request, its base, and its head. Read the diff and the commits since the request opened. Note required checks and open threads. Use the host the URL or the remote names: GitLab with `glab`, GitHub with `gh`.
2. **Classify.**
   - **Refresh.** The change is still wanted, and it can sit on the current base. The work is a rebase or a merge of the base, then a comparison of the old head and the new head.
   - **Rework.** The intent is still wanted, and the diff is not. Name what must be rewritten. Do not start that rewrite here. Hand it to `use-levistack` as a feature or bug-fix once the user agrees.
   - **Close.** The change is obsolete: the base already has it, the product no longer needs it, or it conflicts with a decision made since the request opened. Say which.
3. **Show the evidence.** State the classification, the reason, and a before/after comparison (a range-diff, or the files that differ between the old head and the rebased result when a range-diff is not available). For a close, quote the commit or the file that made the request obsolete.
4. **Stop for a yes** before rewriting history, force-updating a branch, pushing, or closing the request. A refresh that would discard commits the user did not author stops even if they already said to refresh. Say whose commits those are.
5. **Hand off the loop.** After a refresh the user accepted, invoke `code-review`. Use **watch** when they said to watch it or stay with it. Use **prep** when they said to get it merge-ready. When they named neither, use watch.

## Output

The classification, the reason, the comparison, and whether you are waiting or which `code-review` mode is running.

## Related skills

- `code-review`: the review loop after a refresh, in watch or prep.
- `verify`: the checks the comparison depends on.
- `use-levistack`: a rework that is really a new feature or bug-fix.
- `write-mr-description`: the request text is stale after a refresh the user asked to update.

## Done when

- The request is classified with a reason and a comparison, or marked close with the evidence.
- No history was rewritten, and nothing was pushed or closed, without a yes.
- A refresh the user accepted is in `code-review` watch or prep.
- [evals/evals.json](evals/evals.json) covers a refresh, a close, and a plain review.
