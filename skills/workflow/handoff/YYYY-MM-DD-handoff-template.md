# Handoff: <topic in a few words>

- **Date:** YYYY-MM-DD
- **Status:** in progress | blocked | ready for review | done
- **Project:** <name and path>
- **Branch:** `<branch>` at `<short sha>` (<clean | N uncommitted files>)
- **Links:** <issue, pull or merge request, related docs>
- **Supersedes:** <path to an older handoff, or remove this line>

## Start here

<Three lines at most. What this work is. Where it stopped. The very next action.>

## Goals

- **Goal:** <one sentence>
- **Done when:** <the checks that prove it is finished, as a short list>
- **Not in scope:** <what to leave alone>

## Context

<What a fresh session must know before it touches anything.>

- **Why:** <the reason this work exists and who asked for it>
- **Background:** <the facts, constraints, and terms the reader would not guess>
- **Where to look:** <key files and folders with one line each, relative to the project root>
- **Already tried:** <approaches that failed, and why, so nobody repeats them>

## State

- **Done:** <what works, and how you know>
- **In progress:** <what is half done, and exactly where you stopped>
- **Not started:** <what is untouched>
- **Uncommitted files:** <list, or "none">
- **Last verification:** <command, result, and when. Write "not run" if you did not run it.>
- **Unverified:** <claims or assumptions that nobody has checked>

## Checklist

Work from the first unchecked item. Keep the order.

- [x] <finished step>
- [ ] <next step, concrete enough to start now>
- [ ] <following step>
- [ ] <final check or cleanup>

## Decisions

| Decision | Why | Ruled out |
|---|---|---|
| <what was chosen> | <the reason> | <alternatives and why not> |

## Open questions

- <question> (ask: <who>) (blocks: <which checklist item>)

## Resume

```bash
# setup
<install or env commands. Names of variables only, never their values.>

# verify the state before you continue
<test, build, or run command and the result you should see>
```

## Watch-outs

- <flaky test, slow command, file that must not be touched, trap>
