---
name: write-mr-description
description: Open a draft Merge Request with a generated description, self-review it, or both. Scans commits on the current branch since divergence from the target. Use when the user says "write MR description", "open MR", "raise MR", "draft MR", "review my MR", "self-review", "MR template", "PR description", "summarize my branch", or "describe these commits". Works with GitLab (glab) and GitHub (gh). Optimized for self-hosted GitLab (e.g. source.golabs.io) repos with JIRA tickets and conventional-commit prefixes.
disable-model-invocation: true
---

# Write MR Description

Peer skills: [`polyglot-copywriter`](../../engineering/polyglot-copywriter/SKILL.md) (STE simple vocabulary), [`super-noslop`](../../engineering/super-noslop/SKILL.md) (slop-free description), [`glab-code-review`](../glab-code-review/SKILL.md) (GitLab draft review after open).

References: [references/prose-and-visuals.md](references/prose-and-visuals.md), [TEMPLATE.md](TEMPLATE.md), [EXAMPLES.md](EXAMPLES.md), [samples/description-with-diagram.md](samples/description-with-diagram.md).

## Routing

Determine the user's intent and pick one route:

| User says | Route |
|---|---|
| "write MR description", "fill MR template", "describe my branch", "summarize my branch" | **A — Description only** |
| "open MR", "raise MR", "push and open MR", "draft MR", "create MR" | **B — Open draft MR** (runs A first, then pushes + opens) |
| "review my MR", "self-review", "review the MR" | **C — Self-review only** |
| "open MR and review", "raise MR then review", "create MR description and do self review" | **B + C** (open draft, then self-review) |

If ambiguous, use AskQuestion:

```
"What would you like me to do?"
Options:
- "Generate the MR description only (I'll paste it myself)"
- "Push + open a draft MR with the description"
- "Self-review an already-open MR"
- "Push + open a draft MR, then self-review it"
```

---

## Route A — Generate MR description

### A.1 Ask target branch

Detect default:

```bash
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||'
```

Fallback: try `origin/main`, then `origin/master`. Then ask:

```
"Which branch should this MR target?"
Options: [<detected>, "main", "master", "develop", "Let me type it"]
```

If HEAD is already on the target, stop — ask the user to switch to a feature branch.

### A.2 Discover commits

```bash
git rev-parse --abbrev-ref HEAD
git merge-base HEAD origin/<target>
git log --no-merges --reverse --format='%H%x09%s%x09%an' <merge-base>..HEAD
```

If empty, stop.

### A.3 Extract diff signals

For each commit, run `git show --stat <hash>` and `git show <hash> -- <focused paths>`:

- `**/errors/*.go` — error codes / status changes
- `**/task/*.go`, `**/handler/*.go`, `**/workflow.go` — HTTP behaviour
- `**/model/*.go` — request/response fields
- `clients/<service>/*.go` (not `mock/`) — client methods
- `CHANGELOG.md`

Build a signal table:

| Signal | Pattern | Surfaces as |
|---|---|---|
| JIRA ticket | `[A-Z]+-\d+` in subject/branch | `Closes [TICKET]` |
| New error code | `+.*Err\w+.*serviceError\.New` | Table row **NEW** |
| Status code flip | same Err block, `-http.Status*` → `+http.Status*` | `400 → 422` |
| New required header | new `headers.Get("...")` + error return | Breaking + curl |
| New constant | exported `const` in model/config | Bullet |
| New route | `r.Methods(...).Path(...)` | curl |
| CHANGELOG | diff under `## Unreleased` | tick box |

### A.4 Authors + tickets

- Authors from `git log --format='%an <%ae>'`, dedupe. Email `local.part` → `@handle`.
- Tickets from subjects + branch. Most-mentioned = `Closes`; rest = `Related`.

### A.5 Render

Fill the template from [TEMPLATE.md](TEMPLATE.md). Checkbox rules:

- `static_checks` → always unchecked
- `CHANGELOG` → checked only if diff proves it
- `tests` → checked if `_test.go` changes exist for every new task

**Required:** include a **mermaid diagram or scope table** in `### Description` so readers see change boundaries ([prose-and-visuals.md](references/prose-and-visuals.md)).

### A.6 Prose gate

1. **polyglot-copywriter** — English, `register: santai`, [simple-prose.md](../../engineering/polyglot-copywriter/references/simple-prose.md) on summary bullets and narrative (not on code literals or ticket URLs).
2. **super-noslop** — after pass on the full description markdown ([super-noslop § write-mr-description](../../engineering/super-noslop/SKILL.md)).

