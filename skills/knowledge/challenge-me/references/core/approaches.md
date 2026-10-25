# Lay out the approaches

Use this in **brainstorm** mode, after you understand what the user wants and before you write anything down. It is about *how to build it*. For *what the user wants*, let them describe it first with open questions and no menus.

## Steps

1. **Think of several real ways to build it.** Then drop the weak ones. Drop any that work against why the user wants this. Drop any the existing work already rules out.
2. **Keep two or three.** If a less obvious option is real (a smaller slice, a different owner, "do nothing and measure first"), include it. Do not pad the list to reach three.
3. **Tie each option to the project.** Say what it would mean for the code, the data or the people that exist today. Say what it gives up.
4. **Recommend one,** and give the reason in a single sentence.
5. **Send it as its own message.** Do not mix it with other questions or with the write-up. End by asking which way the user wants to go.
6. **Only one way makes sense?** Say so, and say why the others do not fit.
7. **Record it** in the design brief: the option chosen, the options turned down, and why.

## Shape of the message

| Option | What it is | What it gives up | Best when |
|---|---|---|---|
| A. <name> | <one or two lines, tied to the project> | <the cost> | <the situation where it wins> |
| B. <name> | ... | ... | ... |

**My pick:** <A or B>, because <one sentence>. Which way do you want to go?

## Example

The goal: "limit how often one client can call our API."

| Option | What it is | What it gives up | Best when |
|---|---|---|---|
| A. Gateway limit | One rule in the gateway we already run | Cannot vary by endpoint | Every endpoint can share one limit |
| B. Per-handler limiter | A small limiter in each handler | More code to keep in step | Some endpoints are far more costly than others |
| C. Queue and workers | Accept requests, process them at a fixed rate | Callers wait, and a new queue to run | Bursts are normal and delay is fine |

**My pick:** A, because the gateway already exists and the team asked for one simple limit. Which way do you want to go?
