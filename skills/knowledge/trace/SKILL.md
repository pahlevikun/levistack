---
name: trace
description: "Trace why, with evidence on every step. Two modes. Rationale: why code is shaped this way, what tradeoff or incident produced a guard, retry, flag or threshold, from git, PRs, tickets, docs, chat and monitoring. Root cause: Five Whys from a symptom (a bug, an incident, a flaky pipeline, a slow deploy) down to the systemic cause, with branches for split causes. Every link is cited and tiered (direct, supported, inferred, speculative), then double-checked: backward read, counterfactual, falsification, timeline, a competing chain, and the human-error rule. Proposes fixes for root causes, never applies them. Read-only. Use for 'why does X work this way', 'why did we pick Y', 'is this guard still needed', 'why did this happen', 'root cause', 'five whys', 'postmortem', or 'why does this keep failing'. Not for how code runs today (codebase-learner), or reproducing a live failure's mechanism (verify)."
---

# Trace

Trace a "why" to its source, and prove every step. Code shows what it does, not why it exists or why it broke. The why lives in commits, PRs, tickets, docs, chat, logs and dashboards, and all of them are partial. This skill gathers that evidence, builds the chain, and checks the chain before anyone acts on it.

The rationale mode is adapted from pstack's `why` (MIT, Lauren Tan).

## Pick the mode

| The user asks… | Mode | Load |
|---|---|---|
| Why is the code like this, why did we pick Y, what tradeoff, where did this number come from, is this guard still needed | **rationale** | [epistemics.md](references/epistemics.md), [investigator-prompt.md](references/investigator-prompt.md), [synthesizer-prompt.md](references/synthesizer-prompt.md) |
| Why did this happen, root cause, five whys, postmortem, why does this keep failing, why is this slow | **root-cause** | [root-cause.md](references/root-cause.md), [cause-checks.md](references/cause-checks.md), [epistemics.md](references/epistemics.md), examples in [root-cause-examples.md](references/root-cause-examples.md) |
| An incident hit defensive code, or a fix wants to remove a guard | **root-cause, then rationale** | both. Finish the cause chain, then trace why the guard existed before anyone deletes it |

If the words fit both, ask one question: "Q1. Do you want why the code is shaped this way, or why this problem happened? Recommended: <the one the message leans toward>."

## Hard rules (both modes)

1. **Read-only.** Do not change code, data or external systems. Investigators and the synthesizer get the same rule in their brief. Check `git status` after they return.
2. **Every claim has a tier.** Direct, Supported, Inferred, Speculative or Unknown, from [epistemics.md](references/epistemics.md). The tier sets the wording.
3. **Code is not evidence of its own intent.** "It retries three times, so the author wanted three retries" is mechanics, not motivation.
4. **Document the null.** An empty search is a finding. Name what was searched.
5. **The user's guess is a candidate.** Check it like any other hypothesis.
6. **Double-check before you conclude.** Run [cause-checks.md](references/cause-checks.md) on every chain, and its backward-read, counterfactual and timeline checks on every rationale claim marked Supported or higher.

## Subagents

| Role | Spawn | Model |
|---|---|---|
| Investigator (one per evidence category) | `general-purpose` | omit `model` to use the session model, or `sonnet` for a cheap source |
| Synthesizer | `general-purpose` | `opus` |
| Live reproduction (root-cause, Why 1 not confirmed) | run `verify` in investigate-first mode | session model |

Use `general-purpose`, not a read-only agent such as `explorer`. Investigators and the synthesizer need the session's MCP servers. Every brief says "do not write files, commit, post, or change external state".

No subagents in this host? Run each investigation yourself, one source at a time, then synthesize with the same template.

## Step 1. Understand the target and the question

**Rationale:** the target is a chunk of code, a pattern, a feature or a named decision. The question is a rationale, a tradeoff, a motivating edge case, an external constraint, dead code, or a history sweep.

**Root cause:** the target is a symptom. Write the problem block from [root-cause.md](references/root-cause.md): what, where, when, impact, evidence.

If the target is vague, make your best guess from the conversation, state it in one line so the user can redirect, and go on.

## Step 2. Establish the anchor

Build the seed context yourself before spawning anyone.

**Code anchor (both modes):** file paths and line ranges, key symbols, the commits that touched them, PR or MR numbers and ticket ids.

```bash
git blame -w -C -L <start>,<end> <file>    # last-touch commits, through moves
git log --follow -p -- <file>              # full history through renames
git log -S '<exact string>' -- <file>      # commits that added or removed it
git log --format='%h %ad %s' --date=iso -- <file>   # dated history for the timeline check
gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews
glab mr view <number> --comments           # GitLab
```

**Incident anchor (root cause):** first-seen time, deploys and config changes in the window before it, the error group or alert id, and the incident doc or channel.

This anchor goes to every investigator and to the synthesizer.

## Step 3. Spawn parallel investigators

**Default to the full parallel investigation.** The goal is a complete coverage map, not a minimal one.

### Discovery

List the MCP servers this session can use. In Claude Code they are tools named `mcp__<server>__<tool>`, loaded or listed as deferred tools. A server the session reports as "failed to connect" counts as unavailable: name it as a gap, and tell the user it failed to connect.

Map each available server to one evidence category:

1. Source control history (always available through git and `gh` or `glab`)
2. Issue or ticket tracker
3. Long-form documents (inline docs in the repo are always available)
4. Real-time team chat
5. Infrastructure observability
6. Error or exception tracking
7. Product analytics warehouse
8. Deploy and CI history
9. Runtime platform (cluster state, config, feature flags)
10. Live data (databases, event streams, read-only API calls)
11. Customers and support

