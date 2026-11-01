# Make mock behavior observable

Use when a controlled service stands in for an external dependency during an
integration test. The application path under test should stay real where feasible.

- Define an explicit match contract: method, path, query, selected headers and
  body fields, including nested fields. State whether predicates combine with AND
  and how competing rules are ordered. Match synthetically, without real secrets.
- Give every rule a stable diagnostic ID and expose it through a test-only response
  header or fixture log. Verify that the intended rule fired. A successful response
  from a permissive default can hide a broken matcher.
- Prefer a visible unmatched-request failure for strict tests. If the scenario
  deliberately needs a default, assert that default explicitly. Never infer that a
  deny rule works because a different request happened to receive a denial.
- Assert status, important headers, schema/body and application consequences.
  Include negative and boundary matches, unknown rules and malformed inputs.
- Keep synthetic configuration, clocks and keys reproducible; isolate data and
  restore process settings and temporary trust after tests.
- Do not ship fixture-only headers, debug endpoints or credential bypasses in the
  production application. The mock proves the tested scenario, not live-provider
  settings or a completed deployment migration.

A useful receipt names the request case, selected rule, expected/observed outcome,
actual application effects and cleanup status. Redact authorization and body data.
