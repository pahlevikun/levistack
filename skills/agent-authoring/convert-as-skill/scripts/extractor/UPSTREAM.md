# Upstream provenance

Imported material in this package. Keep copyright notices with the files.

## virgiliojr94/book-to-skill (MIT)

- **Upstream:** https://github.com/virgiliojr94/book-to-skill
- **License:** MIT, Copyright (c) 2025 virgiliojr94 (`LICENSE.md` in this folder)
- **What we copied:** document parsers (`pdf.py`, `html.py`, `docx.py`, `epub.py`, `text.py`, `rtf.py`), `sanitize.py`, `dependencies.py`, `config.py`, `exceptions.py`, and `scan_generated_skill.py`.
- **What we did not copy:** their `SKILL.md` generator, `utils.py` as a whole, Calibre/MOBI, pdf-inspector, discovery-tax evals, or `pip install book-to-skill`.
- **Adaptation:** package imports renamed `book_to_skill` → `extractor`. `extract_document.py` is ours: layout guards, user-supplied URL fetch, compact chapter fingerprint, no host/sponsor CLI.