Not every category needs an MCP server. Some are reached with a CLI the user already has (`kubectl`, `glab`, `gcloud`, `psql`). Check that the CLI exists and is logged in before you count the category as available. **Categories 9 and 10 touch running systems:** confirm the environment, and ask the user before you query production.

Spawn one investigator per category that has a matching server, all in one message, each owning exactly one source. Each prompt is [investigator-prompt.md](references/investigator-prompt.md) filled in, plus:

- the playbook for the tool it owns, `references/sources/<tool>.md`, picked from the index in `references/source-playbook.md` (25 playbooks across the 11 categories). Two tools in one category get two investigators.
- `references/sources/incident-postmortem.md` when the target looks defensive, and always in root-cause mode
- the anchor and the user's question
- in root-cause mode, the current chain so far, so the investigator looks for evidence for or against each link

### What each category is best at

1. **Source control** (git, GitHub PRs, GitLab MRs): rationale captured in review. The commit that introduced a bug. Always spawn.
2. **Issue or ticket tracker** (Jira, Linear, GitHub or GitLab issues): the product or business forcing function. The bug report and its history.
3. **Long-form documents** (Confluence, Google Docs, Notion, Lark Docs, inline docs and ADRs): design rationale written before the code. Postmortems. Runbooks.
4. **Real-time team chat** (Slack, Lark): decisions that never reached a doc. What people saw during an incident.
5. **Infrastructure observability** (Grafana, Datadog, logs): the runtime reality: latency, saturation, the incident timeline, the first error line.
6. **Error or exception tracking** (Sentry and similar): the exact exceptions, their first-seen time and their spread.
7. **Product analytics warehouse** (BigQuery, Snowflake, MaxCompute, Databricks): the data behind thresholds, flags and experiments. How many users were hit.
8. **Deploy and CI history** (pipelines, Argo CD, release tags): when the code really shipped, and what else shipped with it. The backbone of the timeline check.
9. **Runtime platform** (kubectl, Lens, k9s, flag services, config stores): restarts, OOM kills, rollout revisions, a flag flipped with no deploy.
10. **Live data** (databases, Kafka and queues, read-only API calls): the actual state of records, lag, dead letters. Ask first.
11. **Customers and support** (Zendesk, Salesforce, support queues in Lark Base): the first report and the real impact, often before any alert.

### When to skip an investigator

Only with a written reason that goes into Sources consulted: no server for that category is available (a gap, not a choice), or the source is provably irrelevant, not just probably.

## Step 4. Analyze

### Rationale mode

Spawn one synthesizer with every investigator's findings (empty and skipped ones too), the anchor, the question, [epistemics.md](references/epistemics.md) and [synthesizer-prompt.md](references/synthesizer-prompt.md). Ask it for two extra parts:

- **Decision timeline:** each shaping commit, PR, ticket or incident in date order, so accretion is visible.
- **Forces:** the constraints behind the shape, grouped as product, data, infrastructure, team or process, and external (a partner, a law, a library).

Then double-check the synthesis yourself: for each Supported or Direct claim, run the backward read, the counterfactual ("would this code exist without that force?") and the timeline check from [cause-checks.md](references/cause-checks.md). Downgrade any claim that fails.

### Root-cause mode

Follow [root-cause.md](references/root-cause.md):

1. Pin Why 1 with proof. A live failure with no confirmed mechanism goes to `verify` (investigate-first) first.
2. Build the chain, one link per why, each with evidence and a tier. `DEPTH` defaults to 5 but is a guide.
3. Branch when a why has more than one cause. Mark causes as necessary, independent or contributing.
4. Run every check in [cause-checks.md](references/cause-checks.md) on every chain: backward read, counterfactual, falsification, timeline, competing chain, human-error rule, scope.
5. Stop at a systemic cause in the team's control: missing validation, docs, process, automation, test or alert. Never at "human error", "a third party failed" or "bad luck".
6. Propose a fix per root cause, with containment labeled separately, how to verify, and what to watch for recurrence.

A synthesizer is optional here. Spawn one when four or more investigators returned, and give it [root-cause.md](references/root-cause.md) as the output template.

## Step 5. Present

Present the result. You may edit lightly for clarity, but **do not rewrite the confidence language**.

- **Rationale:** the structure in [synthesizer-prompt.md](references/synthesizer-prompt.md): The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, Confidence Summary. Add the Decision timeline and Forces. If the user will change this code next, end with a **Preserve / Change / Avoid / Risk** set.
- **Root cause:** the output block in [root-cause.md](references/root-cause.md): Problem, Cause chain, Root cause(s), Checks, Fixes, What we don't know, Sources consulted.

## Common failure modes

- **Recency bias.** Treating the latest commit as the whole story. The current shape is often many decisions stacked up.
- **Stopping at a symptom.** "Missing index" is a detail. Why could it ship?
- **One cause for a split problem.** If the counterfactual fails, there is another branch.
- **A tidy story over the evidence.** If two sources disagree, both stay in the output.
- **Blaming a person.** Human error is where the digging starts, not where it ends.
- **Deleting a guard because no reason was found.** Report it as unknown. The user decides.

## Related skills

- `codebase-learner`: the user needs how the code runs today, not why.
- `verify`: reproduce and confirm the mechanism of a live failure (Why 1) before the chain.
- `second-opinion`: the history explains a guard a reviewer wants to remove.
- `tdd` or `safe-refactor`: carry out a root-cause fix the user chose.
- `execution-ready-spec-plan`: the constraints are known and the change needs a plan.
- `challenge-me`: the user wants to test whether an old decision still holds.
