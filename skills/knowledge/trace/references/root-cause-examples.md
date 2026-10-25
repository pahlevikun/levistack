# Root-cause examples

Illustrations of the shape only. The systems, numbers and files are made up. In a real run, every Evidence line cites something you actually read.

## Example 1: production bug

```
Problem: users see a 500 error on checkout
Where: checkout API, production
When: since Tuesday's deploy, about 3% of checkouts
Impact: lost orders
Evidence: error tracking issue "PaymentTimeout", first seen Tue 14:02

Why 1: the payment service throws an exception
  Evidence: stack trace in the error tracking issue
  Tier: Direct
Why 2: the request times out after 30 seconds
  Evidence: client timeout = 30s in config/payment.yml
  Tier: Direct
Why 3: a database query in the payment path takes 45 seconds
  Evidence: slow-query log, incident window
  Tier: Direct
Why 4: the transactions table has no index for that query
  Evidence: EXPLAIN shows a sequential scan on transactions
  Tier: Direct
Why 5: the index was not in the migration that added the query
  Evidence: the migration in commit a1b2c3 adds the column but no index
  Tier: Direct
Root cause: migration review does not check query performance
  Evidence: the PR template has no query-plan item, and two other migrations this quarter also shipped without indexes
  Tier: Supported
```

Checks: the backward read holds. Counterfactual: with a query-plan check in review, the missing index would have been caught. Timeline: commit a1b2c3 deployed Tue 13:40, first error 14:02. Competing chain: "the payment provider was slow" lost, because outbound latency was normal.

```
Fix: add a query-plan check to the migration PR template and a CI step that runs EXPLAIN on new queries
Containment: add the missing index now
Verify by: p99 of the query under 100 ms, zero PaymentTimeout errors for 24 h
Watch for recurrence: alert on slow queries over 1 s in the payment path
```

## Example 2: flaky CI

```
Problem: end-to-end tests fail now and then
Why 1: a race in the async test setup
Why 2: the test does not wait for the database seed to finish
Why 3: the seed function does not return its promise
Why 4: TypeScript did not catch the missing return type
Why 5: strict mode is off in the test config
Root cause: the TypeScript config differs between src and tests
```

Scope check: search the other `tsconfig*.json` files. If more of them have strict mode off, the root cause is confirmed for all of them.

```
Fix: one shared TypeScript config, with strict mode on everywhere
Verify by: 50 CI runs in a row with no flake
Watch for recurrence: track the flaky-test rate per week
```

## Example 3: two branches

```
Problem: a feature deploy takes 2 hours

Branch A (build):
Why 1: the Docker build takes 90 minutes
Why 2: no layer cache is used
Why 3: dependencies are reinstalled every time
Why 4: the cache is invalidated by a timestamp in the Dockerfile
Root cause A: the Dockerfile uses the current time for versioning

Branch B (tests):
Why 1: the test suite takes 30 minutes
Why 2: integration tests run one after another
Why 3: the test runner config has maxWorkers: 1
Why 4: a developer turned off parallel runs because of flaky tests
Root cause B: flaky tests were hidden by turning off parallel runs
```

Branch B hits the human-error rule at Why 4. Ask: why was turning parallelism off possible without a follow-up (no ticket, no owner)? Why was it not caught (no test-duration alert)?

These are independent causes, so each needs its own fix:

```
Fix A: drop the timestamp, version with the git SHA
Fix B: fix the flaky tests, then turn parallel runs back on
Verify by: a deploy under 30 minutes, with the cache hit rate shown in the build log
Watch for recurrence: alert when a deploy takes over 45 minutes
```
