# Context hygiene: read less, keep the facts

Output savers shorten what you write. This guide shortens what you read. It uses no special tools. Any search, filter, or converter that does the same job works.

## The rules

| Situation | Do this | Do not do this |
|---|---|---|
| You need to find where something is defined or used | Search by symbol or text. Follow the call chain. Open only the matching slice. | Paste or open whole files to look around. |
| You need one function, type, or import list | Read that slice, or list the symbols first. | Read a 500-line file for one function. |
| A command prints a lot (git diff, logs, test output) | Filter it first: keep failures, errors, and the last lines. Quote the shortest decisive line. | Dump the raw output into the reply or the context. |
| The input is a PDF, an Office file, or a spreadsheet | Convert it to text or markdown first, then read the text. | Read a large binary file as it is. |
| You must show the state of a UI | Use text: the DOM text, the accessibility tree, or a short description plus the selector. | Paste a multi-megabyte screenshot. |
| A past decision matters again | Read the one note or decision record. Cite its path and id. | Replay the full old transcript. |
| You already read a document slice | Cite the path and the id. | Copy the slice into the reply again. |
| The task needs one or two tools or skills | Load only those. | Load every available tool and skill "just in case". |
| Context grows fast and you do not know why | Look for re-read loops, repeated large attachments, and tool output that nobody uses. Fix the cause. | Compress the symptom and keep the loop. |
| Work is wide and parallel (many lookups) | Delegate to subagents and demand a short, structured result. See [../concise/references/crew.md](../concise/references/crew.md). | Do ten searches in the main thread. |

## Order of operations

1. **Recall.** Check notes, decision records, and project docs for the answer before you search the code.
2. **Search.** Find the exact location with a symbol or text search.
3. **Normalize.** Convert attachments and images to text.
4. **Filter.** Trim tool output to the decisive lines.
5. **Delegate.** Hand wide lookups to a subagent with a short output contract.
6. **Remember.** Write the decision down once, in the place the project already uses for notes.

## Rules that never bend

- Never trim away a negation, a condition, a number, a version, or an error line that decides the outcome.
- Never put a secret into a note, a memory file, or a compressed copy. Refuse and say why.
- Show the exact command and the exact error. Shorten the text around them, not the facts inside them.
- When the user asks for the full output, give the full output.

## Related

- Reply style: [../concise/references/ste-style.md](../concise/references/ste-style.md).
- Compress a memory or instruction file: [../concise/references/compress.md](../concise/references/compress.md).
- Smallest change: [../principles/references/engineering-principles.md](../principles/references/engineering-principles.md).
