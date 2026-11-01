# Map feature flows before proposing unification

Use for a request to map several features and identify duplicated concerns.
This is a read-only composition recipe, not permission to refactor.

1. Inventory features by behavior rather than assuming directories are boundaries.
   For each, name entrypoints, owners, persistence, external calls and terminal states.
2. Trace one representative flow and important failure/cleanup branches per feature.
   Anchor diagram nodes to source paths and symbols actually read. Mark uncertain
   links and excluded paths. Do not invent a uniform path to make diagrams tidy.
3. Build a concern matrix: feature, concern, implementation, invariants, caller,
   side effects, observed differences and evidence. Distinguish duplicated syntax
   from a shared policy with genuinely identical semantics.
4. Separate the as-built map from any proposal. For a consolidation candidate, list
   which callers would move, which invariants differ, which capability could be lost
   and how that loss would be decided or prevented. Similar names alone justify no merge.
5. Hand a target architecture decision to super-architecture, or an authorized
   behavior-preserving change to safe-refactor. Use write-plan for execution steps
   only after the target scope is settled. Keep unification synthesis with one owner.

Deliver a feature index, cited flow diagrams, concern matrix and concrete next
questions. A giant diagram without traced ownership is not a complete map.
Use diagram for a technical figure and preserve its editable source.
