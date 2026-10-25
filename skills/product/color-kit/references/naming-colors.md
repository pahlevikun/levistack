# Naming colors

Two kinds of names matter. Roles are for code. Plain words are for people.

## Role names (for code)

- Name by job: `text`, `text-muted`, `surface-raised`, `border-strong`, `primary`, `on-primary`.
- Add a state at the end: `primary-hover`, `primary-pressed`.
- Palette steps are numbers: `primary-500`. A number says where it sits, not what it means.
- Never name a token by its look (`blue-button`, `light-gray`). A rebrand turns the name into a lie.
- One role, one meaning. See `data/roles.csv`.

## Plain words (for people)

Use plain words in the report, in a brand sheet, in a legend that someone reads aloud and in design reviews.

```bash
python3 scripts/theme/theme.py name "#6E7090" "#C46A4A" --k 3
```

The command finds the closest entry in our own list of about 100 names (`data/theme/names.json` in the kit). The result reads `Harbor`, `close to Harbor` or `near Harbor`, depending on the distance. The list is small on purpose. It names a color. It is not a catalog.

Rules:

- A plain word is a label, not a value. Keep the hex next to it.
- Do not rename a brand color. The brand already named it.
- Names come from one list. Do not invent a second one in a document.
- If two colors in one palette get the same name, say so. It often means the two are too close.
