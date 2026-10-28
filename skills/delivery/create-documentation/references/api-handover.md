# Client API handover

Produce an HTTP API document that clients can use without the repository, Bruno, or a documentation server. Keep an editable source and render the requested PDF, HTML, or DOCX from it. A collection of successful responses alone is not a contract.

For non-HTTP contracts, use the contract job and the protocol's operation, payload, and error definitions. Reuse the export checks below, but replace HTTP-specific tables and glossary entries with those definitions. GraphQL application errors, gRPC statuses, and WebSocket frames are not interchangeable with HTTP status codes.

## Start with Bruno

1. Locate and read the target collection first. Inspect collection and folder settings, environments, auth, requests, disabled fields, scripts, docs, and assertions. Account for values changed by scripts without executing them. Never execute a collection just to discover its content.
2. If the collection is absent, invoke `create-bruno-collection` in a collection-only phase before drafting. Its discovery step may read code and available specs to construct requests. Return the resulting collection and case inventory to this handover, then read them. Do not recursively launch another handover.
3. Use this same collection throughout reconciliation. Complete a partial or stale collection through `create-bruno-collection` before final delivery. Do not replace an existing collection wholesale when adding missing cases is sufficient.

Collection creation is part of a requested handover. It does not permit changing application behavior, running production requests, or overriding an explicit instruction to leave `.bru` files untouched. If the collection cannot be created from the available evidence or writes are forbidden, report the prerequisite gap. A sample-only draft may proceed with a visible limitation; it is not a complete handover.

## Reconcile the release and evidence

1. Identify the audience, integration scope, API version, document revision, release or commit, environment, and verification date. Use the project's document location and renderer when available.
2. Learn the codebase flow behind the collection. Read mounted routes, validators, serializers, authentication and error middleware, business rules, state definitions, tests, and relevant configuration. For a broad service, use `codebase-learner` before tracing individual operations.
3. Inspect relevant Git history for those files and the target release, using scoped logs, diffs, or blame when needed. Identify changed fields, deprecated responses, and lifecycle decisions. Work from local history; a missing Git repository or shallow history is an evidence gap, not a reason to invent the past.
4. Read available plans, design decisions, existing documentation, and release notes. Separate accepted or implemented behavior from proposals, obsolete descriptions, and unreleased changes. Do not expose private material to clients.
5. Read the available Swagger/OpenAPI definition or framework export, resolve schemas, and compare it with code and Bruno. Preserve the project's spec dialect. Do not fabricate a spec or pretend one exists when absent.
6. Build a working coverage table with one row per operation and a source ledger naming each available input, its version, and any missing source. Key HTTP operations by method and normalized path, not by request filename. Several success and error `.bru` cases may map to one operation.

| Operation | Exposure | Contract and implementation evidence | Bruno cases | Document section | Verification or gap |
|---|---|---|---|---|---|
| `<METHOD /path/{id}>` | `<client, internal, sandbox>` | `<spec pointer, route, test>` | `<case paths or missing>` | `<anchor>` | `<contract, tested, observed, conflict, unknown>` |

Reconcile routes, spec, collection, and document in both directions. Include only the agreed client surface. List intentional exclusions with reasons in the working evidence. Keep sandbox simulation operations clearly labeled. A raw route scan is a lead, not proof of the mounted public surface.

Flag a spec/implementation mismatch with both sources. Resolve it against the target release or record an explicit limitation. Do not silently choose whichever source makes the document look complete. If only Bruno or a PDF exists, label it as sample-derived and list unknown constraints. A successful sample cannot establish requiredness, all enum values, defaults, or every error.

## Cover variants and states

Build a second table with one row per distinct supported scenario. Derive rows from validation branches, middleware and business errors, schema variants, tests, collection cases, and state definitions. Include conditional bodies, omitted/null/empty behavior where distinct, authentication and permissions, conflicts, empty and paginated results, asynchronous outcomes, downloads, and retries only when supported. Cover meaningful equivalence classes and boundaries, not every possible input combination.

