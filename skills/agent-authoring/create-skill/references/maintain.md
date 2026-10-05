# Test, verify and repair skills

## Contents
- Evaluate before you write
- Two-session development
- What to observe
- Metrics
- Verify that the facts are still true
- Heal a skill after a bad run

## Evaluate before you write

Documenting an imagined problem produces a skill nobody needs. Order the work around evidence.

1. **Find the gap.** Run the agent on 3 representative tasks with no skill. Write down what it got wrong or had to be told.
2. **Write the evaluations**, one per gap, plus one near-miss that should not trigger the skill.
3. **Set the baseline.** Record how the agent does without the skill.
4. **Write the minimum** that closes the gaps.
5. **Run, compare, refine.** Change one thing per iteration.

A portable evaluation record:

```json
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Reads the PDF with an appropriate library",
    "Extracts text from every page",
    "Writes readable text to output.txt"
  ]
}
```

Keep these in the repo next to the skill. They are the regression suite for the next edit.

## Two-session development

Use one session to write and one to use.

- **Author session:** finish a real task with the agent, noting what you had to repeat. Ask it to capture that pattern as a skill. Cut anything it explains that a model already knows. Organize for progressive disclosure.
- **User session:** a fresh agent with only the skill runs real tasks. Do not coach it.
- **Back to the author** with what the user session did, not with what you assumed. Apply, retest, repeat.

Models read the skill format natively, so asking for a first draft is fine. Judgment about what to cut stays with you.

## What to observe

| Observation | It usually means |
|---|---|
| It opens files in an unexpected order | The structure is not intuitive; the table of routes is unclear |
| It misses a connection between files | A link needs to be explicit, or the content belongs in `SKILL.md` |
| It leans on one reference every time | Move that content into the body |
| It never opens a file | The file is poorly signalled or unnecessary |
| It does not load the skill at all | The description lacks the user's words |
| It loads the skill for the wrong task | The description is too broad; add "Not for ..." |
| It follows the steps but the output is wrong | The output shape is missing; add a template or example |

## Metrics

Pick one or two. Measure before and after each change.

- **Success rate:** share of tasks finished correctly.
- **Discovery rate:** share of matching requests that load the skill, and share of unrelated ones that do not.
- **Iterations:** how many attempts to reach a correct result.
- **Tokens:** average per task. A rise without a quality gain means bloat.
- **Error rate** and the type of the most common error.

Small, frequent edits beat large rewrites: you can see which change moved which number, and you can revert one.

## Verify that the facts are still true

Linting checks structure. Verification checks truth. A skill makes claims about APIs, CLIs, frameworks and services, and those drift.

1. **Classify by what it depends on** and choose the check:

   | Depends on | Check by |
   |---|---|
   | A service or API | The official docs and changelog; a search for breaking changes |
   | A command-line tool | `command -v <tool>`, `<tool> --version`, `<tool> --help` for each documented flag |
   | A framework or library | Its current docs for each pattern the skill uses |
   | An integration of several | Each part, then the join |
   | Pure process | Nothing external; reread for internal consistency |

2. **Extract the verifiable claims:** tool names and flags, endpoints and auth methods, versions, file paths and config locations, documented output.
3. **Check each one** with the method above. Prefer the primary source. A claim you could not check is "unverified", not "fine".
4. **Report** in four groups: verified current (with the evidence), possibly outdated (what changed), broken (what it should say), could not verify (why).
5. **Offer the edit** and stamp the file with the date checked ("Verified 2026-10-05 against <source>"). Undated claims decay silently.
6. **Suggest when to check again:** an API or service every one to two months, a framework every three to six, a CLI about twice a year, a pure process yearly.

A confident negative ("X is not possible", "Y is the only way") needs an official source. "I did not find it" is not the same as "it does not exist".

## Heal a skill after a bad run

When a run exposed a wrong instruction (an outdated flag, a missing step, a bad assumption), fix the skill while the evidence is fresh.

1. **Identify the skill** that was running. If unclear, ask.
2. **Reflect:** which text was wrong (quote it), how the correct answer was found (docs, an error, trial), the root cause (outdated, missing context, wrong assumption), and what else shares it (other sections, references, scripts).
3. **Propose** each change as before and after, with the reason and the failure it prevents. List every file touched.
4. **Wait for approval.** No edits first.
5. **Apply**, then read each edited section back and check that examples in `SKILL.md` still match the references.
6. **Re-run** the request that failed, plus one that should still work.
7. Commit only if the user asks.
