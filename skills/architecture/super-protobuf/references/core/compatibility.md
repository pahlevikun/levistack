# Compatibility envelope

A `.proto` change is not "safe" because the new file compiles. Decide the envelope before you judge the diff.

## What to establish

- Old schema and new schema (not only the result).
- Encoding: binary protobuf, ProtoJSON, text format, or more than one.
- Persistence: databases, queues, logs, caches, events — stored bytes outlive deploys.
- Consumers: in-repo only, or independent clients and generated languages.
- Extras: HTTP/JSON transcoding, reflection, schema registry.
- Deploy: order, rollback window, how long mixed versions run.

If any of that is unknown, say so and lower confidence. Do not call a change backward-compatible from the new file alone.

## Four dimensions

Assess each changed symbol on all four:

1. **Binary wire** — can old and new readers parse both old and new bytes without corruption?
2. **Named formats** — ProtoJSON, text format, REST transcoding, name-based consumers.
3. **Source / generated API** — will regenerated clients compile? Presence, enum, accessors.
4. **Behavior** — status codes, retry safety, deadlines, authorization, streaming, resource bounds.

JSON is a narrower envelope than binary. Renames that look wire-safe still break JSON and generated names.

## Mixed-version paths

For every non-trivial change, walk:

- old writer → new reader
- new writer → old reader
- old reader modifies and reserializes a new message (unknown-field drop)
- rollback after new writers have emitted new values
- persisted old data read after the migration

Conditionally compatible changes need an explicit writer constraint and a date when it may lift. Default rollout: **readers before writers**; keep the old field or method until rollback is unnecessary.

## Verdicts

Lead with one:

| Verdict | Meaning |
|---------|---------|
| Compatible | Safe inside the stated envelope |
| Rollout-dependent | Parseable, but only with sequencing or value constraints |
| Breaking | Wire, named-format, source, or behavior incompatibility |
| Insufficient context | Old schema, encoding, consumers, or deploy model unknown |

Finding shape:

```text
[severity] Short title
Location: file and symbol
Dimension: binary | JSON/text | source | behavior
Change: old contract -> new contract
Impact: mixed-version scenario that fails
Remediation: smallest schema change or staged migration
```

**Blocker:** tag reuse, unparsable data, unavoidable production break. **High:** likely cross-version loss or unsafe RPC. **Medium:** bounded operability. **Low:** maintainability. Do not inflate style into compatibility.

## Principles

- Never reuse a field or enum number; reserve deleted numbers and usually names.
- Field-number changes and moving fields into an existing `oneof` are breaking.
- Type and cardinality changes are migrations even when wire types look compatible.
- Adding a field or enum value can still break generated code or exhaustive switches.
- Preserve unknown fields on read-modify-write when forward compatibility depends on them.
- Do not recommend retries on a mutating RPC without idempotency or dedupe.
- Do not flag a new optional field as breaking solely because old clients ignore it.
- Do not require streaming, retries, health, or HTTP transcoding of every service.
