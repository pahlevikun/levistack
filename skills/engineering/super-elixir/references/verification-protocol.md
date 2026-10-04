# Verification protocol

Run this on **every finding** before it goes in a report. A finding that fails a gate is dropped, or downgraded to a **question** that says what was not verified.

*Written for this merged skill. The review guides (code-review, security-review, performance-review) were published pointing at a separate `review-verification-protocol` skill that was not part of the import; this file fills that role.*

## Gates, in order

1. **Location.** The finding has `path:line` (or a range) copied from the current file. The path resolves in this repo.
2. **Scope read.** You read the whole function or module section around it, not only a diff hunk or a search hit.
3. **Valid pattern check.** The code is not on the guide's *Valid Patterns (Do NOT Flag)* list, and the *Context-Sensitive Rules* condition for it is true.
4. **Category check.** The category-specific test below passes.
5. **Evidence.** The report quotes the line or attaches the artifact: the search used, the measurement, the failing output.
6. **Severity.** The label matches the table at the end. When unsure, go one level lower and say why.

## Category tests

### Unused or dead code
Search the whole repo, not only the file. Also check: callbacks of a behaviour and protocol implementations, functions called through `apply/3` or `&Mod.fun/arity`, `use`/`__using__` injected functions, templates and `.heex` files, `config/*.exs` entries, test support files, and macro-generated names. If any is possible and unchecked, report a question.

### Missing validation or authorization
Trace the data from ingress to the flagged line. Look upstream for a changeset, a plug, a schema, a context function or a guard that already enforces it. Report only if you can show a path with no check.

### Security
- Name one concrete **ingress** for any "untrusted input" claim: `conn.params`, a decoded JSON body, an uploaded path, a message from another node, a queue payload. If the value is a compile-time constant, a test fixture or internal-only, drop the finding.
- For `String.to_atom`, `binary_to_term`, `Code.eval_*`, dynamic `Module.concat`, SQL `fragment` interpolation and `Phoenix.HTML.raw`, show the value's origin.
- A hard-coded secret is a finding only if it is a real credential. Fixtures and examples are not.

### Performance
Quote the observed or measured fact that meets the guide's "Flag ONLY IF" condition (a rate, an item count, a read to write ratio, a profiler line). Otherwise write **suspected**, name what you did not measure, and keep it out of the Critical list.

### Style and idiom
Mark **N/A** for protocol purposes. Style-only items are Suggestions, never Critical, and are not reported at all when the project's formatter or linter already decides them.

### Tests
A claim that a behavior is untested needs the search you ran for the test, including tests that exercise it through a caller.

## Report format

```
[path:line] ISSUE_TITLE
Severity: Critical | Major | Minor | Suggestion
Evidence: <quoted line or artifact>
Why it matters: <one sentence>
Fix: <the smallest change that resolves it>
```

If a pass finds nothing, say so and list what you checked.

## Severity

| Level | Meaning | Examples |
|---|---|---|
| **Critical** | Exploitable or data-losing, block the merge | `Code.eval_string` on user input, `binary_to_term` without `:safe` on untrusted data, SQL built by interpolation, a real committed secret |
| **Major** | Likely bug, outage or sizable risk | an unsupervised long-lived process, a blocking call in a hot GenServer callback, a missing authorization check, N+1 on a list endpoint |
| **Minor** | Convention break with limited impact | missing `@spec` on a public function, `=` in a `with` where the value cannot fail |
| **Suggestion** | Optional improvement | naming, a clearer pipeline, a doctest |

## Do not

- Report something because it looks unusual. Report it because it fails a gate.
- Pad a report with low-value items to look thorough.
- Present a guess as a fact.
