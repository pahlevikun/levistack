# Mode: review-compat

Review a proto/gRPC diff as a long-lived contract.

## Steps

1. Load `compatibility.md`. Establish encoding, storage, consumers, and deploy order — or state assumptions.
2. Inventory changes by fully qualified symbol (fields, enums, RPCs, options).
3. Score each symbol on binary, JSON/text, generated source, and behavior.
4. Walk mixed-version paths in `evolution.md` (old→new, new→old, RMW, rollback, stored bytes).
5. Run the repo's checks: `buf lint`, `buf breaking --against '.git#branch=main'` (or the Makefile wrap). Do not claim a check passed unless you ran it.
6. Emit a verdict: Compatible / Rollout-dependent / Breaking / Insufficient context, plus findings in the shape from `compatibility.md`.
7. Use `review-checklist.md` for validation and docs nits; those are not compatibility blockers unless they change the contract.

## Do not

- Call a change safe from the new file alone.
- Treat `buf breaking` green as enough when payloads are stored.
- Turn style opinions into compatibility findings.

## Done when

The review has a verdict, an envelope, and remediations or a rollout sequence.
