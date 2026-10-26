# Raster Python tools

Python helpers for **preferences**, **backend discovery**, and **optional API raster generation**. Stdlib HTTP only for API calls. Modules: `scripts/infographic_prefs.py`, `scripts/raster_backends.py`, `scripts/image_generate.py`.

## Preferences (extend file)

Search order (first file wins):

1. `{project}/infographic.prefs.json`
2. `{project}/.levistack/infographic.prefs.json`
3. `{project}/infographic.extend.md` or `.levistack/infographic.extend.md`
4. `$XDG_CONFIG_HOME/levistack/infographic.prefs.json`
5. `$XDG_CONFIG_HOME/levistack/infographic.extend.md`
6. `$HOME/.levistack/infographic.prefs.json`

Template: [../templates/infographic.prefs.json](../templates/infographic.prefs.json). Markdown variant: [../templates/infographic.extend.md](../templates/infographic.extend.md).

| Field | Meaning |
|---|---|
| `preferred_raster_backend` | `auto`, `openai`, `openrouter`, `agent-native`, `codex-cli`, `ask` |
| `quick_mode` / `skip_confirm` | Standing opt-out of [confirmation gates](confirmation-gates.md) when true |
| `generation_batch_size` | Hint for slide batch size (agent may parallelize) |
| `openrouter_model` / `openai_model` | API model ids for `generate` |
| `style_prefix` | Prepended to prompt file text for API calls |

`quick_mode` does not skip evidence rules. It only skips layout and backend confirmation when you already opted in via prefs.

## CLI: `image_generate.py`

From the skill `scripts/` directory:

```bash
python3 image_generate.py prefs show --project .
python3 image_generate.py prefs init --project .
python3 image_generate.py backends --json
python3 image_generate.py resolve --project .
python3 image_generate.py generate --prompt-file prompts/cover.md --output exports/cover.png --aspect 16:9 --dry-run
python3 image_generate.py batch slides-manifest.json --dry-run
```

### Backends

| Id | Driven by script? | Notes |
|---|---|---|
| `agent-native` | No | Prints a receipt. Agent uses the host image tool when available. |
| `openai` | Yes | Needs `OPENAI_API_KEY` |
| `openrouter` | Yes | Needs `OPENROUTER_API_KEY` |
| `codex-cli` | No | Listed when `codex` is on PATH |
| `local-vector` | Use `png_from_svg.py` | Evidence track, not generative art |

API calls use stdlib `urllib` only. Outputs refuse overwrite like other export scripts.

### Batch manifest

`slides-manifest.json` is an array of objects:

```json
[
  {"prompt_file": "prompts/slide-01.md", "output": "exports/slides/01.png", "aspect": "16:9"},
  {"prompt_file": "prompts/slide-02.md", "output": "exports/slides/02.png", "aspect": "16:9", "backend": "openai"}
]
```

Generation runs sequentially. Parallel batches stay with the agent runtime.

## Workflow tie-in

1. Load prefs: `image_generate.py prefs show`.
2. List backends: `image_generate.py backends`.
3. Confirm layout and aspect ([confirmation gates](confirmation-gates.md)) unless `skip_confirm` is true.
4. Write prompt files under `prompts/`.
5. `resolve` or `generate --dry-run` before spending API credits.
6. `generate` or hand off to `agent-native` per receipt.

Raster drafts stay **labeled synthetic**. Factual numbers belong in vector layers or captions, not painted into bitmaps unless the user accepts that tradeoff.
