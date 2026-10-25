# Motion spec: <screen or component>

## The thesis

- Focal moment (at most one): <the one sequence that earns authorship, or none>
- Continuity: <state, layout or navigation changes that need explaining>
- Feedback: <controls and outcomes that need acknowledging>
- Budget: <what may be expensive and how often it runs>

## The gate (answer for every candidate)

| Motion | Purpose in one sentence | How often is it seen | Decision |
|---|---|---|---|
| <name> | <sentence> | <every click, tens per day, occasional, rare> | <none, minimal, standard, delight> |

If the purpose cannot be written, delete the motion. If it is seen 100 or more times a day, or starts from the keyboard, do not animate it.

## Contract per motion

| Field | Value |
|---|---|
| Trigger | |
| Element and property | `transform` or `opacity` unless a layout change is the point |
| Start and end | |
| Duration token | `--dur-fast` / `--dur-base` / `--dur-slow` |
| Easing | ease-out for enter and exit, ease-in-out for on-screen moves, spring for drag |
| Interruption | reverses from the current position |
| Final state | |
| Focus and input during motion | |
| Reduced motion result | removes movement, keeps the state change |
| Platform | |

## Checks

- Used tokens, no literal times.
- Works with reduced motion on and off.
- Smooth on the slowest target device.
- No more than three flashes per second.
