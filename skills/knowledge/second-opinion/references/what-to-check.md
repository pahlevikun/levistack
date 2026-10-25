# What to check

Use the lenses that fit the change. Not every lens fits every change.

## Correctness

Does the code do what the goal says it should?

- Edge cases: empty input, nil or undefined, boundary values, two callers at the same time.
- Errors: are they caught, passed up, or silently dropped?
- Off-by-one, type coercion, integer overflow, string encoding.
- State: race conditions, stale closures, references that outlive their owner.
- Do both the happy path and the failure path work?
- Idempotency: what happens if this runs twice, or if an earlier run crashed halfway? If the answer is "it depends on what was left behind", a cleanup or reconcile step is missing.
- Concurrency: if several actors can touch the same state (files, branches, shared data), is access controlled by structure (locks, ordered phases, one owner), or only by a habit that will not hold?

When you find a possible bug, trace the path. Do not just write "this could be nil". Show the call chain that makes it nil.

## Root cause or symptom

Does the code fix the real problem, or only hide a symptom?

The answer often needs code outside the changed files. Read the callers, the callees, the types and the sibling modules. Learn the design the change lives in. Use Read, Grep and Glob to follow the call chain before you judge whether the fix sits in the right layer.

- A guard clause that hides a broken rule deeper down.
- Retry logic that hides a broken contract.
- A type cast that hides a modeling mistake.
- A workaround: why is it needed, and what would the proper fix look like?
- A fix in module A that belongs in module B's contract.
- A rule written as a comment ("don't do X") or a habit someone must remember. Could it be a type, a lint rule or a runtime check that makes the wrong thing impossible?

## Structure

Does the code fit the system it is part of?

- Boundaries: is input checked once where it enters the system, then trusted inside? Or are checks scattered through the business logic?
- Level: does the code mix high-level steps with low-level detail?
- Coupling: does the change add a dependency that makes later changes harder?
- Data model: do the data structures match how the data is read and written?
- Built in or bolted on: if this need had been known from the start, would the code look like this? Or does it feel patched on?
- Old and new paths side by side: does the change add a new API and keep the old one alive? If there are no outside users, move the callers and delete the old path in the same change. Do not leave a compatibility layer that becomes permanent.

Do not mark simple code down for having no abstraction. An early abstraction is worse than some duplication.

## Verification

Can you tell from reading it that the code works?

- Are there tests? Do they test behavior, or implementation details?
- Are there assertions or invariants that would catch a regression?
- For a bug fix: is there a test that fails without the fix?
- At an integration boundary: is the whole path tested?
- Check the real thing, not a stand-in. Code that checks liveness with a file's change time or a cached value, instead of the real value, has a verification gap.
- For delegated or async work: does the code check the real output, or trust a self-report or a summary?

## Complexity budget

Is the complexity worth what the code does?

- Code that could be simpler without losing correctness or clarity.
- An abstraction with one caller.
- Configuration or parameters for cases that do not exist yet.
- Dead code, unused imports, parameters nobody uses.
- "Just in case" paths with no current caller.
- Old compatibility paths kept after the migration is done. Delete the scaffolding.
- Is the complexity worth it for the user? Every feature, control and option must earn its place. A half-finished feature is worse than a missing one.

Simpler is better, unless simpler is wrong.

## Security

For each security finding, trace the input through the code and show the path.

- User input that reaches a dangerous sink (SQL, a shell, `eval`, `innerHTML`) without sanitizing.
- New endpoints with missing authentication or authorization.
- Secrets in code, logs or error messages.
- Time-of-check to time-of-use gaps (TOCTOU) in security-critical paths.
