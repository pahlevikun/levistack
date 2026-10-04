# Target architecture from a current-state diagnosis

How this skill consumes `super-codebase-learner` output. The diagnosis (smells, layering, HTML review) is owned there; this file is only the *target* half.

Do not re-scan the repo to rediscover current modules. If current-state is missing, tell the user to run learner **diagnose** / **summarize** first, or do that sibling skill before continuing.

## Inputs (from learner)

- `ARCHITECTURE.md` or onboard recon: languages, frameworks, versions, entry points — facts, each with a file when possible
- Diagnose report: candidate files, current problems, ADR conflicts, what must not be re-litigated
- User constraints: team skills, budget, compliance, deadline

## What you produce

A **target** architecture / stack / migration blueprint, not a second smell report.

1. **Separate in-place deepening from stack change.** Module-deepening on the current stack stays with learner + `super-challenge-me` (**grill-docs**). Only continue here when the change is a new framework, runtime, datastore, cloud, or a system-level target shape (for example hexagonal ports the current tree does not have).
2. **Evaluate** if more than one target is plausible — stack-evaluator GUIDE (`specialities/stack-evaluator/GUIDE.md`): comparison, TCO, security, ecosystem, migration effort.
3. **Blueprint** the chosen target — blueprint-generator GUIDE (`specialities/blueprint-generator/GUIDE.md`): versions to adopt, required patterns, templates for new code, diagrams of the *next* system.
4. **Migration path** when a current system exists: phases, risks, rollback — evaluator migration workflow. Cite learner facts as the from-state.

## Report shape

- One recommended target and why
- What current pain the target is meant to remove (cite diagnose candidates, do not rewrite them)
- Confidence and what would change the pick
- Explicit non-goals: documenting today's tree, writing `ARCHITECTURE.md` of as-is code
