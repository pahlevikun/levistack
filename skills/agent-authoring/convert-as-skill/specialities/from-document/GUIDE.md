# From a document

Turn a PDF, docs folder, HTML file, or a user-supplied URL into a skill. Distill structure (frameworks, indexes, procedures). Do not dump the document into `SKILL.md`.

Extractor: `scripts/extract_document.py` (parsers in `scripts/extractor/`: `pdf.py`, `html.py`, `docx.py`, `epub.py`, `text.py`, `rtf.py`, plus `sanitize.py`, `dependencies.py`, `config.py`, `exceptions.py`, `__init__.py`, `LICENSE.md`). After writing, scan with `scripts/extractor/scan_generated_skill.py`.

## Preconditions

- Classify already returned `from-document`. If it did not, stop.
- Python 3 on PATH. Optional extras (pdftotext, pypdf, pdfminer, Docling, BeautifulSoup, python-docx, ebooklib, trafilatura) improve quality; missing ones skip with a hint.

```bash
python3 scripts/extract_document.py --check
```

`--check` always exits 0. MOBI/AZW are out of scope (no Calibre). Fetch a URL only when the user passed it — no crawling.

## Steps

1. **Extract** (script). Refuse happens inside the script for `rules/`, `commands/`, `agents/`.

   ```bash
   python3 scripts/extract_document.py [--mode text|technical] [--json] [--out <work-dir>] <file-or-url-or-docs-dir>
   ```

   `--mode technical` tries Docling first (tables, code, formulas), then the text chain. A scanned PDF aborts: run OCR, then retry.
2. **Fingerprint.** Read the `.meta.json`: format, method, chapter count and method (`numeric` / `structural` / `none`), `has_toc`, token estimate, `sha256`. If chapters are `none`, skim the `.txt` and outline by headings yourself; do not copy the whole file.
3. **Outline for the user** before writing:
   - proposed `name` and `description` (`Use when ...`, the document's own trigger words)
   - which chapters or sections become the skill vs `references/`
   - what you will drop (narration, examples that are not procedures, copyrighted long excerpts)
   - where it will be written (project skills dir, not this catalog unless the user maintains levistack **and** the source is theirs)
4. **Distill** with `create-skill`. One procedure in `SKILL.md`. Depth in `references/`, one level. Quote only short, necessary fragments. Prefer the document's own structure over a rewrite.
5. **Copyright.** Third-party book skills stay **private** (user or project skills folder). Do not commit them to this catalog. Do not paste chapters into chat.
6. **Scan and lint.**

   ```bash
   python3 scripts/extractor/scan_generated_skill.py <skill-dir>
   node <create-agent>/scripts/lint.mjs <skill-dir>
   ```

   Advisory scan findings are review items, not automatic deletes.

## Do not

- Copy the extracted `.txt` into `SKILL.md`.
- Run `convert.mjs` on these files.
- Fetch a URL the user did not pass, or follow links from the page.
- Commit a generated book skill to `skills/` in this repo.
