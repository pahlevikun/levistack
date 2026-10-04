# Commit messages in Simplified Technical English

STE keeps a message short, exact and easy to read for every reader, including readers who are not native speakers. The base rules come from ASD-STE100, as applied in [ste-style.md](../../../engineering/output-savers/concise/references/ste-style.md). The commit discipline is in [commit.md](../../../engineering/output-savers/concise/references/commit.md). The vocabulary and punctuation bar is in [simple-prose.md](../../../engineering/polyglot-copywriter/references/simple-prose.md).

A commit message is not a reply. It has a fixed format, so use these rules and not the chat styles.

## Subject

| Rule | Do | Do not |
|---|---|---|
| Mood | Imperative, present tense: `add`, `fix`, `remove` | `added`, `adds`, `adding` |
| Length | 50 characters or fewer. Hard limit 72 | A subject that wraps |
| End | No period | `fix login bug.` |
| Case | Lowercase after the colon | `Fix Login Bug` |
| Size | One idea. The thing and the action | Two actions joined by `and` |
| Names | Keep identifiers exact: `fix(parser): handle empty token` | Paraphrase a function name |
| Subject | Say what changed in the product or code | List file names |

## Words

Use one common word for one meaning, and use it every time.

| Use | Instead of |
|---|---|
| `add` | `introduce`, `implement`, `create new` |
| `remove` | `delete`, `get rid of`, `drop` (unless it means drop a table) |
| `fix` | `resolve`, `address`, `patch up` |
| `change` | `modify`, `alter`, `adjust` |
| `rename`, `move`, `replace`, `extract` | `refactor stuff`, `restructure` |
| `use` | `utilize`, `leverage` |
| `check` | `validate` (unless it is input validation) |

Avoid vague words. They tell the reader nothing: `various`, `several`, `some`, `stuff`, `things`, `misc`, `etc`, `wip`, `tweak`, `minor changes`, `small fixes`, `improve`, `enhance`, `cleanup` alone.

Say what, not that:

| Weak | Strong |
|---|---|
| `fix stuff in login` | `fix(login): reject expired tokens` |
| `update dependencies` | `chore(deps): bump eslint to 9.4` |
| `improve performance` | `perf(search): cache the index per request` |
| `refactor code` | `refactor(cart): extract price calculation` |
| `misc changes` | split into real commits |
| `fixed the bug where users could not log in sometimes` | `fix(auth): retry token refresh on 401` |

## Body

Write a body only when the reason is not clear from the subject. Always write one for a breaking change, a security fix, a data migration and a revert.

- Explain **why**. The diff shows what.
- Use the active voice. Name the actor: `The cache returned stale data.`
- Use 20 words or fewer in a sentence. One fact per sentence.
- One topic per paragraph. Six sentences at most.
- Leave one blank line after the subject. Wrap at 72 characters.
- Use `-` for bullets. Put references last: `Closes #42`, `Refs #17`.
- No em dash, no en dash, no semicolon. Use a period, a colon or parentheses.
- Keep the warning first when there is one: `Run the migration before you deploy.`
- Do not write: `This commit ...`, `I`, `we`, `now`, `currently`, `as requested`.
- Do not add AI attribution. If the user's rule requires a trailer, add it as a trailer.

Before and after:

```
Before
fix(cache): Fixed an issue where the cache was sometimes returning old data
because it was not being invalidated properly when users updated their profile.

After
fix(cache): invalidate profile cache on update

The cache kept the old profile after an update. Users saw stale names.
Delete the key when the profile changes.
```

```
Before
feat: Added a new endpoint — it returns the profile; mobile needs it.

After
feat(api): add GET /users/:id/profile

The mobile client needs the profile without the full user payload.
This cuts the size of cold-launch requests.

Closes #128
```

## Language

Write in English by default. If the repository history is in another language, write in that language:

1. Keep the type words (`feat`, `fix`, ...) and the scope in English.
2. Apply the same rules in that language: short sentences, active voice, one word for one meaning.
3. Load the language pack of `polyglot-copywriter` for the register and the common words, and read its `simple-prose.md` for the grammar bar.
4. Keep code, identifiers, commands and error text unchanged.

## Check it

```bash
node scripts/check-message.mjs "fix(auth): retry token refresh on 401"
node scripts/check-message.mjs --file .git/COMMIT_EDITMSG
node scripts/check-message.mjs --range HEAD~5..HEAD
```

The script checks the format and the rules above. It cannot judge whether the message is true. A human or the agent reads the diff for that.
