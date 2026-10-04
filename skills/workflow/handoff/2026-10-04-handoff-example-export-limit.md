# Handoff: rate limiting for the export API

- **Date:** 2026-10-04
- **Status:** in progress
- **Project:** acme-api (`~/code/acme-api`)
- **Branch:** `feat/export-rate-limit` at `a1b2c3d` (2 uncommitted files)
- **Links:** issue #214, pull request #231 (draft)

## Start here

We are adding a per-user rate limit to `POST /v1/exports`. The limiter and its config work. The 429 response is not done and the tests for it are not written. Next: return the `Retry-After` header in `src/exports/limiter.ts`.

## Goals

- **Goal:** one user cannot start more than 10 exports per minute.
- **Done when:** the limit works for one user and for many users at once, the response is a 429 with `Retry-After`, `npm test` passes, and the API docs list the new response.
- **Not in scope:** limits on other endpoints, and a shared Redis limiter (see Decisions).

## Context

- **Why:** two users started hundreds of exports last week and slowed the queue for everyone (issue #214).
- **Background:** the export queue has one worker pool. The API runs as 3 identical instances behind a load balancer.
- **Where to look:**
  - `src/exports/limiter.ts`: the new limiter (token bucket, in memory).
  - `src/exports/routes.ts`: the route that calls the limiter.
  - `config/limits.json`: the limit values.
- **Already tried:** a fixed window counter. It allowed bursts of 20 at the window edge, so we dropped it.

## State

- **Done:** the limiter and the config load. The limit blocks the 11th call in a minute (unit test passes).
- **In progress:** the route calls the limiter, but a blocked call returns a plain 500. This is where I stopped.
- **Not started:** the 429 body, `Retry-After`, the docs.
- **Uncommitted files:** `src/exports/limiter.ts`, `src/exports/routes.ts`
- **Last verification:** `npm test -- limiter` passed (4 tests) on 2026-10-04. The full suite was not run.
- **Unverified:** whether three instances behind the load balancer multiply the limit by 3.

## Checklist

Work from the first unchecked item. Keep the order.

- [x] Add the token bucket limiter and its unit tests
- [x] Load the limit from `config/limits.json`
- [ ] Return a 429 with a `Retry-After` header when blocked (`src/exports/routes.ts`)
- [ ] Add an integration test for the 429 and the header
- [ ] Decide how to handle 3 instances (see Open questions)
- [ ] Run the full suite, then update `docs/api/exports.md`

## Decisions

| Decision | Why | Ruled out |
|---|---|---|
| Token bucket, 10 per minute | Allows short bursts but caps the average | Fixed window: bursts at the window edge |
| In-memory limiter for now | No new dependency, and the pull request stays small | Redis limiter: needs infra and a new dependency |

## Open questions

- Is a limit of up to 30 per minute across 3 instances acceptable? (ask: the product owner) (blocks: the instance decision)

## Resume

```bash
npm install
git switch feat/export-rate-limit
npm test -- limiter      # expect: 4 passing
```

## Watch-outs

- `tests/exports.e2e.test.ts` is slow (about 90 seconds). Run it last.
- Do not change `config/limits.json` keys. The deploy tooling reads them.
