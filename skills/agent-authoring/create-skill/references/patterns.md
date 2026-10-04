# Skill writing patterns

Short patterns to copy into a skill body. Pick the one that fits the step; do not stack them all.

## Contents
- Description examples
- Template pattern
- Examples pattern
- Workflow checklist
- Feedback loop
- Conditional workflow
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
