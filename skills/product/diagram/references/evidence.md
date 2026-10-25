# Ground a technical view

For a current-state diagram, inspect the current implementation. Old docs, a directory name and a familiar framework pattern are leads to check. They do not prove a connection.

## Build the bounded inventory

Read entry points, wiring, execution paths, serializers, schema and relevant config. Use the repository's discovery tools and access rules. `rg` works for literals and excluded files. For broad discovery, reuse `codebase-learner` findings with their source anchors.

Record the revision, paths and symbols actually read. Give every important node and edge an evidence row. Mark gaps. Keep assumptions separate from verified paths.

| View | Check before drawing |
|---|---|
| Architecture | Imports and dependencies, registration, runtime ownership, external interfaces and boundaries |
| Deployment | Deployment files, hosts, replicas, exposed ports, environment gates and network paths. Local development config does not prove production topology |
| Request sequence | Router and middleware order, handler calls, task boundaries, side effects, serialization and responses |
| Process or state | Branch conditions, transitions, retries, waits, cancellation, terminal states and error paths |
| Data model | Current migrations or DDL, constraints, references, nullability, types and relationship enforcement |

Prove reachability through a router, registration, scheduler, import/export path or trace. Draw a wired but disabled feature as disabled. Do not call a function dead solely because a narrow search found no callers. Name the search scope and keep uncertain reachability unknown.

Separate current and proposed states. For a before/after view, use stable IDs and the same scope, then list added, removed and changed relationships. A bug found while documenting is a finding. Do not silently change code or turn the bug into a normative contract.

## API and machine contracts

A sequence explains interactions. It does not replace a contract reference. Give `create-documentation` the verified contract inventory when a full reference is requested.

Read routing, validation and serializer configuration together. A domain type may serialize differently. Ground these details when they affect the diagram:

- Method, path, direction, request and response wire shapes, status and error envelope.
- Authentication actually implemented, without adding a familiar provider or grant.
- Required, optional and conditionally required fields. Omitted, null and default values can differ.
- Identifiers, enums, decimal and date encodings, size limits and domain constraints.
- Side effects, transactions, idempotency, retries, ordering, redelivery and acknowledgement.
- Async work and external boundaries, including timeout and failure behavior.

Keep one owner for each field definition. Link an existing OpenAPI, AsyncAPI or schema instead of creating a competing table. If no machine spec exists, keep a compact shape catalog beside the diagram with source anchors. Label examples illustrative and run them when safe and authorized.

## Legacy documentation

Inventory entry points, commands, config, data, integrations and build/deploy surfaces before choosing views. Keep the coverage ledger with commands, dates and denominators. Say which part was read and which remains unknown.

Trace one real scenario across the boundaries. Include surprising shortcuts, unreachable transitions and transport asymmetries when they matter. Cite historical intent only if history or an identified source supports it. Label interpretations as such.

Extend the living documentation instead of building a competing tree. Keep the diagram's source, render, owner and evidence anchors together. Update the index when a view changes or a render is pending. Do not claim exhaustive coverage from a sample of files.
