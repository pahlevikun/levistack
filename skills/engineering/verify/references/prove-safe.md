# Prove it is safe

Use this when someone says "this change is safe", or asks "what could this break?". Also use it on a small diff you do not trust yet.

`proof-by-change.md` has a short checklist for the "before you say done" moment. This file goes deeper. It is for when the claim itself is "safe".

## Contents
- The idea
- Proof grades
- Four moves
- Blind spots
- The proof script
- Answer format
- Do not

## The idea

A change that looks risky is usually safe for one reason. Find that reason. Then prove it by running real code.

A written explanation does not count as proof. It reads well whether it is true or not. Listing callers does not count either, because a search does that in seconds. You are looking for the damage a search cannot show.

## Proof grades

Give every fact a grade. Write the grade next to it.

| Grade | Meaning |
|---|---|
| **Said** | You claim it. No evidence. |
| **Read** | You point at real code: a `file:line`, or the library's own source at the version we pin. Or you walk the failure step by step and show it cannot happen. |
| **Ran** | A script or test calls the real code. It fails loudly if the fact is false. |

Said is never enough. Aim for Ran when it is cheap. If you also watched it work in the running app, add "seen live".

## Four moves

1. **Pin the change.** What does the code do now that it did not do before? Include side effects the diff does not show.
2. **Name the keystone.** Finish this sentence: "This is safe because ...". One fact. If it holds, most of the scary cases are gone. Put your time here, not into a long list of maybes.
3. **Hunt the blind spots.** Use the list below.
4. **Prove the keystone.** Run a script. Then rank the leftover risks by how likely and how costly they are.

## Blind spots

| Where | Look for |
|---|---|
| Outside the repo | The library's real code and version. Local patches. Vendored copies. |
| In time | Order of async work, retries, timeouts, shutdown and teardown. |
| In data | Rows already stored. API payloads. Files written by an older version. Another language reading the same bytes. |
| In config | Feature flags, environment variables, defaults that differ per environment. |
| Far away | Callers many hops out. Generated code. Background jobs. Dashboards and alerts that read the output. |

## The proof script

- Keep it in a scratch place outside the repo, or delete it after. Keep it only if the user wants it as a test.
- It must exit with an error when the fact is false. If it is cheap, feed it one bad input first and watch it fail. Then you know it can fail.
- Print the library version it used. A proof on the wrong version proves nothing.
- Only read from shared systems. Ask before you touch anything in production. If the proof needs a write, give the user the command and stop.

## Answer format

```
Verdict: safe | safe if <condition> | not safe | unproven
Keystone: <the fact> (grade: <Said|Read|Ran>, proof: <command and result>)
Risks, worst first:
  - <how it breaks> at <file:line>. Chance: <low|medium|high>. Cost: <low|medium|high>. Check: <how>
Cleared: <what you checked, and why it is fine>
Before merge: <the cheapest check that would catch the real bug>
```

## Do not

- Give a long list of maybes. Rank them and prove the one that matters.
- Invent callers, endpoints or library behavior. A search that finds nothing is an answer. Say what you searched.
- Stop at Read when Ran is cheap.
- Call a change safe because the tests pass. Tests only cover what they run.
- Review a wide change alone. Ask `second-opinion` for reviewers on different models, and hand them this answer as context.
