# Writing instructions that get followed

Applies to a skill body, a subagent prompt, a command and a rule. The model reads what you wrote and nothing else, so every gap is a decision you left to it.

## Contents
- The golden rule
- Context of use
- Remove ambiguity
- Define edge cases
- Give decision criteria
- Separate must, nice and must not
- Match freedom to fragility
- Test on more than one model size
- Keep one term per concept

## The golden rule

Hand the instructions to someone with no context and ask them to follow them. Where they stop to ask a question, the model will guess. Remove your own context first (project knowledge, unstated assumptions), then add back only what a stranger would need.

## Context of use

One or two sentences on what the output is for and who reads it change the result more than extra rules.

```markdown
Weak:   Remove personal data from these messages.
Strong: Anonymize customer feedback for a quarterly review deck. Replace names with
        CUSTOMER_<n> and emails with EMAIL_<n>@example.com. Leave product names intact.
        If a message has no personal data, copy it unchanged. Output only the messages,
        separated by `---`.
```

The strong version states the purpose, the replacement rules, an exception, the empty case and the output shape.

## Remove ambiguity

Replace words that make an obligation optional or leave a condition open.

| Avoid | Write |
|---|---|
| "Try to ..." | "Always ..." or "Never ..." |
| "You should probably ..." | "Must ..." or "May optionally ..." |
| "Generally ..." | "Always ..., except when <condition>" |
| "Consider ..." | "If <condition>, do <action>" or drop it |
| "Handle errors appropriately" | "On a non-zero exit, print stderr and stop" |
| "Make sure it works" | "Run `npm test`; done when it exits 0" |

```markdown
Ambiguous: You should probably validate the output and try to fix errors.
Clear:     Run `node scripts/validate.mjs out/`. If it fails, fix the cause and run it
           again. Continue only when it prints no errors.
```

## Define edge cases

State the answer to the questions a careful reader would ask. For extraction, ask: what if nothing is found, what if there are duplicates, what if an item is malformed, what exactly is the output shape?

```markdown
Extract email addresses from the file into a JSON array of strings.
- None found: write `[]`.
- Duplicates: keep one.
- Malformed: skip it and log it to stderr.
```

## Give decision criteria

"Pick the right chart" leaves the choice to taste. Give the test for each branch.

```markdown
Use a bar chart when comparing fewer than 10 categories and exact values matter.
Use a line chart for a trend over time.
Use a scatter plot when the relationship between two variables is the point.
```

## Separate must, nice and must not

```markdown
Must have: revenue, costs, margin; at most 5 pages.
Nice to have: charts, industry benchmarks.
Must not: customer names, unexplained jargon.
```

Reserve strong modals (`ALWAYS`, `NEVER`, `ONLY`) for boundaries that cause real damage when crossed. Used everywhere they stop carrying signal.

## Match freedom to fragility

| Freedom | Use when | Write it as | Example |
|---|---|---|---|
| High | Several approaches are valid; judgment decides | Goal, criteria, a short checklist | Code review: structure, bugs, readability, conventions |
| Medium | A preferred pattern exists; some variation is fine | A template or pseudocode to adapt | A report with a default section list |
| Low | Fragile, irreversible or order-dependent | The exact command, "do not modify it" | `python scripts/migrate.py --verify --backup` |

Too much freedom on a fragile step causes failures. Too little on a creative step gives rigid, mediocre output.

## Test on more than one model size

| Size | What it needs | Failure to look for |
|---|---|---|
| Small and fast | Explicit steps, complete examples, a clear done condition | Skips steps; fills gaps with a guess |
| Mid | A balanced default with one escape hatch | Over-explains; ignores a buried rule |
| Large | Principles and constraints, little scaffolding | Follows a rigid script where judgment would do better |

Start with mid-level detail. Run the real requests on the models the skill will meet. Add steps where the small model stalls and cut text where the large one coasts. Stop when both succeed; do not tune for one.

```markdown
# Works across sizes
Use pdfplumber:
    with pdfplumber.open("file.pdf") as pdf:
        text = pdf.pages[0].extract_text()
For scanned PDFs that need OCR, use pdf2image with pytesseract instead.
```

Too thin for a small model: "Use pdfplumber". Too long for a large one: three sentences on what a PDF is.

## Keep one term per concept

Pick "endpoint" or "route", "field" or "box", "extract" or "pull", and use it everywhere, including references and examples. A reader who sees two words assumes two things. Search the finished skill for the discarded synonym.
