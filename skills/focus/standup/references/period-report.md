# Report activity over a selected period

Use this optional mode for a sprint, month, development-plan update or other
explicit date window. Keep daily standup defaults unchanged. Private source
adapters and personal identifiers remain in caller configuration, outside the skill.

1. Establish inclusive start/end dates, timezone, subject and audience. Reuse the
   existing source collectors with explicit bounds. Collect only sources the task
   authorizes; a period report does not authorize broad browsing or private messages.
2. Normalize selected evidence into a JSON array. Each record has id, source,
   kind, title, actor and an ISO timestamp with seconds and an explicit offset. Optional fields: status,
   url and subject_author. Keep kinds concrete, such as authored, reviewed,
   merged, attended or responded. Attendance alone does not prove contribution.
3. Run the reusable report helper:

```sh
node scripts/period-report.mjs --input evidence.json --output activity.md --start 2026-01-01 --end 2026-01-31 --timezone Europe/London --actor contributor
```

The helper filters by local calendar date and actor, deduplicates repeated events,
excludes self-review when subject_author is supplied, strips URL query/fragment
values and keeps recorded statuses. It refuses existing output unless --overwrite
is supplied. Its tests are scripts/period-report.test.mjs.

4. Add a short audience-specific interpretation, keeping observed work separate
   from claimed impact. Link outcomes only when the sources establish them. An open
   request is not shipped work; two activities are not automatically two outcomes.
5. State source coverage, failures and remaining gaps. Missing evidence is not zero
   activity. Draft only; posting, submitting a review or sharing a private report
   requires its own authority. Keep raw evidence local and omit sensitive content.
