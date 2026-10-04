---
description: Humanize a draft with polyglot-copywriter (remove AI tells, keep the facts)
argument-hint: [file path, or paste the draft]
---
Use the `polyglot-copywriter` skill in rewrite mode, humanize pass, on: $ARGUMENTS

Resolve language, register, and use case first. Load `references/humanizer-patterns.md`
and `references/simple-prose.md`. Mark tells strongest first, rewrite in simple words
and short active sentences, then re-check for the survivors (not-X-but-Y, one-line
closer, triad, dash or semicolon, bold label). Keep every supported claim and add no
fact, name, number, date, quote, or citation. Use `[TK: …]` for a missing detail.

First principle: no em dash, en dash, or semicolon in the final text unless my sample
uses them. If I gave a file path, change prose only and write only the final text.
Keep code, commands, paths, YAML, and link targets. If the draft is a reply in a
thread, lead with the decision. Match any sample of my own writing in this conversation.
