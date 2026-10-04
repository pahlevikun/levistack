# Create issues in Jira (Route B)

Use only after the user chose **create ticket** and confirmed project, type, and parent (if any).

## Pick a path (first match wins)

1. **Atlassian MCP** — If the session has an Atlassian/Jira MCP (e.g. Cursor Atlassian plugin): authenticate if needed, then create the issue with summary, description (markdown or rich text per tool schema), project, issue type, and parent/epic fields the tool exposes. Prefer this when available; it avoids hand-built ADF.
2. **`acli`** — If `acli jira auth status` succeeds: create with `acli jira workitem create`. Cloud descriptions must be **Atlassian Document Format (ADF)**, not wiki markup. Passing `h3.` or `*` wiki text in `--description-file` renders literally.
3. **Jira REST API** — If the user supplied `JIRA_DOMAIN`, `JIRA_EMAIL`, and `JIRA_TOKEN`: `POST /rest/api/3/issue` with `fields.description` as ADF. Read-only patterns live in `skills/workflow/standup/scripts/jira.mjs` (ADF text extraction); do not copy secrets into the skill output.
4. **Stop** — If none of the above works, say so once and deliver **markdown only** (Route A) for paste into the UI.

## acli examples

Auth check:

```bash
acli jira auth status
```

Create (replace placeholders; description file must be ADF JSON):

```bash
acli jira workitem create --project PROJ --type Story --parent EPIC-123 \
  --summary "Short imperative title" --label "team-label" \
  --description-file /path/to/description.adf.json --yes
```

Edit description on an existing key:

```bash
acli jira workitem edit --key PROJ-456 --description-file /path/to/description.adf.json --yes
```

Verify description stored as ADF (dict, not a plain wiki string):

```bash
acli jira workitem view PROJ-456 --json | python3 -c \
  "import sys,json;d=json.load(sys.stdin)['fields']['description'];print(type(d).__name__)"
```

### ADF from markdown draft

There is no bundled converter in this repo. Options:

- Use Atlassian MCP create/update if it accepts markdown.
- Build minimal ADF JSON (doc → paragraph → text nodes) from the finalized markdown sections.
- Create with acli using a short plain summary in `--summary` and paste the full markdown body via the Jira UI (tell the user if you fall back to this).

### Batch create (zsh-safe)

Do not index bash arrays in zsh. Pipe explicit `KEY file` pairs:

```bash
D=/path/to/adf
printf '%s\n' \
  "story_01.adf.json" \
  "story_02.adf.json" | while read f; do
  acli jira workitem create --project PROJ --type Story --parent EPIC-123 \
    --summary "..." --description-file "$D/$f" --yes
done
```

## Fields this skill does not set unless asked

- Priority (some acli builds omit it; use a **label** such as `P0` / `P1` if the team encodes priority that way).
- Custom required fields — ask the user or read project metadata via MCP/API before create.

## After create

Return each **issue key**, **summary**, and link pattern `https://<site>.atlassian.net/browse/<KEY>` when the site is known. If create partially failed, list successes and failures separately.
