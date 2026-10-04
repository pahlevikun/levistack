# Semantic commit types

```
feat: add hat wobble
^--^  ^------------^
|     |
|     +-> Summary in present tense.
|
+-------> Type: chore, docs, feat, fix, refactor, style, or test.
```

## The seven types

| Type | Meaning | Ask yourself |
|---|---|---|
| `feat` | New feature for the user, not for a build script | Can a user now do something new? |
| `fix` | Bug fix for the user, not a fix to a build script | Did something wrong become right for a user? |
| `docs` | Change to the documentation | Does the diff touch only docs or doc comments? |
| `style` | Formatting, missing semicolons. No production code change | Would the compiled behavior stay identical? Is it only whitespace or formatting? |
| `refactor` | Change to production code, such as renaming a variable. Behavior stays the same | Do the same tests pass before and after, with no new test? |
| `test` | Adding missing tests or refactoring tests. No production code change | Does the diff touch only test files? |
| `chore` | Updating tooling, tasks, dependencies. No production code change | Is it maintenance that no user sees? |

## Beyond the seven

Use these only when the repository already uses them (check `git log --oneline -30`). If it does not, use the nearest base type.

| Type | Use it for | Nearest base type |
|---|---|---|
| `perf` | A change that makes code faster or lighter | `refactor` or `feat` |
| `build` | Build system or external dependencies | `chore` |
| `ci` | CI configuration | `chore` |
| `revert` | Undoes an earlier commit | `fix` or `chore` |

## Choose the type

1. Start with the user. A change a user can see or rely on is `feat` or `fix`.
2. A change with no behavior difference is `refactor` (code), `style` (formatting) or `docs`.
3. A change to tests only is `test`. A change to tests and code for one feature is the feature's type, because the tests belong with the code.
4. A change that no user sees and that is not code is `chore`.
5. If the diff fits two types, it is two commits.

Hard cases:

| Situation | Type |
|---|---|
| Fix a typo in a user-facing message | `fix` |
| Fix a typo in a code comment | `docs` |
| Bump a dependency to patch a known vulnerability | `fix` if users are affected, else `chore` |
| Rename a private function | `refactor` |
| Run the formatter over a file | `style` |
| Add a test for a bug you fix now | `fix` (same commit) |
| Add a test for old code | `test` |
| Change `.gitignore` | `chore` |

## Scope

The scope is the context that changed. It is optional. Use one when it helps a reader scan the log.

- Use the name of a module, package, layer or feature: `auth`, `api`, `cart`, `parser`.
- Use one word, lowercase. Use the same word every time for the same context.
- Take the scope from the repository when it has a convention. Read `git log --oneline -30` first.
- Do not use a file name or a ticket number as the scope.
- Omit the scope when the change spans the whole project.

## Breaking changes

Add `!` after the type or scope, and explain in the body:

```
feat(api)!: rename /v1/orders to /v1/checkout

BREAKING CHANGE: clients on /v1/orders must move to /v1/checkout.
The old route returns 410 after 2026-06-01.
```

Always write a body for a breaking change, a security fix, a data migration and a revert.

## Examples

```
feat(auth): add OAuth2 login
fix(api): handle null response from /users
docs(readme): add install steps
style(parser): format with prettier
refactor(cart): extract price calculation
test(cart): add checkout edge cases
chore(deps): bump eslint to 9.4
```
