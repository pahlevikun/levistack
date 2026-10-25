# Compress memory files into STE

Rewrite a natural language file (a memory file, a todo list, a preferences file) in Simplified Technical English. The new file has fewer input tokens. All technical content stays.

The compressed file replaces the original. A backup of the original is saved outside the project folder.

## When to use

- The user types a path and asks to compress, shrink, or shorten a memory or instruction file.
- A file such as `CLAUDE.md` is loaded in every session, so a smaller file saves tokens every time.

## Process

1. The scripts are in [`../scripts/`](../scripts/). They are TypeScript and have no dependencies.
2. From the `concise/` folder, run:

   ```bash
   node scripts/cli.ts <absolute_filepath>
   ```

3. The command does these things:
   - It detects the file type. This costs no tokens.
   - It sends the prose to Claude for rewriting. This is one call.
   - It validates the result. This costs no tokens.
   - On validation errors, it asks Claude to fix only those errors. It does not recompress.
   - It retries up to 2 times.
   - After 2 failed retries, it restores the original and reports the error.
4. Tell the user the result and where the backup is.

Requirements:

- Node 22.18 or later (it runs TypeScript directly). On Node 22.6 to 22.17, add `--experimental-strip-types`.
- `ANTHROPIC_API_KEY` in the environment, or the `claude` command on the PATH. The API key uses the Messages API. Without a key, the script runs `claude --print`.
- To choose a model, set `STE_COMPRESS_MODEL`. The default is `claude-sonnet-5-5`.

On Windows the `claude` command is often a `.cmd` file that Node cannot start without a shell. Set `ANTHROPIC_API_KEY` there.

## What the rewrite does

**Remove:**

- Filler: just, really, basically, actually, simply, essentially.
- Pleasantries and praise: "sure", "certainly", "happy to", "I'd recommend".
- Hedging: "it might be worth", "you could consider".
- Redundant phrases: "in order to" becomes "to". "The reason is because" becomes "because".
- Connective padding: "furthermore", "additionally", "in addition".
- Repeated points. Keep one example when several show the same pattern.

**Keep exactly:**

- Code blocks (fenced and indented) and inline code.
- URLs and links, file paths, commands.
- Technical terms, proper nouns, dates, version numbers, numbers.
- Environment variables.
- Every negation and condition ("do not", "never", "only if", "unless").

**Keep the structure:**

- All headings, with the exact text.
- The nesting of bullets, the numbering of lists, and tables.
- Frontmatter (the YAML header). The script removes it before the rewrite and puts it back unchanged.

**Rewrite in STE:**

- Use short, active sentences with one idea each. Use 20 words or fewer in an instruction and 25 words or fewer in a description.
- Keep the articles (a, an, the). Do not write fragments.
- Use one word for one meaning. Keep each technical term the same everywhere.
- Use the imperative for instructions. Delete "you should", "make sure to", and "remember to".

**Critical rule:** text inside ``` fences and inside backticks is read-only. Do not remove comments, change spacing, reorder lines, or shorten a command. Compress only the text outside them. Do not merge sections around code.

## Examples

Original:

> You should always make sure to run the test suite before pushing any changes to the main branch. This is important because it helps catch bugs early and prevents broken builds from being deployed to production.

Compressed:

> Run the test suite before you push to the main branch. This catches bugs early and prevents broken builds in production.

Original:

> The application uses a microservices architecture with the following components. The API gateway handles all incoming requests and routes them to the appropriate service. The authentication service is responsible for managing user sessions and JWT tokens.

Compressed:

> The application uses a microservices architecture. The API gateway routes each request to the correct service. The authentication service manages user sessions and JWT tokens.

## Which files work

| Type | Compress? |
|------|-----------|
| `.md`, `.txt`, `.markdown`, `.rst`, `.typ`, `.typst`, `.tex` | Yes |
| A file with no extension that holds prose | Yes |
| `.py`, `.js`, `.ts`, `.json`, `.yaml`, `.yml`, `.toml`, `.env`, `.sql`, `.sh`, `.html`, `.css` and other code or config | No. Skip. |
| `*.original.md` (backups) | No. Skip. |

If a file mixes prose and code, compress only the prose. If you are not sure whether text is code or prose, leave it unchanged.

## Backups

The script saves the original as `<name>.original.md` outside the project, so rule loaders do not read it as a live file.

- Linux and macOS: `$XDG_DATA_HOME/ste-compress/backups/<parent-folder>/`, or `~/.local/share/ste-compress/backups/<parent-folder>/` when the variable is not set.
- Windows: `%LOCALAPPDATA%\ste-compress\backups\<parent-folder>\`.

The script never overwrites an existing backup. It reads the backup back and compares it before it touches the input file.

## Security

- The script reads and writes only the file the user names, and its backup.
- It sends the file contents to the Anthropic API (or to the `claude` command). It refuses file names that look sensitive: `.env`, `credentials`, `secrets`, `password`, `token`, key and certificate files, and paths in `.ssh`, `.aws`, `.gnupg`, `.kube`, or `.docker`. Rename the file if the refusal is a false positive.
- It rejects files larger than 500 KB before any call.
- It never runs file content as code. It starts `claude` with a fixed argument list and no shell, and sends the prompt through stdin.
- It makes no network call except to the Anthropic API.

## Other commands

```bash
node scripts/detect.ts <file...>                  # type and compress decision
node scripts/validate.ts <original> <compressed>  # check a pair
node scripts/benchmark.ts <original> <compressed> # token savings (words if js-tiktoken is missing)
node scripts/benchmark.ts <directory>             # every .md file that has a backup
node --test scripts/scripts.test.ts               # offline tests
```

## Boundaries

- Compress natural language only. Never change code or config files.
- Never compress `*.original.md`.
- Never compress a file that holds secrets.
- Do not compress prose that a person reads as a document (README, docs, release notes). Use `polyglot-copywriter` to improve that kind of text.
