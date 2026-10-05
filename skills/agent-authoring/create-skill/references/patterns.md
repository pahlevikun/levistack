# Skill writing patterns

Short patterns to copy into a skill body. Pick the one that fits the step; do not stack them all.

## Contents
- Description examples
- Template pattern
- Examples pattern
- Workflow checklist
- Feedback loop
- Conditional workflow
- Plan, validate, execute
- Phase checkpoints
- Error recovery
- Iterative refinement
- Scripts
- Concise versus verbose

## Description examples

```yaml
description: "Extracts text and tables from PDFs, fills forms, merges files. Use when the user mentions PDFs, forms or document extraction."
description: "Analyzes spreadsheets, builds pivot tables and charts. Use when working with .xlsx or tabular data."
description: "Writes commit messages from the staged diff. Use when asked for a commit message or to review staged changes. Not for amending history."
```

Weak: "Helps with documents." It has no trigger and does not separate it from any neighbor.

## Template pattern

Strict output (a parser or a person depends on it): say "Use this exact structure" and show it.
Flexible output: say "Default format, adapt as needed" and show it. Match the wording to the real strictness.

````markdown
## Report structure
Use this exact structure:

# <Title>
## Summary
<One paragraph.>
## Findings
- <Finding with evidence>
````

## Examples pattern

When quality depends on seeing the result, give two input/output pairs rather than prose.

````markdown
Input: Added JWT login and token middleware
Output:
```
feat(auth): add JWT-based login

Add login endpoint and token validation middleware
```
````

## Workflow checklist

For multi-step work, give a checklist the agent can copy and tick, so progress survives an interruption.

````markdown
```
Progress:
- [ ] 1. Analyze the input (run scripts/analyze.mjs)
- [ ] 2. Write the mapping
- [ ] 3. Validate (run scripts/validate.mjs)
- [ ] 4. Apply
- [ ] 5. Verify the output
```
````

## Feedback loop

For quality-critical steps: run a validator, fix, repeat, and only proceed when it passes.

```markdown
1. Make the edit.
2. Run `node scripts/validate.mjs out/`.
3. If it fails: read the message, fix the cause, run it again.
4. Proceed only when it prints no errors.
```

## Conditional workflow

```markdown
1. Decide the type:
   - Creating new content: follow "Create".
   - Editing existing content: follow "Edit".
```

Keep each branch short; move long branches into one reference file each.

## Plan, validate, execute

For open-ended or irreversible work, write the plan to a file, check it, and only then act. Errors surface while they are still cheap.

```markdown
1. Analyze the input and the requirements.
2. Write every intended change to `changes.json`.
3. Run `node scripts/validate-changes.mjs changes.json`. Fix and re-run until it prints no errors.
4. Apply: `node scripts/apply-changes.mjs changes.json`.
5. Verify the output against the success criteria.
```

Use it when the operation is complex, hard to undo, or the plan can be validated on its own. The originals are never touched until step 4.

## Phase checkpoints

For long work, end each phase with a check that must pass before the next begins. A failure in phase 1 should not cost phase 3.

```markdown
Phase 1, collect (steps 1-3). Checkpoint: the data is complete. Continue only if it is.
Phase 2, process (steps 4-6). Checkpoint: the transformations validate. Continue only if they do.
Phase 3, output (steps 7-9). Checkpoint: the output file validates. Deliver only if it does.
```

At each checkpoint: run the validator, read its output, confirm there are no errors or warnings.

## Error recovery

Say what to do when something fails, including when to stop.

```markdown
If validation fails: read the message; if the input is corrupt go back to step 1 with different input; if the logic is wrong fix it and go back to step 1; if only the format is wrong fix it and re-run step 2.
If a save fails: check disk space, permissions and the path; retry once with the corrected condition.
If it still fails after 3 attempts: write down what was tried, save partial results, and report to the user. Do not keep trying the same thing.
```

Retry transient failures (network, locks, rate limits) a bounded number of times with a pause, then fall back. An unbounded retry wastes tokens and can hit limits.

## Iterative refinement

When quality improves with passes: draft, validate, refine, validate, finalize. Each validation gives specific feedback to act on; the last one must pass cleanly. Use it where perfect output matters more than speed.

## Scripts

Bundle a script when the same code would be regenerated each time, or when a step is fragile.
- Say whether the agent should **run** it (usual) or **read** it.
- Node or Python over Bash. Self-contained, clear error messages, no secrets, forward-slash paths.
- Document required packages in the skill body.
- Justify constants; do not leave unexplained numbers.

## Concise versus verbose

Good (about 50 tokens):

````markdown
## Extract PDF text
Use pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

Bad: three sentences on what a PDF is and why pdfplumber is popular before the same code. The model already knows. Cut it.

For reference files over 100 lines, start with a short contents list so a partial read still shows the scope.
