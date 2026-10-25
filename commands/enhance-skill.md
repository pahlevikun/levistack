---
description: "Improve one existing skill by learning from upstream skills, repos or pages: keep, replace and drop each method, rewrite it, test it."
argument-hint: "<skill path> <source url or folder> [more sources]"
---

Use the convert-as-skill skill and its enhance-skill guide. Input: $ARGUMENTS (ask for the skill path and at least one source when empty).

Run `scripts/enhance.mjs` for the inventory and the fetch plan. Fetch sources only into an ignored scratch folder. Read each source to the end, fill the keep, replace and drop map, and stop for my review before you write. Write the result as additions in our own words. Run lint and the repo checks.

Reply with the files changed, the checks, and the path of the private map. Do not copy upstream text. Do not add upstream names or licenses. Do not commit.
