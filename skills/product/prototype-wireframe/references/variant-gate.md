# Gate before you show it

A prototype goes to a person who will decide with it. Run this gate first. It has three parts: a score, a thumbnail check and a receipt.

## Score

Give each line 0, 1 or 2.

| Line | 0 | 1 | 2 |
|---|---|---|---|
| The question | Not visible on the page | Visible but vague | One clear line, the page is built around it |
| Difference | Variants are repaints | Some structure differs | Each variant has its own structure and first thing the eye hits |
| Honest content | Invented numbers or fake UI | Mixed | Real content or labeled sample data, counts match |
| Hierarchy | Competing focal points | Readable | One focal point per screen |
| Small-size read | Fails as a thumbnail | Mostly readable | Reads at 240 px wide |
| Works | A drawn control does nothing | Minor gaps | Every drawn control works or is deleted |

Pass at **9 of 12**. A zero on **Honest content** or **Works** fails, whatever the total. Fix the lowest line and score again. Two rounds is normal.

## Thumbnail check

Put every variant side by side at about 240 px wide each. Ask:

1. Can I tell them apart without reading any text?
2. Is the main structure of each one visible?
3. Is the smallest important label still readable?
4. Do two of them look like one template with new words?
5. Does one accent guide the eye, or is color spread everywhere?

If the answer to 4 is yes, redo the closer one with a new structure. Do not change its color.

## Red-team questions

- Could this screen belong to any product? If yes, it has no point of view.
- If I hide the title, does the screen still say something?
- Is the most noticeable thing also the most important thing?
- Did I use a card because the content needs a box, or because boxes are easy?
- Would a real capture or a plain table be more honest than this drawing?

## Receipt

Keep a short receipt next to the prototype. Copy `templates/receipt.md`. It lets someone else (or you, next month) re-run, compare and delete with no guesswork.
