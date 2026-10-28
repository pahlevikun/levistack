# Deep review of a risky change

Use this pass when the user asks for depth or the change touches identity, permissions, personal data, a public contract, or a migration with hard rollback. It extends the read-only MR preview. Do not turn depth into automatic publication.

1. Name the concrete failure modes to test. Collect the full MR diff, current open threads, relevant contract and source at the MR head SHA, pipeline result, and failing job traces. A summary alone is insufficient.
2. Give independent reviewers distinct questions only where the diff warrants them, such as authorization, data consistency, or test behavior. Each receives the same revision and reports findings with file and line, evidence, and what it could not verify. Skip unused lenses.
3. If reviewers disagree, compare their claims against the source and an executable check or contract. Re-read each proposed finding at the head SHA. Drop findings whose line or behavior does not match that revision.
4. For each changed branch, identify a test example and the assertion that would detect a regression. Mark a missing or stub-only assertion as a gap. Distinguish a local test run from a CI job result.
5. Fold verified findings into the normal preview. State the revision, pipeline evidence, remaining uncertainty, and why the deeper pass changed the verdict, if it did.

Use `second-opinion` instead when the user wants its separate adversarial verdict and decision ledger. A deep pass inside this skill still produces one MR preview.
