---
name: create-readme
description: "Write or refresh a project README. Say what the project is, who it is for, how to install it, and how to run it. Add a changelog section only when asked. Use when the user says write a README, update the README, or explain how to install and run this project. Not for an API handover or feature doc (create-documentation), release notes from commits (write-changelog), or prose polish alone (polyglot-copywriter)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: delivery
  category: delivery
  department: delivery
  related_skills:
    - create-documentation
    - write-changelog
    - polyglot-copywriter
    - codebase-learner
  invokes:
    - skill: write-changelog
      when: They ask for a changelog section and the repo has no unreleased notes
  tags:
    - readme
    - install
    - changelog
  capabilities:
    - project_readme
  languages:
    - en

---

# Create a README

Write the project README a new reader needs. Read the repo first. Do not invent commands, versions, or features.

## Steps

1. Read the existing `README.md` if there is one, plus the manifest (`package.json`, `pyproject.toml`, `go.mod`, or the equivalent) and the real run commands.
2. Draft these sections, in this order. Drop a section that the repo does not support.
   - What it is, in one or two sentences.
   - Who it is for.
   - How to install it, with the commands the repo actually uses.
   - How to run it, including the check command if one exists.
   - How to configure it, only when a real config file or env name exists. Do not invent secrets.
3. When they ask for a changelog section, summarize the unreleased notes already in the repo. If none exist, say so and point at `write-changelog`. Do not invent versions.
4. Show the draft. Wait for a yes before you replace `README.md`.
5. After they say yes, write the file. Keep links and commands exact.

## Related skills

- `create-documentation`: feature docs and API handovers. Not the project README.
- `write-changelog`: release notes from commits.
- `polyglot-copywriter`: plain words after the facts are settled.
- `codebase-learner`: how the code works, when the README would otherwise guess.

## Done when

- The README matches commands and features that exist in the repo.
- A changelog section appears only when they asked.
- Nothing was written before a yes.
- [evals/evals.json](evals/evals.json) covers a new README, a refresh, and a request that is not a README.
