# API reference

Use this for an HTTP API, an event contract or a library surface that needs a reference.

## Contents
- Steps
- What each endpoint entry needs
- The spec skeleton
- Check it

## Steps

1. **Find the source of truth.** An OpenAPI file, route definitions, or typed handlers. If a spec exists, update it. Do not write a second copy by hand.
2. **List every route** with its method, path, parameters, request body, responses and errors. Read the handler and the tests, not only the route table.
3. **Fill the spec or the reference page.** Real example values, taken from tests or a run.
4. **Add the shared parts once:** auth, pagination, the common error shape. Reuse them with references instead of repeating.
5. **Check it** (below).

## What each endpoint entry needs

| Part | Rule |
|---|---|
| Summary | One line, starts with a verb: "List users" |
| Parameters | Name, where it goes (path, query, header), type, required or not, default, limits |
| Request body | The schema and one real example |
| Responses | Every status the code can return, each with a body shape. Include 401, 403, 404, 409 and 422 when the code returns them |
| Errors | The stable error code or message, the cause, and what the caller should do |
| Side effects | Emails sent, jobs queued, other calls made |

## The spec skeleton

```yaml
openapi: 3.1.0
info: { title: <name>, version: <x.y.z> }
servers: [ { url: <base url>, description: <env> } ]
paths:
  /things:
    get:
      summary: List things
      operationId: listThings
      parameters: [ { name: limit, in: query, schema: { type: integer, default: 20, maximum: 100 } } ]
      responses:
        '200': { description: OK, content: { application/json: { schema: { $ref: '#/components/schemas/ThingList' } } } }
        '401': { $ref: '#/components/responses/Unauthorized' }
components:
  schemas: {}
  responses: {}
```

Keep `operationId` unique and stable, because generated clients use it.

## Check it

- Lint the spec with the repo's tool, or a standard OpenAPI linter if there is none.
- Send at least one real request per new endpoint and compare the response with the documented shape.
- Compare the spec with the handlers: a route in code and not in the spec is a gap, and so is the reverse.
