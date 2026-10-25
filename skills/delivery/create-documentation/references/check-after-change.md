# Check docs after a change

Use this after a diff, a branch or a release: "are the docs still right?"

## Steps

1. **Get the diff:** `git diff <base>...HEAD`.
2. **List what a reader can see that changed:** commands, flags, config keys, environment variables, API routes and fields, error messages, defaults, behavior.
3. **Search the docs** for each item (`rg '<name>' docs README*`).
4. **Build a coverage map** with three groups:
   - **Correct:** documented and still true.
   - **Stale:** documented, but the change made it wrong. Give file and line.
   - **Missing:** new, and nobody documented it.
5. **Report the map.** Offer to fix it. Edit only after a yes.
6. Fix with the **write**, **api** or **comments** job, one kind per page.

## Report shape

```
Stale:   docs/cli.md:42 says --out defaults to ./dist, code now uses ./build (src/cli.ts:18)
Missing: new flag --dry-run (src/cli.ts:31)
Correct: 11 items
```

A clean map is a result too: say "no docs affected" and list what you searched.
