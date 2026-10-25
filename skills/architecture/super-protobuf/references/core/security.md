# Defensive gRPC and protobuf review

Harden exposed gRPC and protobuf surfaces. **Review and hardening only.**

Do not include, invent, or complete attack procedures, exploit payloads, PoCs, interception how-tos, schema-recovery recipes, or fuzzing playbooks.

## Treat gRPC as an API

Every method is an API endpoint:

- Authenticate and authorize **per RPC**, not "the network is private."
- Internal services that become reachable (new ingress, grpc-web, mesh expose) need the same authz as public HTTP.
- Put auth in interceptors/middleware; do not rely on clients to omit forbidden fields.
- Map domain errors to gRPC status codes without leaking internals.

## Do not leak the schema

Production should not hand out the contract:

- Disable **server reflection** outside locked-down debug environments.
- Do not ship `.proto` sources, `FileDescriptorSet`, or embedded descriptor blobs in public mobile/web clients.
- Descriptor or proto files in a public repo, CDN, or JS bundle are a contract leak — treat like publishing OpenAPI without a review.
- Admin/debug UI that lists methods belongs behind the same auth as the service.

## grpc-web and HTTP/2

grpc-web rides ordinary HTTP. Apply the same TLS, CORS, auth cookies/tokens, and CSRF story you would for JSON APIs. "It is binary" is not access control.

Plain gRPC on HTTP/2 still needs TLS in production and must not skip auth because the payload is protobuf.

## Checklist (reviewers)

- [ ] Every RPC names who may call it; deny by default.
- [ ] Newly exposed "internal" services have authz before they have clients.
- [ ] Reflection off in production; descriptor endpoints gated.
- [ ] Public artifacts do not include `.proto` or descriptor sets.
- [ ] grpc-web (if any) has the same authz as the REST surface.
- [ ] Validation runs server-side (protovalidate); clients are not trusted.
- [ ] Timeouts, size limits, and cancellation exist so unbounded streams cannot stall the process.

## Related

Compatibility and mixed-version risk live in `compatibility.md` and `evolution.md`. Lint/breaking live in `style.md`. This file does not replace those.
