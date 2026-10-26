# Layout types

Pick a type from evidence and reading goal, then map it to a structure in [composition](composition.md). Use these wireframes for planning and [design specification](../templates/design-specification.md) for the written spec.

## Statistical

**Best for:** research, survey results, industry data with sourced numbers.

```
┌─────────────────────────────────────┐
│           HEADER / TITLE            │
│         key statistic (sourced)     │
├─────────────────────────────────────┤
│   ┌─────┐  ┌─────┐  ┌─────┐        │
│   │ KPI │  │ KPI │  │ KPI │        │
│   └─────┘  └─────┘  └─────┘        │
├─────────────────────────────────────┤
│         main chart (computed)       │
├─────────────────────────────────────┤
│   supporting stats + icons            │
├─────────────────────────────────────┤
│         caveat + source line          │
└─────────────────────────────────────┘
```

## Timeline

**Best for:** dated evidence, milestones, evolution. Use honest spacing or label categorical time.

```
┌─────────────────────────────────────┐
│              TITLE                  │
├─────────────────────────────────────┤
│  2020 ●───────────────●             │
│       event + source                │
│  2021      ●──────────●             │
│            event + source           │
├─────────────────────────────────────┤
│         synthesis + limits          │
└─────────────────────────────────────┘
```

## Process

**Best for:** how-to, workflows, tutorials. Use a technical figure pass when the flow is technical topology.

```
┌─────────────────────────────────────┐
│           HOW TO [X]                │
├─────────────────────────────────────┤
│  (1) Step title + sourced detail    │
│      │                              │
│      ▼                              │
│  (2) Step title                     │
│      │                              │
│      ▼                              │
│  (3) Step title                     │
├─────────────────────────────────────┤
│         outcome + caveat            │
└─────────────────────────────────────┘
```

## Comparison

**Best for:** policies, products, before/after with equal scope.

```
┌─────────────────────────────────────┐
│              TITLE                  │
├────────────────┬────────────────────┤
│    OPTION A    │     OPTION B       │
├────────────────┼────────────────────┤
│  row (sourced) │  row (sourced)     │
├────────────────┴────────────────────┤
│    recommendation + limits          │
└─────────────────────────────────────┘
```

## List

**Best for:** ranked tips, resources, top-N with citations per item.

```
┌─────────────────────────────────────┐
│         TOP N [TOPIC]               │
├─────────────────────────────────────┤
│  #1  Title + one-line proof         │
├─────────────────────────────────────┤
│  #2  Title + one-line proof         │
├─────────────────────────────────────┤
│  #3  ...                            │
└─────────────────────────────────────┘
```

## Geographic, hierarchical, network

Use composition guides for map, layers, and adjacency layouts. Do not pick a type label without a defined meaning for position and link.

## Principles (from layout to spec)

1. Lead with the sourced hook, not decoration.
2. One main message per asset or carousel panel.
3. Simplify numbers without changing meaning. Label rounding.
4. Cite sources on the artifact.
5. Match type to platform size in [formats](formats.md).
