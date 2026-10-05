---
name: super-tech-blueprint
description: "Choose or generate a target technology stack: compare frameworks with TCO, security and ecosystem scoring, plan a migration, or write a blueprint for a new or next system. Use when comparing X vs Y, picking a framework, estimating migration cost, or producing a stack blueprint for greenfield or a target architecture. Not for documenting or diagnosing an existing codebase — use super-codebase-learner."
when_to_use: "Use when the user asks to compare frameworks, pick a stack, estimate TCO or migration cost, assess ecosystem health or security of a candidate, or generate a technology blueprint for a new or next system."
metadata:
  version: "1.1.0"
---

# Super Tech Blueprint

Answers **what should we build with / migrate toward?** Target, greenfield, and stack choice. One skill, two specialities. Call it once. It picks the speciality from the job and loads only that guide.

**Not for** documenting what a repo uses today, writing `ARCHITECTURE.md` of existing code, or diagnosing current module smells — use `super-codebase-learner`. After a current-state map exists, this skill owns the *target*.

The guides are kept whole. Each is a full, separate skill that was merged in.

## Step 0: detect the job

Do this first and do not announce it.

| If the user is doing this | Speciality | Load |
|---|---|---|
| What stack this repo uses, architecture docs of existing code, onboarding, current smells | **not this skill** | `super-codebase-learner` |
| Comparing technologies, scoring ecosystem health, assessing security posture, estimating TCO | evaluate | [stack-evaluator](specialities/stack-evaluator/GUIDE.md) |
| Greenfield or *next* system: stack blueprint, templates, target diagrams | blueprint | [blueprint-generator](specialities/blueprint-generator/GUIDE.md) |
| "Should we move off our current stack" / migrate | learner first (current), then evaluate, then blueprint (target) | sibling, then both, in order |
| Target architecture from a current-state diagnosis | blueprint, using the diagnosis as constraints | [target-from-current](references/target-from-current.md), then blueprint |

The evaluator ships Python scripts and sample inputs. Run them from `specialities/stack-evaluator/`, for example `python scripts/stack_comparator.py --help`. If Python is unavailable, follow the guide's workflows by hand and say so.

## Pipeline: from current facts to a target pick

1. **Current state (sibling).** If a repo exists and facts are missing, load `super-codebase-learner`. Do not re-inventory the tree here.
2. **Evaluate.** [stack-evaluator](specialities/stack-evaluator/GUIDE.md) with current-state as the baseline plus the user's constraints (team skills, budget, compliance, time).
3. **Blueprint the target.** [blueprint-generator](specialities/blueprint-generator/GUIDE.md) for the *next* stack: versions to adopt, patterns to require, templates for new code. How to consume a diagnosis: [target-from-current](references/target-from-current.md).
4. **Report.** One recommendation with the evidence behind it, the confidence level, and what would change the answer.

## Rules that hold across both guides

1. **Facts from the sibling (or the user), estimates labeled.** Detected versions and patterns come from learner output or the user; costs, team size and traffic come from the user or are labeled as assumptions. Do not present a guessed current stack as a scan of this skill.
2. **Say how sure you are.** Mark anything inferred rather than read, and any score built on missing data.
3. **Recommend, do not survey.** End with one pick and the deciding reasons, not a table of equal options.
4. **Do not invent current-state docs.** `ARCHITECTURE.md`, onboarding guides, and smell reports are learner deliverables.

## Bundled helpers (stack-evaluator)

Run from `specialities/stack-evaluator/`. `format_detector.py` detects the input format and `report_generator.py` renders the final report; both are called by the other scripts. The `assets/` JSON files are sample inputs (`sample_input_structured.json`, `sample_input_text.json`) and an expected output (`expected_output_comparison.json`) for trying the scripts.

## Related skills

- `super-codebase-learner`: current-state facts are missing.
- `super-challenge-me`: stress-test the pick before you commit.
- `super-architecture`: choose the architecture style for the target stack.
- `writing-plans`: turn the migration into a step-by-step plan.
- `create-jira-story`: split the plan into tickets.

## Done when

- Current-state work was sent to `super-codebase-learner` when that was the job.
- The guide that matches the job was opened, and the second only when the job needs both.
- Every current-stack fact cites learner output or a file the user provided; every estimate is labeled as one.
- A comparison ends in a recommendation with its confidence.

## Breaking renames

- `technology-stack-blueprint-generator` → **blueprint** speciality (now *target* / greenfield, not a current-repo inventory)
- `tech-stack-evaluator` → **evaluate** speciality
- `improve-codebase-architecture` (target stack / migration / next architecture) → this skill; current smells → `super-codebase-learner` **diagnose**
