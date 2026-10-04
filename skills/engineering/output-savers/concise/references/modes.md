# Modes: levels, flavors, and job profiles

The reply style has two settings and a set of job profiles. [../../references/auto-detect.md](../../references/auto-detect.md) picks all three from the job. The user can override any of them in plain words.

## Levels

| Level | Words | What the user sees |
|-------|-------|--------------------|
| **light** | "light" | Full short sentences. Brief reasons stay. Answers use yes or no. |
| **default** | "default", or no word | The answer comes first. Status, cause, action. One fact per sentence. A reason appears only when it changes the action. |
| **heavy** | "heavy", "shortest" | Callouts only: identifiers, numbers, and commands. No explanation unless the user asks. |

The level changes how much you say. It never changes what must stay exact. See "Never compress" in [ste-style.md](ste-style.md).

## Flavors

| Flavor | Use for | Habits |
|--------|---------|--------|
| **Pilot** (default) | Questions, debugging, explanations, review, status | Status, cause, action. Affirm or negative. Readback before a critical step. |
| **Astronaut** | Runbooks, deploys, migrations, setup, rollback, incident steps | Constraints first. Numbered steps. Expected result per step. GO or NO-GO. Hold on failure. |

## Job profiles

These jobs have fixed formats. The format is the saver, so the level does not apply.

| Job | Reference |
|-----|-----------|
| Commit message | [commit.md](commit.md) |
| Code review comments | [review.md](review.md) |
| Compress a memory or instruction file | [compress.md](compress.md) (scripts in [../scripts/](../scripts/)) |
| Delegate to subagents | [crew.md](crew.md) |

## Read less as well

The reply style shortens what you write. For huge logs, big files, attachments, and long histories, shorten what you read first. See [../../references/context-hygiene.md](../../references/context-hygiene.md).

## Style and principles

| Risk | Use |
|------|-----|
| Long, padded replies | The reply style (this folder) |
| Extra files, layers, and abstractions | The principles ([../../principles/SKILL.md](../../principles/SKILL.md)) |

Both can be on at the same time. They solve different problems: too many words, and too much code.
