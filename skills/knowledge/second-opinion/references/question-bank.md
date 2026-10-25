# Question bank

Ready-made questions for each node in `decision-tree.md`. Fill in the brackets from the code. Each question has one decision, a recommended answer and one sentence of reasoning.

Before you ask any of them, check the "Infer from" column. If that source answers the node, mark it `inferred: <path>` and do not ask.

## Brief nodes

| Node | Question | Recommended answer comes from | Infer from (skip the question) |
|---|---|---|---|
| N1 Intent | "Is this the change: [one paragraph]?" | commits, PR body, the diff | the user's message or the PR body states the goal in their own words. Still restate it, and ask only "Right?" |
| N2 Scope | "Review `[base]...HEAD`, [N] files, +[A]/-[D] lines, without [generated files]?" | `git diff --stat`, the merge base | the user named the files or the diff |
| N3 Focus | "Anything to weight or skip: [security / performance / file X / tests]?" | the riskiest area in the diff | the user's message already names a focus |
| N4 Risk | "Where does this run: [production hot path / behind flag F / internal tool / one-off script]?" | entry points, flags, config | a flag guards it, or the path is clearly a script or a test |
| N5 Merge pressure | "Must this merge soon ([hotfix / deadline]), or can it wait for a cleaner fix?" | branch name, commit words like "hotfix" or "revert" | the branch or the PR says hotfix |
| N6 Known gaps | "Anything already deferred: [tests / docs / a follow-up PR]?" | TODOs in the diff, the PR body | the PR body has a "follow-up" or "not in this PR" list |

## Reviewer question nodes (Q-n)

Rewrite the reviewer's question so the author can answer it in one line, and name the finding it decides:

| Reviewer wrote | Ask the author |
|---|---|
| "Unclear whether `userId` can be null here" | "Q[n] (F[k]). Can `userId` be null when [the cron job] calls `[fn]`? Recommended: no, because [the job filters it at file:line]." |
| "Is the 500-item limit intended?" | "Q[n] (F[k]). Is 500 the intended limit for [what]? Recommended: yes, because [it matches the upstream API limit in file:line]." |
| "Who else calls this endpoint?" | First search the repo. If nothing outside the repo is visible: "Q[n] (F[k]). Does anything outside this repo call `[endpoint]`? Recommended: no, because [no client in the repo uses it]." |

## Finding nodes (F-n)

| Finding | Question | Recommend |
|---|---|---|
| Act on, one clear fix | "Q[n] (F[k]). Fix [one line] now in this branch, or block the merge on it?" | fix now |
| Act on, several fixes | "Q[n] (F[k].fix). Which fix: A [one line] or B [one line]?" | the smaller fix that removes the cause, not the symptom |
| Consider | "Q[n] (F[k]). Fix [one line] now, in a follow-up, or leave it?" | follow-up under merge pressure, fix now when it can wait |
| User pushes back | "Q[n] (F[k]). Is [the reviewer's assumption] wrong here? If yes, I dismiss it." | what the code shows |
| Reviewers disagree | "Q[n] (F[k]). Reviewer A says [x], reviewer B says [y]. Which matches how this is used?" | the one the code supports, with the line |
| Bulk offer (more than six open) | "Q[n]. Go one at a time, or take my recommendation on every Consider finding and only raise the ones you disagree with?" | one at a time for Act on, bulk for Consider |

## Term nodes (T-n)

Ask when the review needs a project word pinned down:

- "Q[n] (T[k]). In this repo, does '[term]' mean [A] or [B]?" Recommended answer from how the code or `CONTEXT.md` uses it.
- "Q[n] (T[k]). The code says '[term1]' and the PR says '[term2]'. Same thing?" Recommend one name for both.

## What makes a good question

| Bad | Why | Good |
|---|---|---|
| "Any thoughts on error handling?" | No decision, no stance | "Q4 (F2). Return 409 or 422 when the export already exists? Recommended: 409, because the other create endpoints in `api/` use it." |
| "Is this safe and fast and tested?" | Three decisions in one | Three questions, asked one at a time |
| "Should we refactor this?" | Asked before reading the code | Read the callers first, then ask about the one concrete change |
| "What do you want to do about F3?" | No recommendation, hands the design back | "Q6 (F3). Follow-up or leave it? Recommended: follow-up, because this is a hotfix." |
