# Judge completed work

This mode is read-only. Treat the report being judged as a list of claims to test. It may judge one artifact or a completed `rumbling` batch. `second-opinion` owns adversarial code-change review and the author's decision ledger; use it when that specialized review is needed, then test its material claims here.

1. Extract each material claim: what changed, what passed, what was untouched, and what was published. Include any stated scope or acceptance condition.
2. Inspect the actual artifact and its source record. For code, read the diff and status against the intended base. For a document, inspect the exported file and its source. For a data result, inspect the source and reproduce a decisive calculation.
3. Rerun each claimed check when the environment permits. Record the command, scope, exit code, and meaningful output. A test count of zero or a check of the wrong branch does not support a pass claim.
4. Look for changed or skipped checks, unsupported facts, unrelated edits, omitted required work, and outward actions without authorization. For domain work, use its actual contract and authority rather than a generic checklist.
5. Give one verdict. **Verified** means the material claims reproduced. **Verified with limits** means the artifact is sound but named claims could not be checked. **Refuted** means a material claim failed; quote the contradiction and name the smallest corrective action. Use a claims table with evidence for each row. Do not edit the judged work in this mode.

For a completed parallel batch, wait until every worker has finished or been marked a dropout. Read every report and inspect each actual output. Apply the coordinator's stated criteria to each candidate or task result. Separate independent agreement from repeated assumptions, show disagreements and missing checks, and recommend which outputs can be accepted. A vote is not evidence; if the criteria cannot distinguish two candidates, say which fact or test would settle it. The coordinator owns integration and any edits after this judgment.

For a **suite** request, first locate the target's real eval cases and ground truth. Run those cases with the stated candidate and baseline if the runner exists. A single run is a smoke exercise, not a measured improvement. If fixtures or a runner are missing, judge the available artifact and report that the suite was not run. Never cite an upstream suite that is not installed here.
