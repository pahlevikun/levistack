# Synthetic archive API contract

This fictional contract is an evaluation input. It is not a deployed service. Treat the facts below as the complete normative contract for this exercise. No request has been run. Generate client documentation, not server code.

## Identity and access

API version 1.0.0. Contract revision demo-1. Environment sandbox only. Base URL `https://archive.example.test`. Document revision may differ from API version. Support is the client's integration contact, with no email address specified.

All three operations require `Authorization: Bearer <ACCESS_TOKEN>`. The integration contact supplies the token. Provisioning mechanism, token expiry, and refresh are unspecified. Scope `archives:read` permits reads. Scope `archives:write` permits creation. Request header `Accept: application/json` is optional. JSON requests require `Content-Type: application/json`.

## Public operation inventory

| Method | Path | Operation ID | Purpose | Scope |
|---|---|---|---|---|
| POST | /v1/archive-jobs | createArchiveJob | Queue an archive job | archives:write |
| GET | /v1/archive-jobs/{job_id} | getArchiveJob | Read a job | archives:read |
| GET | /v1/archive-jobs | listArchiveJobs | List jobs | archives:read |

An internal `GET /internal/metrics` route is not part of the client contract. There are no simulation endpoints.

The companion `archive-bruno/` folder contains actual Bruno request files, `bruno.json`, and a placeholder Sandbox environment. Inspect that collection before drafting the handover. Its initial six cases are `create-valid`, `create-invalid`, `create-no-token`, `read-found`, `read-missing`, and `list-first-page`. The completed collection has 20 declared cases across three operations, not 20 endpoints. It adds the remaining supported endpoint errors, optional-label variants, all four read-state scenarios, next-page, and empty-list scenarios. Requests and assertions have not been run. State, missing-resource, cursor, and empty-list cases need externally prepared test data; they do not force a response or introduce new endpoints.

No application implementation, service Git history, plan, machine-readable Swagger/OpenAPI file, or live service is supplied. Record these source gaps rather than inventing them. This fictional contract supplies the intended behavior. Collection files supply requests and declared assertions, not proof of runtime behavior.

## Create a job

`POST /v1/archive-jobs` queues work. It has no path or query parameters. It does not support idempotency keys. A request may enqueue another job if repeated. On timeout, ask the integration contact to check the outcome before resubmitting. No reliable client-side lookup key is defined.

Body is a required JSON object with no additional properties:

| Field | Wire type | Presence | Null accepted | Meaning and constraints |
|---|---|---|---|---|
| source | object | Required | No | Source selection; no additional properties |
| source.collection | string | Required | No | Collection name, length 1 through 40 |
| label | string | Optional | Yes | Display label, at most 80 characters; omitted becomes null; empty string is retained |

Request example is `{"source":{"collection":"demo-records"},"label":null}`.

Success is HTTP 202 with `Content-Type: application/json`, `Location: /v1/archive-jobs/job_demo_01`, and `X-Request-ID: req_demo_create`. Body is the Job schema in state QUEUED. HTTP 202 does not mean that the archive is ready.

Errors are 400 with application code `INVALID_INPUT`, 401 with `UNAUTHENTICATED`, or 403 with `SCOPE_REQUIRED`. The shared error schema and actions below apply. There are no documented 409, 422, or 429 responses.

## Read a job

`GET /v1/archive-jobs/{job_id}` has one required path parameter `job_id`, a non-null string matching `^job_[a-z0-9_]+$`. There are no query parameters and no request body.

HTTP 200 returns Job as JSON with `X-Request-ID`. HTTP 404 returns error code `JOB_NOT_FOUND`. Shared 401 and 403 errors also apply. Example ID is `job_demo_01`.

## List jobs

`GET /v1/archive-jobs` has no path parameters or body. Optional integer query `limit` is 1 through 50, default 10. Optional query `cursor` is an opaque non-null string. Omit cursor on the first page and send the previous `next_cursor` verbatim through URL encoding on the next page. Sort is creation time ascending, then ID ascending. A snapshot is not guaranteed across pages.

HTTP 200 returns `{"items":[<Job>],"next_cursor":null}` as JSON with `X-Request-ID`. Both fields are always present. `items` is a non-null array of Jobs and may be empty. `next_cursor` is either an opaque string or null; null means there are no more pages. A later-page illustrative cursor is `page_demo_02`. Query example `?limit=1&cursor=page_demo_02` is illustrative and not a default or observed result. Shared 400 INVALID_INPUT, 401, and 403 errors apply.

## Shared Job schema

All fields below are always present. Job is a JSON object with no additional properties.

| Field | Wire type | Null accepted | Meaning |
|---|---|---|---|
| id | string matching ^job_[a-z0-9_]+$ | No | Job identifier, response-only |
| source | object | No | Object with required non-null string collection, length 1 through 40 |
| label | string, max length 80 | Yes | Label supplied at creation, or null |
| status | enum string | No | QUEUED, RUNNING, READY, or FAILED |
| created_at | date-time string | No | Creation timestamp in UTC, example 2026-01-01T10:00:00Z |
| result_url | HTTPS URI string | Yes | Download location, populated only in READY |

QUEUED means work is waiting. It may become RUNNING. RUNNING means the archive is being built and may become READY or FAILED. READY means the archive is available and is terminal. FAILED means processing stopped and is terminal. The worker drives every transition. There is no cancellation operation, webhook, or automatic retry guarantee. Unknown enum values are not part of this contract. Clients should report an unexpected value rather than invent a transition.

Poll the read operation to observe state. No polling interval, completion deadline, download expiry, or rate-limit policy is specified. Do not invent these values. A failed job's `result_url` is null. A READY example uses `https://downloads.example.test/demo-archive.zip`. The download host is illustrative and no download request is part of this three-operation contract.

## Shared errors

Every error response has JSON `{"error":{"code":"<CODE>","message":"<TEXT>"},"request_id":"req_demo_error"}`. All shown keys are required and non-null strings except `error`, which is a required non-null object. No additional properties occur. Messages are explanatory and not stable identifiers. `X-Request-ID` repeats `request_id`.

| HTTP status | Application code | Cause | Caller action |
|---|---|---|---|
| 400 | INVALID_INPUT | Invalid body or query field | Correct the input before retrying |
| 401 | UNAUTHENTICATED | Missing or invalid token | Obtain a valid token from the integration contact |
| 403 | SCOPE_REQUIRED | Token lacks the operation's scope | Ask the integration contact for the required permission |
| 404 | JOB_NOT_FOUND | No job with that ID | Verify the ID; do not retry blindly |

No server failure envelope, backoff policy, or Retry-After behavior is specified. A schema check or fixture review does not constitute a live request.
