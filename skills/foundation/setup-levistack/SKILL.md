---
name: setup-levistack
description: "Checks this machine for the runtimes and optional CLIs levistack scripts call (node, python3, rsvg-convert, ffmpeg, mmdc, Playwright, glab, jq, sqlite3, pdftotext), then writes the result to ~/.levistack/setup.md. Installs nothing without a yes. Use when the user types /setup-levistack, asks to set up levistack, or a skill step failed because a tool was missing. Not for picking models or reasoning budgets, or for installing skills (find-skills)."
disable-model-invocation: true
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: foundation
  category: foundation
  department: foundation
  related_skills:
    - help-levistack
    - use-levistack
    - find-skills
  tags:
    - levistack
    - setup
    - tools
    - doctor
  capabilities:
    - tool_availability_check
    - local_setup_note
  languages:
    - en

---

# Setup levistack

Find out which tools levistack scripts can use on this machine, and leave a note other runs can read. Most skills are prose and need nothing. A few run scripts, and those scripts call tools that may be missing.

`use-levistack` runs your check before it routes. When it sends the user here, the task is waiting. Finish this skill, then return to its step 1 once the status is no longer blocked. If they decline a required install, the route stops.

## Steps

1. Run the check and show the result:

   ```bash
   node scripts/check.mjs
   ```

   The script path is relative to this skill folder. Without `node`, nothing here runs: say so and give the install line for the user's OS.
2. Write the note. Rerunning overwrites it:

   ```bash
   node scripts/check.mjs --write
   ```

   It writes `~/.levistack/setup.md`. Pass `--out <path>` only when the user names another place.
3. For each missing tool, name the gap and the step it stops, using the note's install line. Ask once whether to install any of them. Install only what the user says yes to, one command at a time, then rerun step 2.
4. Point at the next move: `/use-levistack` with a goal and a check, or `/help-levistack` with a question.

## Tools

| Tool | Needed | Used by |
|---|---|---|
| `node` 20+ | Required | Every Node script, `npm run check` |
| `python3` | Required | Diagram, infographic, file-toolkit, convert-as-skill, mcp-management scripts |
| `rsvg-convert` | Optional | `diagram` `export_svg.py`, `infographic` `png_from_svg.py` |
| `ffmpeg` | Optional | `diagram` animated export and Mermaid GIF encoding |
| `mmdc` | Optional | `diagram` Mermaid to SVG or PNG |
| Playwright (Python) | Optional | `diagram` `mermaid_playwright_gif.py` |
| `glab`, `jq` | Optional | `code-review` `mr-context.sh` |
| `sqlite3` | Optional | `standup` `collect.mjs` browser history |
| `pdftotext` | Optional | `convert-as-skill` `extract_document.py` |

A missing optional tool is a named gap, not a failure. The skill that needs it reports the gap and skips that step. A missing required runtime blocks every script.

## Boundaries

- Install nothing without a yes. Never run `sudo` on your own.
- Write only the note path. Do not edit shell profiles, PATH, or global config.
- No model choice or reasoning budget. This catalog does not set them.

## Output

The table from the note, the status line (ready, ready with named gaps, or blocked), the gaps with install lines, and the path written.

## Related skills

- `help-levistack`: answers questions about the catalog once setup is known.
- `use-levistack`: runs the work. It calls this skill before its seven steps when the machine check is blocked.
- `find-skills`: installs skills. This skill checks tools only.

## Done when

- `~/.levistack/setup.md` exists, or the user declined the write and the reply says so.
- Each missing tool is named with the step it stops and its install line.
- Nothing was installed without a yes.
- [evals/evals.json](evals/evals.json) covers a clean machine, a missing optional tool, and an install request that needs a yes.
