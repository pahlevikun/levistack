---
name: create-documentation
description: "Write docs readers can use, or find which docs a code change made wrong. Researches the code first, then writes one kind of page at a time (tutorial, how-to, reference, explanation), runs every example, and checks claims against the code. Also writes API references from an OpenAPI spec and code comments (doc comments with a one-line summary and runnable examples). Use when asked to document a feature, module, project or API, write a README or guide, add doc comments, or check whether docs are still right after a diff. Not for a repo map (codebase-learner), an MR description (write-mr-description) or prose polish (polyglot-copywriter)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: delivery
  category: delivery
  department: delivery
  related_skills:
    - diagram
    - codebase-learner
  invokes:
    - skill: diagram
      when: Docs need technical figures
    - skill: codebase-learner
      when: Module map is unknown
  tags:
    - documentation
    - docs
  capabilities:
    - feature_documentation
  languages:
    - en

---

# Create documentation

Write pages that a reader can follow, and that match the code. Research first, write second, run everything before you say done.

Peer skill: `polyglot-copywriter` cleans the wording of every page. Code, commands and paths stay exact.

## Pick the job

| The user wants | Job | Read |
|---|---|---|
| Pages for a feature, module or project | **write** | [pages.md](references/pages.md) |
| An API reference | **api** | [api-reference.md](references/api-reference.md) |
| Doc comments inside the code | **comments** | [code-comments.md](references/code-comments.md) |
| To know which docs a change made wrong | **check** | [check-after-change.md](references/check-after-change.md) |

If the request mixes jobs ("document the new endpoint and fix stale pages"), do **check** first, then **write** or **api** for the gaps.

## Rules for every job

1. **Read-only on code.** You edit docs and doc comments only. Other code stays untouched.
2. **Research before writing.** Read entry points, types, tests and config. Run the thing. For a wide area, use `codebase-learner` (explain mode) to get the picture first.
3. **One kind per page.** Never mix a tutorial, a how-to, a reference and an explanation on one page.
4. **Every example was run.** Copy output from a real run. If you could not run it, say so and mark the example "not run".
5. **No invented behavior.** Every claim traces to code, a test or a run. Private internals are not documented as public.
6. **Use the repo's own places.** Its docs folder, its README sections, its doc-comment style. If there is no docs folder, ask where pages should live.
7. **Show the file list before you write,** and write after the user agrees.
8. **Wording pass.** Run each page through `polyglot-copywriter`.

## Done when

- The user saw the page list and agreed.
- Every command ran and every link opened.
- Every claim has a source in the code, and the page cites the file where that helps.
- Each page has exactly one kind.
- For **check**: the coverage map is reported, and edits were made only after a yes.

## Related skills

- `codebase-learner`: understand an area first (explain), or write one `ARCHITECTURE.md` of what exists (summarize).
- `polyglot-copywriter`: simple words and short sentences for every page.
- `write-mr-description`: describe the change in the MR. Docs for readers of the product come here.
- `verify`: prove a documented command or claim by running it.
- `atomic-semantic-commit`: commit the docs separately from the code.