| Operation and scenario | Trigger or prerequisite | Status and response variant | State or transition | Source evidence | Bruno case | Document entry | Verification or gap |
|---|---|---|---|---|---|---|---|
| `<operation; scenario ID>` | `<input or fixture>` | `<HTTP status, headers, body schema/example>` | `<field/value or edge, if relevant>` | `<code/test/spec/history/docs>` | `<case path or missing>` | `<anchor>` | `<present, unrun, tested, unknown, conflict>` |

Reconcile this matrix in both directions. Cases with the same method and path stay separate scenarios under one operation. Every evidenced business state and allowed transition needs its meaning, conditions, client action, and scenario evidence. Explain how to obtain the prerequisite resource state; do not invent a request parameter or a simulation endpoint to force it.

Use `create-bruno-collection` to add missing supported cases and state prerequisites, then reread the changes before writing. Missing or unsupported fixtures remain gaps. Distinguish a case that exists but was not run from a case absent from the collection. Keep undocumented future or historical behavior out of current coverage. Do not promise complete coverage when any supported variant is still missing or unresolved.

## Assemble the packet

Use the handover template and glossary selected from SKILL.md. A packet may bind several page types. Keep the first-call walkthrough, glossary, endpoint reference, and lifecycle explanation in separate sections, with a contents page and internal links.

Include these client-facing parts:

1. Document identity, scope, supported environments, API version, and revision history. Distinguish the document revision from the API and schema versions.
2. A terminology guide with an annotated request. Explain each part before using unexplained abbreviations.
3. Access prerequisites, credential provisioning, authentication scheme, permissions, expiry, and refresh only where supported. Use placeholders for credentials. Identify who supplies each value.
4. A first-call walkthrough with a copyable cURL command, expected HTTP response and JSON body when the API returns JSON, and a verification label. Prefer a safe read operation. State prerequisites for operations with side effects.
5. An endpoint index and a complete entry for each included operation.
6. Shared schemas, errors, pagination, business states, rate limits, and retry rules that actually exist. State unavailable information instead of guessing.
7. Support and escalation information approved for clients, deprecation or migration notes, and known limitations.

Clients must not need internal source paths to understand a field. Keep detailed evidence and collection-case mappings in the working coverage table. Attach the sanitized spec and Bruno collection when requested, at matching versions.

## Fill each operation

Use a stable heading and anchor for the method and templated path. Keep concrete IDs and query strings in examples. Explain the purpose, permission, environment restrictions, side effects, and prerequisites.

Describe request headers, path parameters, query parameters, cookies when used, and body fields separately. For a missing part, state `None` or `Not applicable` explicitly. For every field provide:

- Exact wire name and full nested path, including array items such as `items[].quantity`.
- Wire type and format, meaning, units, and source of values.
- Required, optional, or conditional presence, with the condition. State nullability separately.
- Default when omitted, allowed values, bounds, length, precision, and serialization where supported.
- A consistent sanitized example. Cover variant bodies and conditional fields, not just one happy path.

Expand reusable schemas once and link within the exported document. Preserve composed and recursive schemas, discriminator rules, and differences between request and response fields. Do not flatten away `oneOf` conditions or read-only and write-only restrictions. Resolve external references into the packet so lookup works offline.

Document each supported request and response media type. For every evidenced response, record HTTP status, headers, body schema, example, trigger, and caller action. A `204` response has no body. Downloads need content type, filename headers, and save instructions. Streams need event shape and termination behavior. Explain stable application error codes separately from HTTP status codes. Include middleware and gateway errors when part of the supported contract.

Show a copyable `curl` command for each operation with its method, URL, supported headers, query values, and body when applicable. Show the matching sample request JSON separately when the request media type is JSON. Show the full HTTP status line, relevant headers, and complete sample response JSON for each JSON outcome. Cover every distinct supported error and conditional response scenario from the matrix under the operation. A shared error-code table, schema link, or global example is supporting reference and does not replace those responses. For bodyless, binary, form, or stream operations, state or show the actual wire format instead of inventing JSON.

