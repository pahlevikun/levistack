---
description: "Per-route-group security contract: identity source, constant-time secret checks, generic failures, bounded input, negative tests."
alwaysApply: false
---

# API security

For every route group, require an **approved**:
- identity source and authentication flow
- authorization model
- safe failure behavior
- request and body bounds
- transport exposure (TLS, ports)
- secret rotation path
- log redaction
- response allowlist
- **negative tests** (missing, wrong and malformed credentials)

## Rules
- Never trust caller-supplied identity headers. Never restore a removed gateway convention by inference.
- Verify static tokens by **hashing and constant-time comparison.** `==` on secrets is a timing side channel that normal tests never reveal.
- Failure responses are **generic** (`401` with no detail) and carry no stack traces, paths or internals.
- Enforce a minimum secret length and support rotation through the environment.
- Unknown routes and services fail closed.
- Responses are built from an allowlist of fields, never serialized straight from storage structs.
- Never log credentials, tokens, raw bodies, personal or financial data, SQL parameters or adapter exceptions.
- Health endpoints are unauthenticated and sensitive-data-free; everything else is authenticated.
- Preserve existing security tests (generic `401`, minimum length, rotation, response allowlists, credential-negative cases) when changing a route.
