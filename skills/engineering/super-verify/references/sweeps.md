# Scope and sweeps

Two moments need extra care: before the first edit, when the scope is vague, and at the end of a task whose scope is "every item".

## Contents
- Confirm scope before editing
- Sweep completion

## Confirm scope before editing

A request with spatial scope ("migrate my project", "refactor the codebase", "update everywhere", "fix this across the app") has no defined scope. Imperative phrasing is not a scope. Before the first write, inspect the repository to find the real blast radius:

```bash
rg -l 'pattern' | cut -d/ -f1 | sort | uniq -c | sort -rn   # files per top-level directory
rg -l 'pattern' | xargs -n1 dirname | sort -u                # affected directories
```

- If the request and the repository structure point to one safe reading, state the assumption and proceed.
- If readings differ materially in result, show the breakdown and ask which one. Use the harness's question tool if there is one, otherwise numbered options in chat. Do not edit the disputed part while waiting.
- Skip the question for explicit file paths or one clear repository-wide reading.

## Sweep completion

When the task is *every* item in a set (a repo-wide rename, "migrate everywhere", audit every file, resolve all findings), a passing command proves it passed, not that it covered the whole set. Track coverage explicitly.

1. **Enumerate the set into a ledger** held outside version control: a session scratch path if the harness gives one, otherwise a git-ignored local directory. Never a tracked file.
2. **One row per item,** each with a disposition: `pending`, `done`, `excluded (reason)` or `blocked (evidence)`.
3. **Complete means zero `pending` and zero `blocked`.** "I covered a lot of them" is not a disposition.
4. **Re-enumerate after any move or rename,** so items created or relocated mid-sweep join the list instead of falling outside it.
5. **Keep removed items in the ledger** until they are explicitly accounted for. An item that silently disappears looks the same as one that was finished.

Never claim coverage the ledger does not show.
