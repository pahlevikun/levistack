# Evaluate the tool integration

Separate four acceptance layers:

1. The selected configuration is syntactically valid and preserves unrelated data.
2. The real transport negotiates a compatible version and advertises the expected
   capabilities and schemas.
3. Individual operations obey their input/output, ownership, failure, pagination,
   bounded-work and idempotency contracts.
4. A caller can discover the correct operation and complete the actual task.

Use synthetic data and a controlled upstream to reproduce timeouts, denied access,
malformed data, empty and terminal pages, schema violations and partial failure.
Tests should fail when their relevant guard or behavior is removed. Test duplicate
or conflicting operation requests when the integration can mutate shared state.
No operation becomes safe because its descriptor says read-only.

For agent-level evaluations, use representative user tasks and a ground truth
that can be independently checked. Include near-miss requests, ambiguity and one
unsupported task so broad discovery does not look like good coverage. Report
missing tools and model-selected wrong operations separately from server failures.
Use the same task set and environment for baseline/candidate comparisons; record
actual results, repetitions and uncertainty. A small smoke run does not establish
a benchmark improvement or general reliability.

Keep recorded inputs, expected outputs and receipts free of live credentials or
private source data. A mock pass establishes the selected fixture contract; it does
not prove a remote deployment or another runtime works. Re-run against the target
host and required real service only when that environment and operation are authorized.
