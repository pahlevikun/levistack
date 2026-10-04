# Inline comment bodies

## Priority

1. **One finding per inline draft** on the relevant diff line.
2. Include a **GitLab suggestion** when the fix is a small, safe edit.
3. Keep the opening sentence specific (`This returns nil when…` / `Can we guard X before…?`).
4. No **summary** comment that repeats the whole review at the top of the MR.

## Suggestion block

Use GitLab markdown suggestion syntax in the body file:

````markdown
Can we return a typed error here so callers do not swallow the failure?

```suggestion
if err != nil {
    return fmt.Errorf("load config: %w", err)
}
```
````

Rules:

- Suggestion must apply to the **same line range** as the draft position.
- Do not suggest large refactors in one block; split across lines or leave prose-only.
- Code inside the fence must compile in context when possible.

## Prose

- Run comment text through **polyglot-copywriter** (`glab-code-review` use case, STE/simple — [simple-prose.md](../../../engineering/polyglot-copywriter/references/simple-prose.md)).
- Run **super-noslop** on filler phrases (`I'd suggest considering`, `It might be worth`, generic LGTM blocks).

## Severity (inline, optional)

Prefix with one token when helpful: `[must]` `[should]` `[nit]` — plain words, not emoji walls.
