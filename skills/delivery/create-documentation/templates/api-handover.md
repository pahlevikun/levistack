# <Service> API integration guide

Document revision: <revision>. API version: <version>. Source release: <release>.
Prepared: <date>. Verification: <scope and date>. Audience: <client team>.
Status: <draft, limited coverage, or verified scope>.

Working evidence: <Bruno collection read or created first; code snapshot; relevant Git range; available plans, existing docs, Swagger/OpenAPI; missing sources>. Keep private source paths in the working notes rather than the client export.

<!-- Authoring template. Replace placeholders, expand repeated sections, and remove author instructions. Never present illustrative values as verified service behavior. -->

## Contents

<!-- Add internal links to the completed sections and each operation. Verify links in the export. -->

## Scope and environments

<What the client can integrate, supported versions, intentional exclusions, and sandbox-only features.>

| Environment | Base URL | Purpose and access prerequisites |
|---|---|---|
| <environment> | <approved URL> | <purpose, who supplies credentials> |

## API terms

<Insert the relevant definitions and annotated request from the glossary. Include path parameters, query parameters, headers, body, response, HTTP status, application code, and business state.>

## Access and first request

<Explain actual authentication, permissions, credential provisioning, supported expiry or refresh, and required tooling.>

1. <Obtain credentials through the documented channel.>
2. <Set the base URL and placeholders locally.>
3. <Run a safe first request. Show its copyable cURL command and matching HTTP response, including complete JSON when returned.>

Example evidence: <live sandbox run, fixture test, schema check, or not run>.

## Endpoint index

| Method | Path | Purpose | Permission | Availability | Entry |
|---|---|---|---|---|---|
| <method> | <templated path> | <purpose> | <scope> | <environment or maturity> | <internal link> |

## <METHOD /path/{id}>

<Purpose, prerequisites, side effects, and environment restrictions.>

### Request

Method: <method>. Path: <templated path>. Authentication: <scheme and scope>.
Request media type: <type or no body>. Response media types: <types>.

#### Headers

| Header | Presence | Value or format | Meaning and constraints |
|---|---|---|---|
| <name> | <required, optional, conditional> | <format> | <meaning, source, condition> |

#### Path parameters

| Name | Wire type | Presence | Meaning and constraints | Example |
|---|---|---|---|---|
| <name> | <type and format> | Required | <meaning and limits> | <synthetic value> |

#### Query parameters

| Name | Wire type | Presence | Default or omission behavior | Meaning and limits |
|---|---|---|---|---|
| <name> | <type and encoding> | <presence> | <verified behavior> | <meaning, bounds, values> |

#### Body fields

<State no body when applicable. Describe variants before their field tables. Add cookies or form/file fields when used.>

| Field path | Wire type | Presence | Nullable | Meaning and constraints |
|---|---|---|---|---|
| <full nested path> | <type and format> | <presence and condition> | <yes or no> | <units, allowed values, defaults, bounds> |

### Example request

<Give one copyable command per operation. Replace this illustrative shape with an evidenced route and fields. Include how to obtain IDs and state the evidence label. Never put a real credential in the export.>

```sh
curl --request <METHOD> \
  --url '<BASE_URL>/<path>?<supported_query=value>' \
  --header 'Authorization: Bearer <ACCESS_TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '<complete sanitized JSON request body>'
```

<Remove unsupported headers, query fields, and --data. For a JSON body, show the same complete payload separately so clients can read and copy it. For a bodyless operation, state "Request body: None".>

```json
<complete sanitized request JSON when the operation accepts JSON>
```

### Responses

| HTTP status | Condition | Relevant headers | Body or schema | Caller action |
|---|---|---|---|---|
| <evidenced status> | <trigger> | <headers> | <internal schema link or no body> | <next step> |

#### Response fields

| Field path | Wire type | Presence | Nullable | Meaning and constraints |
|---|---|---|---|---|
| <full nested path> | <type and format> | <presence> | <yes or no> | <semantics and limits> |

#### Success example

<Show the response matching the cURL request. Label observed, fixture-tested, contract-derived, or not run. For a download, describe binary format and saving instead of inventing JSON. For a 204, state "No response body".>

```http
HTTP/1.1 <actual success status and reason phrase>
Content-Type: <actual media type when present>
<other relevant response headers>
```

```json
<complete sanitized success response JSON when the operation returns JSON>
```

#### Error and conditional examples

| Scenario | HTTP status | Application code | Meaning | Recovery or retry |
|---|---|---|---|---|
| <supported scenario> | <status> | <actual code or none> | <cause> | <safe caller action> |

<Include matching sanitized error bodies and relevant conditional payloads. For each distinct error, show the failing request or exact prerequisite, response status, relevant headers, and complete body. Do not imply untested cases were observed.>

##### <Error scenario for this operation>

Trigger or prerequisite: <invalid input, missing permission, resource state, or other evidenced condition>.
Example evidence: <observed, fixture-tested, constructed from contract, or not run>.

```http
HTTP/1.1 <actual error status and reason phrase>
Content-Type: <actual media type>
<other relevant response headers>
```

```json
<complete sanitized response body using the service's actual error envelope>
```

Cause: <why this case fails>. Caller action: <correction, safe retry, or escalation>.

<Repeat under this endpoint for each supported error variant. Preserve nested validation details when returned. For a bodyless error or a non-JSON response, state or show its actual representation. A code table or shared schema link does not replace these examples.>

### Supported response and state variants

| Scenario | Request or state prerequisite | HTTP outcome and body variant | Meaning and client action | Example |
|---|---|---|---|---|
| <supported scenario> | <how it is reached> | <status, headers, full body shape> | <what happens next> | <internal link> |

<Include all evidenced success, error, conditional payload, and business-state outcomes. Reconcile against the working scenario matrix and Bruno cases before calling the packet complete.>

## Shared schemas and conventions

<Expand referenced fields here when several operations share a schema. Keep requiredness and nullability separate. Explain timezones, units, precision, omitted values, pagination, sorting, idempotency, and limits where supported. Include a next-page example.>

## Business lifecycle

<Distinguish HTTP success from completion. Use a separate table for each business state field and explain how the client observes changes.>

| State field and value | Meaning | Entry event | Allowed next states | Terminal | Client action |
|---|---|---|---|---|---|
| <field=value> | <meaning> | <trigger> | <evidenced transitions> | <yes, no, or unknown> | <poll, wait, act, or escalate> |

## Troubleshooting and support

<Explain actual error envelope, request IDs, rate limits, safe retries, timeouts with uncertain outcomes, known limitations, and approved support contact.>

## Revisions and migration

| Document revision | Date | API release | Client-visible change or migration |
|---|---|---|---|
| <revision> | <date> | <release> | <change> |

## Verification and companion files

<State what was checked and what remains unverified. List matching sanitized OpenAPI and Bruno artifacts when included.>

Editable source: <filename>. Export: <filename>. Regeneration: <actual command or documented tool steps>.
