---
name: second-opinion
description: "Adversarial read-only review of a diff, branch or named files that drives every open decision to a commitment. It restates the change and confirms it, then turns the brief, the reviewers' questions and every open finding into one decision tree and resolves it in dependency order: explore first, then exactly one question per node, each with a recommended answer. Independent reviewers on different models challenge the change through what-to-check lenses and a code-quality lens, and it buckets findings into Act on, Consider, Noted or Dismissed. Exits only when zero nodes are open, with a decision ledger, and offers CONTEXT.md terms and decision records. Quick triage first. Uses codebase-learner for context and why before removing a guard. Never applies fixes. Use for 'second opinion', 'interrogate', 'adversarial review', 'challenge this code', 'find blind spots', or 'what did I miss' before merge. Not for the routine MR review loop (code-review) or a plan or doc (challenge-me)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: knowledge
  category: knowledge
  department: knowledge
  related_skills:
    - verify
    - code-review
    - evidence
    - rumbling
  invokes:
    - skill: verify
      when: Each fix from review needs evidence
  tags:
    - review
    - adversarial
  capabilities:
    - blind_spot_review
  languages:
    - en

---

# Second opinion

Spawn independent reviewers to adversarially review a code change, then drive every open decision about it to a commitment with the author. The adversarial signal comes from model diversity, not assigned personas. The deliverable is a **decision ledger** with zero open nodes. Do NOT auto-apply changes.

How to open, pace and close the conversation is in [references/author-talk.md](references/author-talk.md). The node states, dependency order, ledger format and the two optional files are in [references/decision-tree.md](references/decision-tree.md). Read it before Step 2.

## How to ask

Ask **exactly one question per turn**, for one node:

```
Q3 (F2). <one question, one decision, binary or small multiple choice>
    Recommended: <answer>, because <one sentence from the code or the reviewers>
```

- Number questions across the whole review and name the node in brackets, so the user can answer "Q4: defer, after the launch".
- Use the host's question tool with one question (`AskUserQuestion` in Claude Code, the recommended option first). In `-p` mode or without the tool, ask in plain text with the shape above.
- Ready-made questions for every node type, and what makes a good one: [references/question-bank.md](references/question-bank.md).
- **Explore before asking.** If a quick read of the diff, `git log`, the PR or MR body, config, `CONTEXT.md` or an existing decision record answers the node, resolve it as `inferred: <path>` and do not ask.
- The user can confirm, pick another option, push back or defer. Pushback means: read the code again, then re-ask or change the recommendation. Defer means: mark the node DEFERRED with their reason.
- "Your call" resolves the current node with the recommendation (source `user (accepted recommendation)`) and moves on. It does not end the review.

## Step 0. Triage

Ask what you already know about the change and what is missing. A tiny change with a plain intent gets one quick pass from you, with no reviewers and no tree: say what you checked. An author who says "just run it" gets the reviewers with defaults stated in one line, and the ledger and the gate still apply. Everything else gets the full review. Then say how big the review is (small, standard or large) and let the author override it. Details: [author-talk.md](references/author-talk.md).

## Step 1. Gather (no questions yet)

Find what to review from context:

- If the user points at specific files or a diff, use that.
- On a feature branch, run `git diff <base>...HEAD` (usually `main`) for the full changeset, plus `git diff --stat` for its size.
- If the user's message refers to recent work, gather those files.
- Read the commit messages and the PR or MR body if one exists.

Package the diff or file contents with the surrounding context files reviewers need: types, callers, tests. [references/scope-and-context.md](references/scope-and-context.md) covers picking the base, large diffs, what to leave out and which context files to add.

**Context from `codebase-learner`.** If the change lands in a subsystem you do not already understand, run `codebase-learner` in **explain** mode on its simple path ("how does <the touched area> work?"). Put its How It Works and Gotchas sections into the reviewer prompt. Reviewers working from a bare diff miss call chains. Skip it for a small, self-contained change.

## Step 2. Restate and confirm (node N1)

Restate the change in one paragraph (about 150 words): what it does, for whom, and the goal it serves. Add what you found about how the touched area works today and what the change reaches, and flag a surprise (a hidden caller, a conflict, a cheaper path) if there is one. If the author did not ask for an interview, add one light line offering to just run the reviewers. Ask the user to confirm that this is the change being reviewed. **Do not go on with a wrong restatement.** If the user corrects it, restate again and re-confirm. Reviewers never question the intent, so it must be right first.

## Step 3. Resolve the brief (nodes N2 to N6)

