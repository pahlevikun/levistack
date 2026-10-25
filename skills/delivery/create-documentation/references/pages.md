# Write pages

## Contents
- The four kinds
- Steps
- Shapes
- Do not

## The four kinds

Every page is exactly one kind. Readers arrive with different needs.

| Kind | The reader wants | Shape |
|---|---|---|
| **Tutorial** | To learn by doing, with no prior knowledge | One path that works from start to end. Small steps. Show the result after each step. |
| **How-to** | To finish one goal | A numbered list for one task. Assumes the basics. |
| **Reference** | To look up a fact | Complete, dry, easy to scan. Commands, flags, config keys, routes, fields, errors, defaults. |
| **Explanation** | To understand why | Prose about the design, the trade-offs and how the parts fit. No steps. |

## Steps

1. **Scope it.** Feature, module or whole project? Who is the reader? Read the docs that exist, and do not repeat them.
2. **Study the whole thing before page one.** Entry points, types, tests, config. Run it.
3. **Plan the pages.** List what readers need, and give each need one kind. Show the list and mark the gaps.
4. **Draft one page at a time.** One kind per page. Copy-paste commands. Real output. Link across kinds: a tutorial links to the reference, a how-to links to the explanation.
5. **Clean the wording** with `polyglot-copywriter`.
6. **Verify.** Run every command. Open every link. Check every claim against the code.
7. **Show the file list,** then write.

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

- Paste an example you did not run.
- Put a tutorial, a reference and an explanation on one page.
- Document private internals as if they were public.
- Invent a folder layout when the repo already has one.
