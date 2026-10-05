# Third-party provenance

Imported material in this catalog. Keep copyright notices with the files.

## virgiliojr94/book-to-skill (MIT)

- **Upstream:** https://github.com/virgiliojr94/book-to-skill
- **License:** MIT, Copyright (c) 2025 virgiliojr94 (copy: `skills/agent-authoring/convert-as-skill/scripts/extractor/LICENSE.md`)
- **What we copied:** document parsers (`pdf.py`, `html.py`, `docx.py`, `epub.py`, `text.py`, `rtf.py`), `sanitize.py`, `dependencies.py`, `config.py`, `exceptions.py`, and `scan_generated_skill.py`.
- **What we did not copy:** their `SKILL.md` generator, `utils.py` as a whole, Calibre/MOBI, pdf-inspector, discovery-tax evals, or `pip install book-to-skill`.
- **Adaptation:** package imports renamed `book_to_skill` → `extractor`. `extract_document.py` is ours: layout guards, user-supplied URL fetch, compact chapter fingerprint, no host/sponsor CLI.

## mattpocock/retro (procedure)

- **Upstream:** https://www.skills.sh/mattpocock/skills/retro
- **What we used:** the idea of reading a named prior session's transcripts before harvesting a skill. No files were copied. The steps live in `skills/agent-authoring/convert-as-skill/specialities/from-conversation/GUIDE.md`.
