# API terms for a client handover

Adapt these definitions to the service. Include them in the exported packet so readers do not need an external website. Examples below are illustrative, not claims about the client's API.

## Read a request

```http
GET /v1/widgets/wdg_example?include=history HTTP/1.1
Host: api.example.test
Authorization: Bearer <ACCESS_TOKEN>
Accept: application/json
```

The base URL is `https://api.example.test`. The method is `GET`. The path is `/v1/widgets/wdg_example`. The path parameter `widget_id` replaces `{widget_id}` in `/v1/widgets/{widget_id}`. The query parameter `include=history` follows `?`. Headers appear below the request line. This example has no body.

## Request and response parts

| Term | Meaning for the caller |
|---|---|
| API | An interface through which software requests data or actions from another system. |
| Client and server | The client sends a request. The server receives it and returns a response. |
| Base URL | The service address for an environment. Add an operation's path to it using the documented version prefix once. |
| Environment | A deployment such as sandbox or production. Its credentials, data, and available operations may differ. |
| Endpoint or operation | In an HTTP reference, a method and path together, such as `GET /v1/widgets/{widget_id}`. The same path can support several methods. |
| HTTP method | The action named in the request, such as `GET`, `POST`, `PATCH`, or `DELETE`. Use the operation's documented method and semantics. |
| Path parameter | A value substituted into a path placeholder. A declared OpenAPI path parameter is required. Send the value, not the braces. |
| Query parameter | A named value after `?` in the URL, often a filter or page control. Separate pairs with `&`. Follow the documented encoding for lists and special characters. |
| Params | An ambiguous shorthand. State whether you mean path parameters or query parameters. Framework naming does not change where the value travels. |
| Request header | Metadata sent with a request, such as authorization or the body format. It is separate from the URL and body. |
| `Authorization` | A header carrying credentials according to the documented scheme. A bearer token goes after `Bearer ` and must remain private. |
| `Accept` | A request header describing response media types the client can accept. |
| `Content-Type` | A header identifying the format of the message body, such as `application/json`. A request and its response can have different content types. |
| Request body or payload | Data sent as the request content. It may be JSON, form fields, XML, or binary data. Some operations have no body. |
| Response | The server's reply, comprising an HTTP status, headers, and a body when applicable. |
| Response header | Metadata returned by the server, such as a request identifier, location, or download filename. |
| HTTP status code | A three-digit result for one request. `2xx` indicates success at the HTTP level. It does not by itself prove completion of a business process. |
| Application error code | A service-defined error identifier in the response. It has a different meaning and namespace from the HTTP status code. |
| Business state or status | A field describing the resource's progress. Its values and transitions are defined by this service. |
| Schema | A definition of the allowed structure, types, and constraints of a message. An example illustrates a schema but does not list every valid message. |
| cURL example | A command for making an HTTP request. Replace named placeholders and follow prerequisites before running it. |

If a request asks for "server code", describe HTTP status codes unless the context clearly asks for server source code. Client reference documents do not need private implementation code.

## Read a field table

| Term | Meaning for the caller |
|---|---|
| Required | The field must be present in the stated request, response, or variant. |
| Optional | The field may be omitted. This does not mean that `null` is accepted. |
| Conditional | The field is required or valid only when a stated condition holds. |
| Nullable | The field may contain JSON `null`. Presence and nullability are separate rules. |
| Omitted, null, and empty | An omitted key, a `null` value, an empty string `""`, an empty array `[]`, and an empty object `{}` are different inputs. The API defines how each behaves. |
| Default | The documented value or behavior when a field is absent. An example value is not a default. |
| Enum | A defined set of allowed values. Match spelling and case exactly. |
| Format and units | Additional meaning, such as a date-time with a timezone or an amount represented as a decimal string. Use the documented format and units. |
| Nested field | A value inside another object. `address.city` identifies `city` inside `address`; `items[].quantity` identifies a field in every array item. These paths describe the table, not literal JSON keys. |
| Read-only or write-only | A field restricted to responses or requests respectively by the schema. Confirm the applicable message direction. |

## Shared behaviors

| Term | Meaning for the caller |
|---|---|
| Authentication | How the service establishes who is calling. |
| Authorization or scope | Which operations or resources that caller may access. |
| Pagination | Retrieving a long list in portions. Follow the documented next-page mechanism and stopping condition. |
| Cursor | A server-issued page token. Treat it as opaque unless the contract says otherwise. |
| Idempotency | A documented way to repeat an operation without repeating its business effect. A service may use a key with defined limits. Do not assume every operation supports it. |
| Rate limit | A service-defined request allowance. Follow the documented limit and retry instructions. |
| Correlation or request ID | A value used to trace requests. Supply the documented identifier to support when reporting a failure. |
| Webhook | A request the service sends to a client-provided endpoint to report an event. Verify it using the documented mechanism. |
| Terminal state | A state with no further transitions in the documented lifecycle. A value that sounds final is not sufficient evidence. |
| Deprecation | A declared plan to retire or replace an operation or field. Follow the documented migration and verified retirement schedule. |

Definitions follow HTTP semantics and OpenAPI terminology. Verify any service-specific use against its contract. Standards references are [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html) and the [OpenAPI parameter definition](https://spec.openapis.org/oas/v3.1.0.html#parameter-object).
