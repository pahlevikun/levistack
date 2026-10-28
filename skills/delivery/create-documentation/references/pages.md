# Write pages

## Contents
- The four kinds
- Steps
- Shapes
- Do not

## The four kinds

Give each page or clearly bounded section one kind. Readers arrive with different needs. A handover packet can bind several kinds under separate headings.

| Kind | The reader wants | Shape |
|---|---|---|
| **Tutorial** | To learn by doing, with no prior knowledge | One path that works from start to end. Small steps. Show the result after each step. |
| **How-to** | To finish one goal | A numbered list for one task. Assumes the basics. |
| **Reference** | To look up a fact | Complete, dry, easy to scan. Commands, flags, config keys, routes, fields, errors, defaults. |
| **Explanation** | To understand why | Prose about the design, the trade-offs and how the parts fit. No steps. |

## Steps

1. **Scope it.** Feature, module or whole project? Who is the reader? Read the docs that exist, and do not repeat them.
2. **Study the whole thing before page one.** Read entry points, types, tests, and config. Use safe local checks or existing evidence. Do not contact production or perform destructive actions to verify prose.
3. **Plan the pages.** List what readers need, and give each need one kind. Show the list and mark the gaps.
4. **Draft one page or section at a time.** Use copyable commands and evidence-backed output. Label illustrative or unrun examples. Link across kinds: a tutorial links to the reference, a how-to links to the explanation.
5. **Clean the wording** with `polyglot-copywriter`.
6. **Verify.** Check commands safely at the available level and label those not run. Open links and check claims against their sources. Distinguish syntax, fixture, schema, and live checks.
7. **Report the file list and checks.** Write within the user's authorized scope. If the request is review-only, report the plan without editing.

## Shapes

**Tutorial**

```
# <Do the thing>
What you will build, and what you need first.
## Step 1: <action>
<command or code> then what the reader should see.
## Step 2: ...
## What you built
<where to go next: a how-to, the reference>
```

**How-to**

```
# How to <goal>
When you need this. Prerequisites.
1. <step>
2. <step>
If it fails: <the common cause and the fix>
```

**Reference**

```
# <Thing> reference
| Name | Type | Default | What it does |
```
Group by area. Keep descriptions to one line. Add one short example per entry only when the shape is not obvious.

**Explanation**

```
# Why <thing> works this way
The problem. The choice made. What it costs. What was rejected and why.
```

## Do not

- Present an unrun example as observed output.
- Mix teaching, lookup, and rationale inside one undifferentiated section.
- Document private internals as if they were public.
- Invent a folder layout when the repo already has one.
- Treat a multi-section handover packet as one undifferentiated page. Give each section one purpose and preserve navigation in the export.
