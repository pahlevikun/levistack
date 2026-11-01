# Review an initiative or team delivery

Use this mode for a **multi-artifact retrospective**: an epic, initiative, milestone, release train, or sprint theme that spans tickets, people, and pull requests.

Session mode covers one agent conversation. Artifact mode covers one ticket or branch. Initiative mode connects several artifacts into one timeline and one set of team-level lessons.

## Bound the initiative

Record:

- Initiative name or goal in the user's words.
- Time window and repositories in scope.
- Included artifacts: epics, tickets, PRs, releases, docs, or runbooks the user lists.
- Participants or roles only when they appear in cited evidence (no invented ownership).

Read authorized tracker and git sources read-only. Do not assign work, change status, or post retrospective notes unless the user explicitly asks outside this skill's proposal-only contract.

## Build the initiative timeline

Merge artifact-level facts into one ordered timeline. Prefer links and IDs over narrative.

| Phase | What to capture |
|---|---|
| Kickoff | Stated goal, constraints, and baseline |
| Execution | Merged work grouped by theme, not only by date |
| Integration | Cross-team dependencies, env promotions, flag flips |
| Finish or pause | What shipped, what slipped, what was descoped |

For each milestone entry, cite at least one primary source (merge commit, release tag, ticket transition, review approval).

When an artifact has enough detail, you may reuse the delivery-record shape from artifact mode as a subsection. Do not duplicate full diffs for every ticket.

## Run a team retrospective lens

After the timeline is factual, inspect these initiative categories. An empty category needs no finding.

| Category | Look for |
|---|---|
| Scope | Creep, hidden dependencies, or unclear "done" |
| Coordination | Handoffs, waiting on review, duplicate work across tickets |
| Quality | Defects or rework that crossed artifact boundaries |
| Flow | Batch size, WIP, or integration pain |
| Observability | Missing metrics or signals until late |
| Knowledge | Onboarding cost, tribal docs, or repeated explanations |
| Environment | Shared staging, data, or machine facts that blocked multiple people |

Team agreement in a meeting is one data point, not recurrence. Two **independent episodes** on the initiative still gate supported durable lessons.

## Proposals at initiative strength

Walk the same fix ladder as repo mode. Prefer changes that help the **next initiative**, not only this one:

- Architecture or platform work when the same dependency blocked multiple streams.
- Types or contracts when integration broke at boundaries.
- CI or lint when the same check failed on several PRs.
- Behavior tests when regressions escaped review repeatedly.
- Prose in playbooks, skills, or review guidance when judgment was the bottleneck.

Each proposal names the **concrete home** (repo path, template, CI job, or authoring skill target). Initiative mode does not authorize implementing them.

## Return shape

1. **Initiative timeline** with citations.
2. **Themes** (optional short bullets grouping events; must trace to timeline entries).
3. **Supported proposals**, **open leads**, and **rejected** per synthesis (after the review views in `SKILL.md`).
4. For repo-wide enforcement, include the rule table from repo mode when at least one class qualifies.

Offer `standup` only when the user wanted a personal yesterday summary instead of an initiative lookback.
