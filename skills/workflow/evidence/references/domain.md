# Build a domain workflow

Use this mode when the user wants a reusable workflow for a specific domain. The output is a catalog skill, not a new framework of mandatory adapters.

1. Define the domain, the user's recurring task, the reader, and a concrete result. Search the catalog first. If a skill already owns that task, improve it instead of adding a competing router.
2. Read domain-specific primary sources and current rules where accuracy matters. Identify what counts as evidence, who owns the decision, and how a practitioner checks the output. Do not present a general agent checklist as professional authority.
3. If source material exists, classify it with `convert-as-skill` and use its appropriate guide. Otherwise use `create-skill`. Write the workflow in original prose with ordered actions, evidence requirements, and a visible stop condition. Add a flowchart only if branching is hard to follow in text. Use `diagram` for a technical flowchart or `infographic` for an audience-facing visual; the infographic may include one verified technical figure without calling back to the domain workflow.
4. Add one ordinary case, one tempting failure case, and one routing negative to the skill's evals. Run a real smoke exercise against the produced skill. Record what the exercise tested and what remains unverified.
5. Follow `manage-stack` for catalog metadata, lint, sync, validation, and tests. Keep third-party source files and their notices intact. Do not call copied material original or remove a license from copied code.

If a serious legal, medical, financial, or safety decision needs qualified sign-off, design the skill to collect evidence and prepare a reviewable draft. Do not imply that passing a smoke eval grants domain expertise.
