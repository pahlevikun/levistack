# Prototype

A throwaway prototype answers one open question. This skill does not hold a second prototype procedure. Use the `prototype-wireframe` skill.

## When to ask for one

- A behavior or rule is disputed and talking has not settled it.
- A novel interaction or layout has no precedent in the product.
- Two or three directions need a fair comparison on the same task.

If reading the code answers it, read the code. If it needs a person's knowledge, ask. If it is already clear, write the plan.

## What the prototype skill gives you

- A logic playground, a set of look variants, a grayscale wireframe or a flow map.
- A file under `prototypes/<topic>/`, labeled throwaway, that does not touch product code.
- An answer, a pick and what is still undecided.

## What you do with the answer

1. Write the answer in the plan, the issue or the design-system document, with what was learned.
2. Delete the prototype or move it to a clearly marked place if someone may want it again.
3. Build the real version properly, with `ui-ux-kit` for screens and `tdd` for behavior. A confirmed rule block from a logic prototype is lifted into the real module.
4. Do not keep a prototype next to the product code and do not ship it. If it must be kept, keep it on a clearly named throwaway branch and put the branch name in the issue.
