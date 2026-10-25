# Audit the colors that already exist

Most products hold several times more colors than the design made decisions about. Inventory first. Change nothing until the user accepts the plan.

## Steps

1. **Collect every literal.** The script finds hex (`#RGB`, `#RRGGBB`, and 8-digit hex, read as `#AARRGGBB` in Android `.xml` files and `#RRGGBBAA` elsewhere), `rgb(`, `hsl(`, `oklch(` and Kotlin or Dart `0xFFRRGGBB` colors, including SVG fills and strokes, chart configs and email templates. It does **not** see utility-class colors (`bg-blue-500`), CSS named colors (`red`, `white`), or constructor calls such as `UIColor(red:green:blue:)` and `Color(red:green:blue:)`. Search for those with grep and add them to the inventory by hand.

   ```bash
   python3 scripts/theme/theme.py audit <project folder> --out color-audit.md
   ```

   The script (in `design-system-kit`) skips build folders, groups near duplicates (OKLab distance under 0.02), counts literals outside token and theme files and lists the top files for each group. It edits nothing.
2. **Sort by lightness inside each hue family.** Duplicates show up as neighbours that look the same.
3. **Collapse near duplicates.** Two colors within 0.02 of each other are one color that drifted. Keep the one used most. Never average them.
4. **Give each survivor a role** from `data/roles.csv`. A color that matches no role is a missing token or a mistake. Decide which and say so.
5. **Count what is left.** More ramps than the structure needs (one neutral, one accent, the statuses shown) means the palette outgrew its design.
6. **Check the roles.** Which pairs does the product really draw? Measure them (see the contrast proof guide).
7. **Write the role inventory** with `templates/role-inventory.md`: color found, uses, role today, role it should play, token, action.

## Report rules

- Report the inventory and the role inventory before any change.
- Consolidating a palette changes rendered output on screens nobody asked about, so it stays a proposal until accepted.
- Separate facts from choices. A count of literals is a fact. Which duplicate to keep is a choice you propose.
- List what you could not see: colors built at runtime, remote theme values, user-chosen colors, images.

## What to look for

| Finding | Meaning |
|---|---|
| Many literals outside theme files | Components bypass the system |
| A color under 0.02 from another | Drift. Merge |
| A ramp for a status nobody shows | Remove |
| Two grays of different temperature | Pick one neutral |
| A third accent hue with no job | Remove or give it a job |
| One value used as both a border and a text color | Missing role |
| No dark values | Dark mode does not exist yet |
| Brand color fails contrast on its own button | Keep the brand. Move the filled step |
