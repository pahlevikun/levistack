# Evidence report

Use when the reader cannot see the commands you ran, or the claim is ship-level. Delete any line that has nothing to say. Do not pad.

```
Claim: <the specific claim, e.g. "the retry fix works and the suite is green">

Evidence (run after the last change):
- <check>: `<command>` -> <exit code, executed/passed/failed/skipped, key line>
- <check>: `<command>` -> <result>

Covers: <the requirement or failure path the evidence addresses>
Not checked: <skipped, unavailable or out-of-scope items, and why>
Proof kind: <live | fixture or mock | read the diff only>
Residual risk: <material risk only>
```

Example:

```
Claim: the duplicate-invoice bug is fixed and nothing else regressed.

Evidence (run after the last change):
- Reproduction: `./repro.sh` -> exit 0, no duplicate row (failed before the fix)
- Full suite: `mix test` -> 412 tests, 0 failures, 3 skipped (same 3 skipped on base)
- Build and format: `mix compile --warnings-as-errors && mix format --check-formatted` -> exit 0

Covers: the reported double submit, and one retry after a timeout.
Not checked: the production queue (no access); the retry path under real broker latency.
Proof kind: live against the local database; broker is stubbed.
Residual risk: duplicate protection is untested against a real broker redelivery.
```