Build the brief nodes from [decision-tree.md](references/decision-tree.md): scope, focus, risk, merge pressure, known gaps. Treat them as territory to cover, not a form to read out: build each question on the last answer or on what you found. After the brief, play it back in 100 to 200 words with your assumptions marked as yours ([author-talk.md](references/author-talk.md)). When looking further would help (callers, CI history, incidents), offer it and let the author decide. Create only the nodes that apply. Resolve them in dependency order, one question each, inferring every node the workspace already answers.

How the brief changes the review:

- Scope fixes what the reviewers see.
- Focus and known gaps go into the reviewer prompt, so deferred work is not reported as a finding.
- Risk and merge pressure set the bar in Step 6. A production hot path raises correctness and security findings toward Act on. A hotfix moves structural cleanup toward a follow-up.

## Step 4. Spawn reviewers

Launch all reviewers in one message, labeled Reviewer A, B and so on.

| Reviewer | Spawn | Model |
|---|---|---|
| A | `general-purpose` | omit `model` (the session model) |
| B | `general-purpose` | a different model from A: `sonnet` when the session runs on `opus`, otherwise `opus` |
| C (optional) | `security-reviewer` agent | the diff touches auth, PII, secrets, webhooks, spawned processes or external clients, or the brief named security |

Every brief says "do not edit files, commit or post anything". After the reviewers return, check that `git status` did not change.

**A non-Claude reviewer adds the most diversity.** If the user has another vendor's coding CLI installed and wants it, run it as one more reviewer in a read-only sandbox (for example `codex exec --sandbox read-only "<prompt>"`, after checking its `--help`). Never give it write access.

No subagents in this host? Do two separate passes yourself, one per lens order, and say the review had no model diversity.

Read `references/reviewer-prompt.md` and fill in the same template for every reviewer with the confirmed intent, the brief, the `codebase-learner` context if any, the diff or file contents, the lenses from `references/what-to-check.md`, the code-quality lens from `references/code-quality-review.md`, and the matching rows from [references/change-type-checks.md](references/change-type-checks.md) (migration, API contract, background job, …).

## Step 5. Synthesize, then resolve reviewer questions (nodes Q-n)

As results come back, build one picture with [references/synthesis.md](references/synthesis.md). Merge findings that describe the same issue in different words, and note which reviewers raised each. Findings two or more reviewers raised independently are the highest signal. Read a lone reviewer's finding, but weight it accordingly. Note disagreements: if one reviewer flags something and another explicitly says the opposite, that is context for the verdict.

Turn each reviewer's **Questions for the Author** into a Q-n node tied to the finding it affects. Merge duplicates. Resolve them before judging anything: infer from the code where you can, and ask the rest one at a time. An answer can open a new finding or dismiss one.

## Step 6. Lead judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. Read `references/judge-findings.md` for the full framework, and apply the risk and merge-pressure nodes.

**History check with `trace`.** Before you put a finding in Act on when it says to delete or loosen defensive code (a guard, retry, timeout, rate limit, feature flag, fallback), run the `trace` skill on that code. If the history shows the defense answers a real incident or constraint, the finding moves to Consider or Dismissed, with the citation. If nothing is found, say so and keep the finding where the evidence puts it.

Put every finding in one of four buckets, with the reviewer(s) that raised it and a one-line rationale:

- **Act on.** Real issues affecting correctness, security or maintainability given the actual goals. They would block a real PR.
- **Consider.** Legitimate, but you are not sure they outweigh the cost of fixing them now. Worth the user's attention.
- **Noted.** Technically valid but not actionable: context-dependent, premature optimization, or low impact at this stage.
- **Dismissed.** Wrong, nitpicky or missing context, with a brief reason.

Every Act on and Consider finding becomes an open F-n node.

## Step 7. Resolve the findings (nodes F-n and F-n.fix)

Show the buckets, then resolve each F-n node in order (Act on first), one question each:

| Finding | Ask | Recommend |
|---|---|---|
| Act on, one clear fix | "Fix now in this branch, or block the merge on it?" | fix now |
| Act on, several reasonable fixes | first F-n, then F-n.fix, which goes in a message of its own with a short trade-off table (what each fix gives up, when it wins): "Which fix: A <one line> or B <one line>?" | the smaller fix that removes the cause |
| Reviewers disagree, or the author says "that cannot happen" | offer a throwaway check (a failing test in a scratch copy, a one-off script), then go back to the node | what the check shows |
| Consider | "Fix now, follow-up, or leave it?" | from the risk and merge-pressure nodes |
| The user pushes back | "Is <the reviewer's assumption> wrong here? If yes, I dismiss it." | what the code shows |

More than six F-n nodes open? Ask one question first: "Go one at a time, or take my recommendation on every Consider finding and only raise the ones you disagree with?" Recommend one at a time for Act on.

**Exit only when zero nodes are open.** DEFERRED nodes do not block the exit. Then ask one closing question: "Hand the 'fix now' items to `tdd` (or `safe-refactor` for structure-only fixes) now?" Still apply nothing yourself.

