# Document processes

Answer a bounded question about a workflow, handoff, or state machine. Use the process the system implements or the agreed business procedure, and label a proposed process as proposed.

## Trace the process

1. Identify the trigger, actors, inputs, completion condition, and audience.
2. Follow the steps or transitions through source code, tests, event records, or approved procedures.
3. Record decision conditions, handoffs, concurrent work, exceptions, and recovery paths. Keep unknown paths visible.
4. For each state, explain its meaning, entry condition, allowed next states, terminal status, and any caller action supported by evidence.
5. Distinguish independent status fields. A transport success, overall business state, and processing substate may describe different things.

## Choose the form

Use a numbered procedure for a simple sequence. Use `diagram` when relationships need a graph:

| Reader needs to understand | Useful diagram |
|---|---|
| Decisions and branches | Flowchart |
| Lifecycle and allowed transitions | State diagram |
| Messages between actors over time | Sequence diagram |

Follow the repository's diagram format. Match the detail to the question instead of drawing every internal call. Treat every label and arrow as a claim that needs evidence. Do not infer a transition merely because two state values appear in samples.

Use `infographic` for an audience-facing process overview, evidence-based timeline, or comparison when composition explains the process better. It can embed the verified diagram. Pass editable source, evidence and unknowns, and the requested export format. Keep a single visual owner and at most one diagram/infographic handoff per artifact, without a callback loop or an unsolicited second asset.

## Deliver and verify

Provide enough prose for the trigger, outcomes, exceptions, and consequences of the process. Avoid restating every arrow in a second full description.

Keep editable diagram source. Render it with the existing tooling and inspect the result. For a PDF or DOCX, embed the rendered diagram and retain source with regeneration instructions. Keep source and derived output consistent with the project's export policy.

Check transitions, actors, branches, and terminal states against the evidence. Report unverified paths and conflicting records rather than drawing an apparently complete process.
