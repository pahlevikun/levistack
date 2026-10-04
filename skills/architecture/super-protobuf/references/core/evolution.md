# Schema evolution

Stay in the current package version for additive change. Cut a new `vN` directory for breaks.

## Safe in the same version

- Add a field with the next number (prefer 1–15 for hot fields).
- Add an enum value (never reuse 0; keep `*_UNSPECIFIED`).
- Add a method or service.
- Add a message.
- Mark elements `[deprecated = true]`.

Document new fields. Add protovalidate constraints that old writers can still satisfy (do not tighten "required" on a field old clients omit).

## Wire-safe, still a migration

These often parse on the wire and still break generated code, JSON, or stored data:

- Add `optional` to an existing scalar (presence changes).
- Remove a field (reserve number **and** name).
- Remove an enum value (reserve).
- Move existing fields into a `oneof`.
- Change between "compatible" integers (`int32` ↔ `int64`) without a range and rollout plan.

Treat these as **rollout-dependent**. Deploy readers that understand both shapes before writers switch.

## Breaking — new package version

- Reuse or renumber fields.
- Incompatible type changes.
- Rename fields (JSON and generated APIs).
- Change RPC request/response types or streaming mode.
- Remove without reserving.
- Semantic change of an existing field ("this int is now millis, not seconds").

Create `…/v2/` beside `v1`. Do not rename `User` to `UserV2` inside `v1`.

## Stored data and events

If messages hit a database, queue, or log:

1. Old bytes must still decode after the change.
2. New bytes must not poison old readers still in the fleet.
3. Read-modify-write paths must not drop unknown fields.
4. Cache keys that embed proto blobs should include a schema version.

A `buf breaking` pass that is green against git is necessary, not sufficient, when stored payloads exist.

## Mixed-version deploys

Typical sequence for a new field that old readers must ignore:

1. Ship readers (and stored-data migrators) that tolerate the new field.
2. Ship writers that populate it.
3. Only then enforce new validation that requires the field.
4. Keep rollback to step 1 until the fleet and stored data are clean.

Typical sequence for a replacement field:

1. Add the new field; dual-write.
2. Readers prefer the new field, fall back to the old.
3. Deprecate the old field; stop writing it.
4. After the compatibility window, reserve the old number in a **new** major version (or never remove it on a published API).

## Tooling

```bash
buf breaking --against '.git#branch=main'
```

Use `FILE` (strict, default in this catalog's `buf.yaml`) unless the repo already chose `PACKAGE`, `WIRE_JSON`, or `WIRE`. Changing the rule set does not make an unsafe change safe.
