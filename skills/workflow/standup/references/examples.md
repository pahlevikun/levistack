# Examples

Fictional projects and people. Match the voice, not the content. Each example notes which sources produced the lines, because that is the habit to copy: every bullet traces back to something collected.

## 1. Regular day (Tuesday to Friday)

```markdown
# Standup: Thursday, 8 Oct 2026

## What I worked on (yesterday, 2026-10-07)
- Most of the day on the retry logic for the upload service (ABC-212). Pulled the backoff into its own helper because the old version retried on 4xx too, which was the actual bug. MR is up.
- Reviewed Sam's MR on the invoice export (!342). Approved with one nit about test coverage.
- Short sync with Priya on how the new settings page registers its sections. We're going with the provider pattern.

## Today
-

## Tickets
- **[ABC-212]** Retry flaky uploads: In Progress → In Review, MR !351
- **[ABC-198]** Invoice export timeout: Done, merged yesterday

## Reviews
- !342 `billing-service`: invoice export refactor, approved
- !189 `web-app`: settings section registry, left 2 comments

## Blockers
- nothing blocking atm
```

Sources: commits and an AI session on the upload service (machine), `!351` opened and `!342` approved (forge), status changes (Jira), the sync's calendar title and notes (Lark).

## 2. Monday (window is Friday to Sunday)

```markdown
# Standup: Monday, 12 Oct 2026

## What I worked on (Fri 2026-10-09 – Sun 2026-10-11)
- Friday was wrapping up the retry work: tests green, pushed for review, then the weekly retro in the afternoon (nothing big came out of it).
- Nothing over the weekend apart from a small fixture fix on Saturday morning.

## Today
-

## Tickets
- **[ABC-212]** Retry flaky uploads: In Review, waiting on feedback
- **[ABC-260]** Test fixture cleanup: Done

## Reviews
- !350 `web-app`: add client retries, approved Friday

## Blockers
- need Sam to look at !351 before I can start the next piece; pinged him Friday, following up today
```

The Saturday commit came from the machine step; the weekend has one line because that is all there was.

## 3. After a holiday

```markdown
# Standup: Wednesday, 14 Oct 2026

## What I worked on (Fri 2026-10-09 – Tue 2026-10-13)
- Friday: got the database migration in for the new preferences table and registered the provider. Reviewed two MRs before logging off, one approved, one with a question about error handling.
- Mon and Tue were a holiday and a bridge day, offline.

## Today
-

## Tickets
- **[ABC-270]** Preferences provider: In Progress, migration done, service layer next
- **[ABC-212]** Retry flaky uploads: merged while I was away

## Reviews
- !355 `web-app`: update client timeout config, approved
- !192 `billing-service`: user delete edge case, commented on error handling

## Blockers
- need to confirm the new auth response format with the platform team, it changed while I was out
```

Needs `holidays` in the config (or the user saying so); otherwise the window would have started on Monday.

## 4. Meeting-heavy day

```markdown
# Standup: Friday, 9 Oct 2026

## What I worked on (yesterday, 2026-10-08)
- Honestly not much code. Sprint planning in the morning, then a deep dive with the platform team on the archive flow.
- After lunch I squeezed in two MR reviews and updated the design doc for scoped authorization with what came out of the deep dive (we're dropping the per-request lookup).
- Also helped debug a production timeout: the client's circuit breaker was too aggressive. Config change is out.

## Today
-

## Tickets
- **[ABC-234]** Scoped authorization: In Progress, design doc updated after the meeting
- **[ABC-250]** Client timeout config: Done

## Reviews
- !156 `web-app`: partner client retry logic, requested changes (missing error wrapping)

## Blockers
- waiting on the platform team to confirm the new API contract before I can start the integration layer, expecting an answer today or tomorrow
```

Sources: calendar titles and meeting notes (Lark) supply "what came out of it"; the doc edit (Lark drive search) supplies the design-doc bullet.

## 5. Quiet day

```markdown
# Standup: Tuesday, 6 Oct 2026

## What I worked on (yesterday, 2026-10-05)
- Half day, errands in the morning. Caught up on threads after lunch and reviewed one MR.

## Today
-

## Tickets
- **[ABC-234]** Scoped authorization: In Progress, no movement

## Reviews
- !342 `billing-service`: card group repo refactor, approved

## Blockers
- none, picking the auth work back up today
```

A quiet day gets a short standup. Do not pad it.

## 6. Investigation with no commits

```markdown
# Standup: Wednesday, 7 Oct 2026

## What I worked on (yesterday, 2026-10-06)
- Chased a memory growth issue in the worker. No code yet, but I narrowed it to the batch loader keeping every page in memory. Written up on the ticket with the dashboards I used.
- Reviewed two MRs.

## Today
-

## Tickets
- **[ABC-281]** Worker memory growth: In Progress, root cause found, fix next

## Reviews
- !360 `web-app`: fix nil pointer in enrichment, approved
- !361 `web-app`: log level cleanup, approved

## Blockers
- nothing blocking
```

Sources: browser history (dashboards, the ticket, profiler docs), a Jira comment, no commits. This is the day browser history exists for. "Narrowed it to" is fine because the ticket comment says so; "fixed" would not be.

## What bad looks like

> Yesterday, I diligently worked on implementing retry logic as specified in ABC-212. I conducted a thorough refactoring of the backoff component to address deficiencies. Additionally, I performed a comprehensive review of a merge request.

Too formal, no specifics, and "comprehensive" and "thorough" are not evidence. Compare with example 1.
