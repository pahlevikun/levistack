---
name: compare-models
description: "Run one prompt on two or three models this host can spawn and compare the results. Asks once if the prompt is missing. Reports what each model produced, where they disagree, and which result you would ship and why. Use when the user says compare models, which model should do this, or run this prompt on two models. Not for timing one model (verify), several attempts with no model question (rumbling Contest), or a paid quality score."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: workflow
  category: workflow
  department: workflow
  related_skills:
    - verify
    - rumbling
    - figure-it-out
  tags:
    - models
    - comparison
  capabilities:
    - same_prompt_model_comparison
  languages:
    - en

---

# Compare models

One prompt. Two or three models. One table. No paid judge and no outside benchmark binary.

## Steps

1. **Take the prompt.** Use the user's words. When they name a catalog skill instead, use that skill's task as the prompt and say so. If neither is present, ask once. Do not invent a prompt.
2. **Pick models this host can spawn.** Two or three. Prefer models the user named. If they did not, use distinct models the session can actually start, and name them. Skip a model the host cannot start. Say which you skipped. One model is not a comparison. Stop and say so.
3. **Run the same prompt on each model.** Give each the same inputs and the same limits. Do not send the prompt to a paid scoring service, a provider benchmark binary, or an OpenRouter adapter.
4. **Compare.** Read each result. Do not rank them with a numeric score you invented.

## Output

A table with one row per model: what it produced, in one or two lines. Then where the results disagree, and which result you would ship and why. Save a file only when the user asks.

## Related skills

- `verify`: time one model, or check a performance number. Not a comparison across models.
- `rumbling`: several attempts at one brief when the question is the solution, not the model.
- `figure-it-out`: the comparison is one step inside a larger run.

## Done when

- Two or three real runs are in the table, or the reply says the host could not start a second model.
- The reply names a result you would ship and why, or says they are tied.
- No paid judge ran, and no file was written unless the user asked.
- [evals/evals.json](evals/evals.json) covers a two-model prompt, a missing prompt, and a single-model timing request.