For each error case, give the triggering request or prerequisite, full HTTP status line, relevant response headers, complete sanitized response body, cause, and recovery action. Separate machine-readable error codes from human-readable messages. Preserve validation details and nested field errors when the service returns them; never add fields the contract lacks. For a genuinely bodyless error, state that explicitly. Mark constructed contract examples and unrun cases honestly.

Use plain text code blocks, with no line numbers or inserted line breaks inside URLs or tokens. Explain ID dependencies between requests. Redact tokens, cookies, personal data, internal hosts, and account details consistently across the packet.

## Explain statuses and lifecycle states

Keep these concepts distinct:

- **HTTP status** describes the result of one request. `201` can create an object whose business work remains pending. `202` means acceptance for processing, not completion.
- **Application error code** identifies a service-specific failure inside a response. Its meaning comes from the service contract.
- **Business state** belongs to a resource or processing stage. Multiple state fields may describe different stages. Do not collapse them into one lifecycle.
- **Endpoint availability** describes environments or release maturity, such as sandbox-only or deprecated, when the service declares it.

For each business state field, enumerate evidenced values in a separate table. Include meaning, entry event, permitted next states, terminal status, client action, and how the caller observes progress. Source transitions from handlers, state definitions, tests, or an authoritative contract. An event sample is only one observed path. Do not infer that a value is terminal from its name.

Document polling or webhook behavior, ordering, timestamps, and consistency delays only when known. Flag contradictory state fields rather than explaining away a mismatch. Describe null, unknown future values, and absence according to the actual compatibility contract.

## Retry and pagination semantics

For idempotent operations, explain the key's scope, lifetime, replay response, changed-payload conflict, and concurrent-request behavior when known. An idempotency header in one example does not establish those guarantees.

For timeouts or transient errors, distinguish a safe retry from an operation whose result must first be checked. Never recommend retrying every write after a `5xx`. Document supported backoff and `Retry-After` behavior without inventing limits.

For lists, define every filter and cursor or offset field, ordering, page-size limits, the end-of-results signal, and a next-page example. An example value is not a default. Explain empty results separately from missing resources.

## Render and verify

1. Check the operation inventory and scenario matrix against Bruno and document entries. Confirm that codebase, relevant Git history, plans, existing docs, and Swagger/OpenAPI were reviewed when available, with absent inputs recorded. Check fields, statuses, headers, complete error bodies, payload variants, state values, and allowed transitions against the target release. Validate examples with the project's schema tool when available.
2. Run safe examples in an authorized sandbox or mock. Record whether evidence is a live request, test fixture, schema validation, or inspection. If a service is unavailable, retain `not run` labels and report that limitation. Do not call sample hosts or perform production writes to verify a document.
3. Render through the existing documentation pipeline. Otherwise produce a self-contained printable HTML file with embedded styling and assets. Use an available PDF or DOCX helper when that format is requested. A browser's print-to-PDF is a fallback. Report missing export tooling instead of renaming a text file or claiming an uncreated PDF.
4. Open the exported artifact. Check its contents, links, page numbers, repeated table headers, fonts, diagrams, code wrapping, and page breaks. Keep headings with their content. Preserve searchable, selectable text and copyable requests. Widen or split tables when field names, enum values, or words such as `Required` break across lines. Format JSON before export so wrapping does not split strings. Avoid tiny text and clipped columns.
5. For PDF, extract its text and compare the operation and schema inventory with the source. Render representative pages, including the widest table and longest example, and inspect them visually. An export command succeeding does not prove a usable PDF.
6. Deliver source, requested exports, and concise verification notes. Mark unresolved contract gaps as draft or limited coverage. Record the source version and regeneration command so API changes update the spec, document, and collection together.
