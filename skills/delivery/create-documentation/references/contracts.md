# Document contracts

Describe the externally visible agreement for events, messages, webhooks, files, or shared payloads. Use the **api** job for HTTP endpoint references and **handover** for an HTTP client packet. Non-HTTP client packets stay in **contract** mode and reuse the handover export checks without its HTTP-specific tables. Runtime language types alone do not establish the wire contract.

## Find authoritative definitions

Inventory operations or message types and their producers and consumers. Read the schema, validators, serializers, middleware, and contract tests. Record the checked revision. Compare declared requirements with actual serialized behavior and report mismatches.

Maintain one source of truth for each schema. Update that source when requested, then render reference tables from it. A generated PDF view may repeat complete field information without becoming a second hand-maintained contract.

## Describe what crosses the boundary

For each operation or message, state its purpose, transport, direction, access requirements, inputs, outputs, and errors. Add behavior that affects consumers, including side effects, ordering, delivery guarantees, retry policy, deduplication, and idempotency when supported.

For payload fields, document:

- Exact wire name, nesting, wire type, format, units, and constraints.
- Required, optional, or conditionally required presence, including the condition.
- The separate meanings of omission, `null`, empty values, and defaults.
- Enum values and their meanings. Keep lifecycle transitions distinct from a list of allowed values.
- Serialization of dates, time zones, decimals, large integers, binary content, and precision when relevant.
- Update semantics such as replacement versus patch and compatibility rules when defined.

Keep shared payload shapes in one maintained location. Explain operation-specific differences where they occur. Include success, error, and conditional examples as needed to resolve ambiguity, with their verification level stated.

## Output shape

```text
Contract scope, version, and inventory
Shared transport and delivery rules
Operation or message reference
Reusable payload definitions and field meanings
Error behavior, compatibility, and examples
Known gaps and verification record
```

## Verify

Compare the inventory with all in-scope definitions. Validate examples against the authoritative schema and test actual serializers where possible. Check field presence and wire types, not only a valid JSON parse. External readers must understand the contract without opening internal source files. Label gaps instead of filling them with conventional but unproven behavior.
