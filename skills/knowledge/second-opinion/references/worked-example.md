# Worked example

A made-up review, to show the shape of one full run. The repo, the files and the findings are invented. Use it as a pattern, never as facts about a real codebase.

## The change

Branch `feature/export-retry`, 4 files, +120/-30 lines. It adds a retry to the call that sends invoice exports to a partner API, and a new `export_attempts` column.

## Step 2. Restate and confirm

```
Q1 (N1). Is this the change: "Retry failed invoice exports to the partner API up to
3 times with backoff, and record each attempt in export_attempts, so exports stop
failing on short partner outages"?
    Recommended: yes, because the commits and the PR body say exactly this.
```

User: "Yes."

## Step 3. Brief

- N2 Scope: inferred from `git diff --stat main...HEAD`. 4 files, nothing generated. Not asked.
- N4 Risk, asked:

```
Q2 (N4). Where does this run: in the checkout request, or in the nightly export job?
    Recommended: the nightly job, because export_invoices is only called from jobs/nightly.ex.
```

User: "Nightly job."

- N5 Merge pressure: inferred from the PR body ("no rush, partner outage is rare"). Not asked.
- N6 Known gaps: inferred from the PR body ("alerting comes in a follow-up"). Not asked.

## Steps 4 and 5. Reviewers and their questions

Reviewer A (session model) and Reviewer B (`sonnet`) return 5 findings in total. Both found the duplicate-invoice issue, so after merging there are 4, and one question:

```
Q3 (Q1 → F1). Does the partner API treat a repeated export with the same invoice id
as the same export (idempotent)?
    Recommended: no, assume duplicates, because their docs in docs/partner.md do not say.
```

User: "Not idempotent. They create a second record."

That answer raises F1 to Act on.

## Step 6. Buckets

- Act on: F1 the retry can send the same invoice twice when the first call times out after the partner saved it (A, B).
- Consider: F2 the backoff runs with `Process.sleep` inside the job, which holds a worker for up to 70 seconds (B).
- Noted: the new column has no index. It is never queried yet.
- Dismissed: "extract a Retry module" (A). One caller. An early abstraction.

## Step 7. Resolve the findings

```
Q4 (F1). Fix the duplicate risk now in this branch, or block the merge on it?
    Recommended: fix now, because a duplicate invoice is a money error.
```

User: "Fix now."

```
Q5 (F1.fix). Which fix: A send an idempotency key the partner supports, or
B check the partner for the invoice before each retry?
    Recommended: A, because docs/partner.md lists an Idempotency-Key header.
```

User: "A."

```
Q6 (F2). Fix the sleeping worker now, in a follow-up, or leave it?
    Recommended: follow-up, because this is a nightly job with spare workers.
```

User: "Leave it, we have 20 workers at night."

## Output

```markdown
### Change
> Retry failed invoice exports to the partner API up to 3 times with backoff, and record each attempt in export_attempts.

### Reviewers
- Reviewer A: general-purpose, session model, 3 findings
- Reviewer B: general-purpose, sonnet, 2 findings

### Findings
- Act on: F1 a retry after a timeout can create a duplicate invoice (A, B)
- Consider: F2 backoff sleeps inside the job worker (B)
- Noted: export_attempts has no index, never queried yet
- Dismissed: extract a Retry module (A). One caller, early abstraction

### Decision ledger
- Intent - retry partner exports 3 times and record attempts - user
- Scope - main...feature/export-retry, 4 files - inferred: git diff --stat
- Risk - nightly export job only - user
- Merge pressure - can wait - inferred: PR body
- Known gaps - alerting in a follow-up - inferred: PR body
- Q1 Partner API idempotent - no, creates a second record - user
- F1 Duplicate invoice on retry - fix now - user
- F1.fix - send the partner's Idempotency-Key header - user
- F2 Backoff sleeps in the worker - leave it - user ("20 workers at night")

### Agreement map
- A and B agreed on F1 on their own. Only B saw F2.
- No codebase-learner or why run was needed.

### Files written
- docs/decisions/0007-export-idempotency-key.md (the user said yes: a hard-to-undo contract choice)
```

Then the closing question: "Hand F1 to `tdd` now?"
