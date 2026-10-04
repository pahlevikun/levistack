# Domain: API

HTTP/gRPC routes, request validation, response envelopes, status codes, OpenAPI, and webhook handlers.

## Checklist

- [ ] Validation at the trust boundary that owns the outcome (R-03, R-25).
- [ ] Stable error codes and fields — no `An error occurred` (R-02).
- [ ] Status codes match domain siblings; no `200` with empty body or noop work (R-24, R-26).
- [ ] Success payload matches existing contract — no generic `{ "message": "Success" }` (patterns).
- [ ] OpenAPI descriptions are specific to this operation — not "Returns data" (R-28).
- [ ] Idempotent retries on mutating routes use keys/upsert/outbox (R-32).
- [ ] Webhooks and async ingress validated before side effects (R-03).
- [ ] User-facing API copy: no em dash; failures name the domain (R-02).

## MR review signals

Generic errors, missing envelope, fake success, template OpenAPI — [review-dimensions.md](../../../../delivery/glab-code-review/references/review-dimensions.md) §8.
