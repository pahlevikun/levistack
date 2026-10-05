# Orchestrating several agents

Use more than one agent only when the task is large enough to repay the coordination. A single capable agent is often better than three simple ones.

## Contents
- Choosing a pattern
- Sequential
- Parallel
- Hierarchical
- Coordinator
- Orchestrator and workers
- Handoffs
- Synchronization
- Running plans with fresh context
- Model tiers
- Anti-patterns

## Choosing a pattern

```
Can the task be split into independent parts?
  yes -> Parallel
  no  -> Does each part need the previous part's output?
           yes -> Sequential
           no  -> Does it need decomposition plus oversight?
                    yes -> Hierarchical
                    no  -> Does the next step depend on what was found?
                             yes -> Coordinator
                             no  -> one agent
```

Choose the simplest pattern that meets the need. Speed: parallel, then hierarchical, then sequential. Complexity runs the other way.

## Sequential

A fixed chain: each agent consumes the previous one's output. Use it for review pipelines (security, then performance, then style), data pipelines (extract, transform, validate, load), and staged reasoning (research, analyze, synthesize). Easy to debug; one failure blocks the chain and latency adds up.

## Parallel

Independent agents work at once on the same input or on different items, and the main session merges the results. Use it for independent analyses of one change, reviewing many files, and gathering from several sources. Wall time is the slowest agent, not the sum. Cost is higher and merging needs care.

## Hierarchical

A lead breaks a large task into parts, delegates each to a specialist, and integrates what comes back. Use it for work with natural layers (design, components, implementation) and where oversight matters. The workers know nothing of each other, so the lead owns coherence. Watch for misalignment between levels.

## Coordinator

A routing agent decides at each step which specialist to call, based on what the last one found: quality analysis finds a security smell, so route to the security reviewer; it finds issues, so route to a fixer; then to a test writer; then synthesize. Use it when requests vary and the path is not known in advance. The coordinator is a single point of failure, so keep it thin: it routes and synthesizes, it does not do deep work.

## Orchestrator and workers

One orchestrator splits a batch (fifty services, a hundred files) into chunks, gives each chunk to a worker running the same agent, and aggregates. Workers do not talk to each other. Make the chunks independent, and give each worker a disjoint set of files to own.

## Handoffs

Every handoff is a chance to lose context. Give the next agent what it needs in a fixed shape:

```
To: <agent>
Task: <the specific job>
Done so far: <summary of prior work>
Key findings: <what matters, with file:line>
Constraints: <limits and requirements>
Expected output: <the report shape>
Attachments: <paths to files or earlier reports>
```

"Found issues" is not a handoff. "Three issues: SQL injection at `db.ts:127` (Critical) ..." is. A downstream agent must validate its inputs and not assume upstream output is sound.

## Synchronization

For parallel work:
1. Start every agent with the shared context.
2. Track which have finished.
3. Wait for all, or until a timeout.
4. Proceed with what arrived and flag what is missing.

If one of three fails, go on with two and name the gap. If two of three fail, retry or stop. Always report what was completed against what was attempted.

## Running plans with fresh context

A plan with no human checkpoints can run in a subagent whose context starts empty, so it cannot degrade. For a plan with checkpoints, run the stretches between checkpoints in subagents and the checkpoints in the main session:

- before the first checkpoint, after a verify-only checkpoint: subagent;
- after a decision or a human action that the next tasks depend on: main session.

Tell each segment's subagent which tasks are its own, to follow the plan's deviation rules, and not to write the summary or commit. Collect results, write one summary, make one commit. See `create-skill` `references/plans.md`.

## Model tiers

Use the strongest model where mistakes are expensive (planning, validation, security, synthesis) and a faster, cheaper one where the task is clear and mechanical (bulk reading, template filling, high-volume transforms). A planner on the strong model, workers on the cheap one, and a validator on the strong one is a common split. Pin models only after the agent works.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Three agents to review ten lines | Use one agent; reserve orchestration for real complexity |
| Several agents, no synthesis, conflicting reports | Always merge into one result and say which parts conflict |
| Independent analyses run in sequence | Run them in parallel |
| Vague handoffs | Use the structured handoff |
| One failure ends the workflow | Retry, fall back, or continue with partial results; see `references/reliability.md` |
| Two agents own the same files | Give each a disjoint set |
| Overlapping responsibilities ("both review quality") | One concern per agent |
| A coordinator that does the work | Route and synthesize only |
| Agents too broad ("helper") or too narrow ("SQL injection in Express only") | Name a role at the level of a real specialty |

Tell every subagent whether it may start others. The safe default is no.