If the user stops answering, deliver the ledger with the remaining nodes marked open. Do not call the review done.

**Play back the buckets** before the first F-n question: 100 to 200 words on what the review found, with anything you assumed marked as yours.

**Cold read (large reviews).** When the review is large or the ledger will leave this chat, give the output contract to a fresh reader before you hand it over. Sort their questions into answered, minor and the author's, and ask only the author's, in one message. Steps and prompt: [references/cold-read.md](references/cold-read.md).

**The gate.** Nothing in the reviewed change is edited until the author approves the ledger. The "fix now" items go to `tdd` or `safe-refactor` after that yes.

## Step 8. Offer the files

Following [decision-tree.md](references/decision-tree.md), offer, and write only after a yes:

- **CONTEXT.md**, when the review pinned down project-specific terms. Merge in place, never overwrite.
- **Decision records**, one per contested or hard-to-reverse node, numbered from the highest existing record in the repo's decision folder.

## Output contract

A full run, from restatement to ledger, is in [references/worked-example.md](references/worked-example.md).

Short and pasteable. No prose summary. No hedging.

```markdown
### Change
> [The confirmed one-paragraph restatement]

### Reviewers
- Reviewer A: <agent, model>, N findings
- Reviewer B: <agent, model>, N findings

### Findings
- Act on: F1 <one line> (A, B)
- Consider: F3 <one line> (B)
- Noted: <one line each>
- Dismissed: <one line each, with the reason>

### Decision ledger
- <Decision> - <Choice> - <user | inferred: <path> | DEFERRED: <reason>>

### Agreement map
- <where reviewers agreed or split, one line each; name any codebase-learner or why run and what it changed>

### Files written
- <path>, or "none"
```

## References

| File | Use it for |
|---|---|
| [author-talk.md](references/author-talk.md) | Triage, the first message, asking by territory, play-backs, recon offers, fix trade-offs, throwaway checks, sizing, the gate, red flags |
| [cold-read.md](references/cold-read.md) | A fresh reader checks that the ledger stands on its own |
| [decision-tree.md](references/decision-tree.md) | Node states, dependencies, the resolve loop, the ledger, `CONTEXT.md` and decision records |
| [question-bank.md](references/question-bank.md) | Ready-made questions per node, and good versus bad questions |
| [scope-and-context.md](references/scope-and-context.md) | Base branch, diff size, exclusions, context files, filling `{BRIEF}` |
| [reviewer-prompt.md](references/reviewer-prompt.md) | The prompt every reviewer gets |
| [what-to-check.md](references/what-to-check.md) | Correctness, root cause, structure, verification, complexity, security |
| [code-quality-review.md](references/code-quality-review.md) | The strict code-quality lens and approval bar |
| [change-type-checks.md](references/change-type-checks.md) | Extra checks per kind of change, linked to levistack rules |
| [synthesis.md](references/synthesis.md) | Merging findings, weighting agreement, disagreements, severity |
| [judge-findings.md](references/judge-findings.md) | Filters for bucketing, and how the brief moves the bar |
| [worked-example.md](references/worked-example.md) | One made-up review from start to ledger |

## Anti-patterns

- **Several questions at once.** The user loses context, and you lose the chance to react to each answer.
- **Asking before exploring.** If a quick read answers the node, read first.
- **A question without a recommendation.** That is a survey. It hands the design back to the user.
- **Rolling past an open node.** If a dependency is not pinned, the downstream question is premature.
- **Applying patches "to be helpful".** The user decides. `tdd` or `safe-refactor` does the fix, and `verify` proves it.
- **Treating one reviewer's nit as Act on** without context.
- **Running it on a plan or doc.** That is `challenge-me`.
- **Reading the brief out like a form.** Cover the ground in conversation, built on the last answer.
- **Keeping a throwaway check.** It was only there to settle a node. Keeping it is a new request.

## Related skills

- `codebase-learner`: context for reviewers when the change lands in unfamiliar code.
- `trace`: the history behind a guard a finding wants to remove.
- `challenge-me`: the same decision walk for a plan, doc or design instead of code. It shares the `CONTEXT.md` and decision-record files.
- `code-review`: the normal review loop, posting MR notes, or acting on review comments.
- `tdd` or `safe-refactor`: carry out the "fix now" decisions.
- `verify`: prove each fix after it lands.
- `evidence`: read-only Judge mode checks the final artifact and claimed proof, including a completed parallel batch. It does not drive this skill's author decision ledger.
- `rumbling`: coordinate multiple independent tasks, competing artifacts, or a judgment council; call this skill only when the code-change decision itself needs adversarial review.
- `noslop`: the findings are mostly slop (generic errors, filler comments, N+1).
