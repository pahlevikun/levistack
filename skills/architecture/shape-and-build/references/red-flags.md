# Shape red flags

Screen every candidate before you pick. A red flag is a reason to revise the shape or drop it.

| Flag | What it looks like | Fix |
|---|---|---|
| Shallow module | A wide public surface that hides little. Callers chain several calls to finish one operation, or options expose internal stages | Fold the stages behind one call that owns the policy |
| Leaked decision | One representation, policy, or wire detail appears in several modules, so a change needs coordinated edits | Parse external data into domain types at the boundary. Keep storage and transport types private |
| Ordered by time | Modules split by execution order (load, validate, transform, save) each re-check the same invariants | Group code by the knowledge it owns. Steps that run at different times can share a module |
| Pass-through layer | A method forwards the same arguments to another with the same shape | Remove the layer, or give it real policy or adaptation |
| Split ownership | Two modules write the same state or keep their own copy | Give each piece of state one owner. Others read it or ask the owner |
| Boolean soup | Several flags whose combinations encode states, some impossible | A tagged union or a state machine with only the valid states |
| Stringly typed | IDs, units, or states passed as bare strings or numbers | Named types the compiler can tell apart |
| Hidden temporal coupling | A call is only valid after another, and nothing enforces it | Return a value from the first call that the second requires |
