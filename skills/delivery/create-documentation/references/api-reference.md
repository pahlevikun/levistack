# API reference

Use this for an HTTP API reference or OpenAPI specification. Use the contract job for events, messages, and other wire interfaces. Use the handover job when clients need a standalone PDF, HTML, or DOCX packet.

## Contents
- Steps
- What each endpoint entry needs
- The spec skeleton
- Check it

## Steps

1. **Find the source of truth.** Identify the target release, public scope, existing spec, and framework export. Compare mounted routes, middleware, validators, serializers, and tests. A language type alone does not prove the wire representation.
2. **List every included operation** by method and templated path, with inputs, media types, responses, errors, and permissions. Reconcile code and spec in both directions. Mark internal and sandbox-only operations. Record missing evidence and contract disagreements instead of inventing behavior.
3. **Fill the spec or reference.** Update the existing owner. Prefer its generator over a parallel hand-written spec. Keep the project's OpenAPI version and tools. Add sanitized examples from fixtures or a permitted run, labeled with their evidence. Sample-only collections cannot establish the complete schema.
4. **Add the shared parts once:** supported auth, pagination, stable errors, and reusable schemas. Document overrides per operation. Do not infer a login route, token lifetime, permission model, or rate limit from a generic template.
5. **Check it** below. Report coverage, commands run, and unverified behavior. Documentation work does not authorize production requests or installing a documentation server.

## What each endpoint entry needs

| Part | Rule |
|---|---|
| Summary | One line, starts with a verb: "List users" |
| Identity and access | Method, templated path, stable operation ID, availability, auth scheme, scopes, and prerequisite IDs |
| Parameters | Name, location (path, query, header, cookie), wire type, format, required or conditional presence, serialization, omission behavior, default, limits |
| Request body | Media types, complete nested schema, requiredness distinct from nullability, variants, constraints, and valid examples |
| Responses | Every evidenced status, including middleware errors, relevant headers, media types, schemas, and examples. A 204 has no body. Describe binary or streaming responses accurately |
| Errors | HTTP status, stable application code, cause, example envelope, caller action, and safe retry behavior |
| Side effects | Emails sent, jobs queued, other calls made |
| Shared semantics | Pagination and end condition, units and decimal precision, timezone, state meanings, idempotency, compatibility, and deprecation when supported |

## The spec skeleton

This small illustrative spec is internally complete. Replace its operations and behavior with verified service facts. It is not evidence that any target API supports these routes or errors.

```yaml
openapi: 3.1.0
info: { title: Widget API example, version: 1.0.0 }
servers: [{ url: 'https://api.example.test', description: Example only }]
paths:
  /widgets:
    get:
      summary: List widgets
      operationId: listWidgets
      parameters:
        - name: limit
          in: query
          description: Maximum items returned
          schema: { type: integer, minimum: 1, default: 20, maximum: 100 }
      responses:
        '200':
          description: A list of widgets
          content:
            application/json:
              schema:
                type: array
                items: { $ref: '#/components/schemas/Widget' }
              example: [{ id: wdg_example, label: null }]
components:
  schemas:
    Widget:
      type: object
      required: [id, label]
      properties:
        id: { type: string, description: Widget identifier }
        label: { type: [string, 'null'], description: Display label when assigned }
```

Keep `operationId` unique and stable, because generated clients use it.

In OpenAPI 3.0, nullable schema values use `nullable: true` with an explicit type. OpenAPI 3.1 uses JSON Schema null types, such as `type: [string, 'null']`. Preserve the document's dialect. Neither form makes a property optional; the parent object's `required` list controls presence. A request body's own `required` flag is separate from its fields.

Document security schemes and operation overrides when the API uses them. Do not put a real token in the spec. Swagger UI, SDK generation, or a served docs route are separate implementation work when requested, not prerequisites for a reference document.

## Check it

- Use the repo's OpenAPI linter, or an available compatible linter. Resolve all schema references, validate example types and formats, and check unique operation IDs, path placeholders, required flags, and security overrides.
- In an authorized sandbox or mock, run at least one request per new operation plus relevant error and conditional cases. Compare status, headers, and body with the spec. Use test evidence when a live service is unavailable and label what was not run.
- Compare public routes, spec operations, Bruno cases when supplied, and reference entries. Report omitted, stale, or extra operations and exclusions. Multiple test cases are not multiple endpoints.
- If no validator or service is available, report the inspection performed and its limits. Do not claim a lint or runtime check passed.

Normative definitions are in the [OpenAPI 3.0 schema specification](https://spec.openapis.org/oas/v3.0.3.html#schema-object) and [OpenAPI 3.1 schema specification](https://spec.openapis.org/oas/v3.1.0.html#schema-object).