Output as a single fenced markdown block, then list up to 3 follow-up bullets (missing CHANGELOG line, stale docs, 💥 justification, missing diagram/table).

---

## Route B — Open draft MR

Prerequisite: run **Route A** first to produce the description.

### B.1 Push

```bash
git push -u origin HEAD
```

### B.2 Detect platform

| Remote contains | CLI |
|---|---|
| `source.golabs.io` or `gitlab` | `glab` |
| `github.com` | `gh` |

### B.3 Create draft

**GitLab:**

```bash
glab mr create \
  --draft \
  --target-branch <target> \
  --title "<prefix>(<scope>): [<TICKET>] <summary>" \
  --description "$(cat <<'EOF'
<description from Route A>
EOF
)"
```

**GitHub:**

```bash
gh pr create \
  --draft \
  --base <target> \
  --title "<title>" \
  --body "$(cat <<'EOF'
<description from Route A>
EOF
)"
```

### B.4 Confirm

Print the MR/PR URL. If the user chose **B + C**, proceed to Route C.

---

## Route C — Self-review

Can run standalone (on an already-open MR) or after Route B. For GitLab **draft inline review** with suggestions, prefer loading [`glab-code-review`](../glab-code-review/SKILL.md) instead of only this checklist.

### C.1 Get the diff

```bash
git diff origin/<target>...HEAD
```

If the target isn't known (standalone invocation), detect it:

```bash
glab mr view --json targetBranch -q .targetBranch   # GitLab
gh pr view --json baseRefName -q .baseRefName       # GitHub
```

### C.2 Review dimensions

Scan the diff for:

1. **Correctness** — logic bugs, nil derefs, unreachable code
2. **Error handling** — bare `errors.New` (should be typed), swallowed errors, wrong status
3. **Tests** — new task without `_test.go`, missing table rows for new branches
4. **Style** — gci import order, missing package doc, wrong export visibility
5. **Docs/contracts** — stale README, test/data fixtures listing old codes, curl with wrong headers
6. **Breaking impact** — is 💥 warranted and documented?
7. **Dead code** — unused imports, commented blocks, duplicate conditions

### C.3 Present findings

Output:

```markdown
## Self-review findings

| # | Sev | File:Line | Finding |
|---|---|---|---|
| 1 | 🔴 | task/verification_check.go:145 | ... |
| 2 | 🟡 | model/model.go:52 | ... |
| 3 | 🟢 | api_test.go:304 | ... |
```

Severity:
- 🔴 **Critical** — must fix before review
- 🟡 **Suggestion** — reviewer would likely comment
- 🟢 **Nitpick** — optional

Then ask:

```
Which findings should I fix? (numbers, "all", or "none")
```

### C.4 Implement fixes

For each selected finding:

1. Make the change
2. Run `go test -race -count=1 ./<package>/...`
3. Commit: `fix(<scope>): address self-review finding #N — <one-liner>`

After all fixes:

```
Fixes applied. Push to update the draft MR? (yes/no)
```

If yes: `git push`

---

## Heuristics

- Status code changes → table row, not paragraph.
- Quote error messages verbatim from the diff.
- Curl headers from `headers.Get(...)` calls in the diff, not memory.
- Multi-commit branches → group by intent.
- Single-commit → still re-extract signals from diff.

## Anti-patterns

- ❌ Raw `git log` in description.
- ❌ Authors from chat context instead of `git log`.
- ❌ CHANGELOG box checked without proof.
- ❌ Extra sections the template doesn't have.
- ❌ 💥 for internal-only refactors.
- ❌ Non-draft MR. Always draft first.
- ❌ Self-review that just says "LGTM".
- ❌ Committing fixes without running tests.

## Resources

- [TEMPLATE.md](TEMPLATE.md) — MR template skeleton
- [EXAMPLES.md](EXAMPLES.md) — worked example
- [references/prose-and-visuals.md](references/prose-and-visuals.md) — STE, noslop, mermaid/table
- [samples/description-with-diagram.md](samples/description-with-diagram.md)

## Related skills

- `atomic-semantic-commit`: the branch has mixed changes, split commits first.
- `glab-code-review`: self-review the diff before you open the MR.
- `super-verify`: prove the test plan before you write it down.
- `create-jira-story`: the MR needs a linked ticket.
- `polyglot-copywriter`: polish the final wording.
