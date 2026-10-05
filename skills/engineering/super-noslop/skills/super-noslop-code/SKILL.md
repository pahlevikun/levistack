---
name: super-noslop-code
description: "Code comment hygiene for super-noslop: remove generic AI-slop comments, keep valuable ones, never touch executable code. Use when the task edits comments only or after the core super-noslop filter is loaded."
metadata:
  version: "2.0.0"
---

# super-noslop-code

> No Slop: code comments skill

Part of the super-noslop system. Read with the core [`super-noslop/SKILL.md`](../../SKILL.md) and [workflow-gates.md](../../references/core/workflow-gates.md). This skill filters comments that read as generic AI (decorative, restating the obvious, stiff, loud) while preserving comments that carry real information. It cites core rules by number and never renumbers them.

Load when the task writes or edits code comments. The coordinating agent should route comment-only cleanup here after the core filter is in play.

## How to use

- Load together with the core whenever the task touches comments. The core holds purpose test, three tiers, and Delivery Gate; this file holds comment-specific depth.
- Every entry: **Tell** (pattern), **Why** (why it reads as slop), **Fix**, with governing core rule as R-XX.
- **Scope guardrail:** only comments. Never modify executable code, identifiers, imports, formatting, indentation, whitespace, control flow, or logic. When in doubt, leave the code untouched.
- Run the "Code comment checklist" alongside the core Delivery Gate.

## Comments that add nothing

### Decorative separators

- **Tell:** banners of `===`, ALL CAPS labels, box drawing around a section name.
- **Why:** decoration is the message. It signals "AI made this".
- **Fix:** one plain line, or remove if the label adds nothing (R-31).

### Restating the obvious

- **Tell:** `// Initialize the variable` above `let count = 0`, `// User class` above `class User {}`.
- **Why:** the code already says it.
- **Fix:** remove; leave the code line alone.

### Workflow narration

- **Tell:** `// Step 1: Validate input`, `// First...`, `// Finally...`.
- **Why:** control flow is visible in the code.
- **Fix:** remove. If the flow is hard to follow, that is a structure problem.

### Empty labels

- **Tell:** `// Main logic`, `// Helper function`, `// Note: This is important.`
- **Why:** names a category, not a fact.
- **Fix:** remove unless the line carries a specific constraint.

### Vague placeholders

- **Tell:** `// TODO: Improve this`, `// Additional optimization can be added here`.
- **Why:** names a feeling, not a task.
- **Fix:** remove. Keep a TODO only when it names a specific, actionable task.

### Signature echo

- **Tell:** docs that only repeat `@param price The price` for names that already say it.
- **Why:** length without understanding.
- **Fix:** keep docs that explain rules, edges, assumptions, algorithms, limitations, side effects, API behavior, or security. Never strip real documentation.

### Decorative emoji

- **Tell:** `// ✅ Validation`, `// 🚀 Performance`.
- **Why:** visual noise and the AI default vocabulary.
- **Fix:** plain English, or remove.

### End markers

- **Tell:** `} // end if`, `# End of function`.
- **Why:** the brace already ends the block.
- **Fix:** remove unless a rare long-file case prevents confusion.

## How it should read

### The over-explained comment

- **Tell:** several lines stacking history around a one-line constraint.
- **Why:** a person leaves a note; a generator writes a case.
- **Fix:** one line, two at most. Keep the platform trap, silent failure, protocol rule, or cost. Drop issue numbers and reasoning chains unless the repo requires them.

### Line-by-line narration

- **Tell:** a comment on every trivial statement.
- **Why:** none of them matter.
- **Fix:** one concise comment per logical block, or none.

### Stiff or loud wording

- **Tell:** "This function is responsible for validating whether..." or `// MAIN LOGIC`.
- **Why:** generated voice.
- **Fix:** short sentence-case: `// Validate credentials before issuing a token.` Explain why, not what.

## Not a ban (preserve these)

Never remove comments that explain business logic, architecture, security, performance, concurrency, protocol, API contracts, workarounds, edge cases, assumptions, licensing.

Example that must stay:

```js
// Stripe may retry webhook deliveries for up to three days.
// Ignore duplicate events using the event ID.
```

Value is not length. A workaround note is one line about the workaround.

## Code comment checklist

Run with the core Delivery Gate. All answers must be **yes**:

- [ ] Every comment adds information the code does not already show? (R-31)
- [ ] No decorative separators, ALL CAPS banners, or box-drawn headers?
- [ ] No restating the next line, declaration, or signature?
- [ ] No step-by-step workflow narration?
- [ ] No empty labels or vague TODOs?
- [ ] No decorative emoji or habit end markers?
- [ ] Density is one per logical block, not one per line?
- [ ] One line, or two only when the second is a new fact?
- [ ] Remaining comments short, natural, sentence case?
- [ ] Scope held: only comments changed, code untouched?

## Related skills

- `super-noslop`: the parent skill.
