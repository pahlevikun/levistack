#!/usr/bin/env python3
"""Extract text from a document or a user-supplied URL. Distill in the GUIDE, not here.

  python3 extract_document.py --check
  python3 extract_document.py [--mode text|technical] [--json] [--out DIR] <file-or-url...>

Refuses rules/, commands/, agents/. Fetches a URL only when the user passed it.
MOBI/AZW are out of scope (no Calibre). Optional extras via --check; stdlib fallbacks.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

if __name__ == "__main__":
    sys.dont_write_bytecode = True

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from extractor.config import (  # noqa: E402
    CALIBRE_EBOOK_EXTENSIONS,
    CJK_CHARS_PER_TOKEN,
    HTML_EXTENSIONS,
    SUPPORTED_EXTENSIONS,
    TEXT_EXTENSIONS,
    WORDS_PER_TOKEN,
    supported_formats_message,
)
from extractor.dependencies import (  # noqa: E402
    normalize_install_mode,
    prepare_dependencies,
    run_dependency_check,
)
from extractor.exceptions import ExtractionError  # noqa: E402
from extractor.parsers.docx import extract_docx  # noqa: E402
from extractor.parsers.epub import (  # noqa: E402
    count_epub_chapters,
    count_epub_images,
    extract_with_ebooklib,
    extract_with_zipfile,
)
from extractor.parsers.html import extract_html_file  # noqa: E402
from extractor.parsers.pdf import (  # noqa: E402
    count_pages,
    extract_with_docling,
    extract_with_pdfminer,
    extract_with_pdftotext,
    extract_with_pypdf,
    looks_image_only,
)
from extractor.parsers.rtf import extract_rtf  # noqa: E402
from extractor.parsers.text import read_text_file  # noqa: E402
from extractor.sanitize import sanitize_extracted_text  # noqa: E402

MAX_URL_BYTES = 20 * 1024 * 1024
LAYOUT_REFUSE = {"rules", "commands", "agents"}
_CJK_RE = re.compile(
    r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
    r"\U00020000-\U0002a6df\U0002a700-\U0002b73f"
    r"\U0002b740-\U0002b81f\U0002b820-\U0002ceaf]"
)
_EXPLICIT_CHAPTER = re.compile(
    r"^\s*(?:#{1,3}\s+)?(?:chapter|unit|lesson|module|part|chapitre|kapitel|"
    r"cap[ií]tulo|capitolo|ch\.?)\s*(\d{1,2}|[IVXLCDMivxlcdm]{1,7})\b",
    re.IGNORECASE,
)
_MD_HEADING = re.compile(r"^#{1,3}\s+\S")
_TOC = re.compile(r"\b(table of contents|contents|índice|sommaire|inhaltsverzeichnis)\b", re.I)


def refuse_layout(path: Path) -> str | None:
    parts = {p.lower() for p in path.resolve().parts}
    hit = parts & LAYOUT_REFUSE
    if hit:
        return (
            f"{path} sits under {'/'.join(sorted(hit))}/; "
            "that layout is from-rule or from-agent. Use classify.mjs, then convert.mjs."
        )
    return None


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    cjk = len(_CJK_RE.findall(text))
    if not cjk:
        return int(len(text.split()) / WORDS_PER_TOKEN)
    latin_words = len(_CJK_RE.sub(" ", text).split())
    return int(latin_words / WORDS_PER_TOKEN + cjk / CJK_CHARS_PER_TOKEN)


def detect_structure(text: str) -> dict:
    """Compact chapter/ToC fingerprint. Distill uses this; it is not a dump."""
    numbers: set[str] = set()
    headings: list[str] = []
    md_headings = 0
    in_fence = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not s:
            continue
        m = _EXPLICIT_CHAPTER.match(s)
        if m:
            numbers.add(m.group(1).upper())
            headings.append(s)
        elif _MD_HEADING.match(s):
            md_headings += 1
            if len(headings) < 10:
                headings.append(s)
    if len(numbers) >= 2:
        method, count = "numeric", len(numbers)
    elif md_headings >= 3:
        method, count = "structural", md_headings
    elif numbers:
        method, count = "numeric", len(numbers)
    else:
        method, count = "none", 0
    return {
        "chapters_detected": count,
        "chapters_method": method,
        "chapter_headings_sample": headings[:10],
        "has_toc": bool(_TOC.search(text[:30000])),
    }


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sniff_ext(input_path: Path) -> tuple[str, str]:
    ext = input_path.suffix.lower()
    if ext in SUPPORTED_EXTENSIONS:
        return ext, ext.lstrip(".")
    try:
        header = input_path.read_bytes()[:8]
    except OSError as exc:
        raise ExtractionError(f"Could not read {input_path.name}: {exc}") from exc
    if header[:4] == b"%PDF":
        return ".pdf", "pdf"
    if header[:2] == b"PK":
        try:
            with zipfile.ZipFile(input_path) as zf:
                names = set(zf.namelist())
                if "mimetype" in names and zf.read("mimetype").startswith(b"application/epub"):
                    return ".epub", "epub"
                if "word/document.xml" in names:
                    return ".docx", "docx"
        except (zipfile.BadZipFile, KeyError, OSError):
            pass
        raise ExtractionError(
            f"Unsupported ZIP-based format '{input_path.name}'. Supported: {supported_formats_message()}"
        )
    raise ExtractionError(
        f"Unsupported format '{ext or '<none>'}'. Supported: {supported_formats_message()}"
    )


def extract_single_file(input_path: Path, extraction_mode: str, install_mode: str) -> dict:
    if not input_path.exists():
        raise ExtractionError(f"File not found: {input_path}")
    blocked = refuse_layout(input_path)
    if blocked:
        raise ExtractionError(blocked)

    ext, document_format = sniff_ext(input_path)
    if ext in CALIBRE_EBOOK_EXTENSIONS:
        raise ExtractionError(
            f"{ext} is out of scope for convert-as-skill (no Calibre). "
            "Convert the file to EPUB or PDF first."
        )

    prepare_dependencies(ext, extraction_mode, install_mode)
    input_str = str(input_path)
    text = ""
    method = ""
    pages = 0
    pages_label = "sections"
    images_dropped = None

    if ext == ".epub":
        text = extract_with_ebooklib(input_str) or ""
        method = "ebooklib" if text.strip() else ""
        if not text.strip():
            text = extract_with_zipfile(input_str) or ""
            method = "zipfile" if text.strip() else ""
        if not text.strip():
            raise ExtractionError(
                "Could not extract text from EPUB. Install ebooklib + beautifulsoup4, or the zip fallback failed."
            )
        pages = count_epub_chapters(input_str)
        pages_label = "spine_items"
        images_dropped = count_epub_images(input_str)
    elif ext == ".pdf":
        if looks_image_only(input_str):
            raise ExtractionError(
                f"{input_path.name} looks like a scanned (image-only) PDF. Run OCR, then retry."
            )
        if extraction_mode == "technical":
            text = extract_with_docling(input_str) or ""
            if text.strip():
                method = "docling"
            else:
                extraction_mode = "text"
        if extraction_mode == "text" or not text.strip():
            text = extract_with_pdftotext(input_str) or ""
            if text.strip():
                method = "pdftotext"
            else:
                text = extract_with_pypdf(input_str) or ""
                if text.strip():
                    method = "pypdf"
                else:
                    text = extract_with_pdfminer(input_str) or ""
                    if text.strip():
                        method = "pdfminer"
                    else:
                        raise ExtractionError(
                            "Could not extract text from PDF. Install pdftotext, pypdf, or pdfminer.six."
                        )
        pages = count_pages(input_str)
        pages_label = "pages"
    elif ext in TEXT_EXTENSIONS:
        text = read_text_file(input_str) or ""
        if not text.strip():
            raise ExtractionError(f"Could not read text document: {input_path.name}")
        method = "plain-text"
    elif ext in HTML_EXTENSIONS:
        text = extract_html_file(input_str) or ""
        if not text.strip():
            raise ExtractionError(f"Could not extract text from HTML: {input_path.name}")
        method = "html-parser"
    elif ext == ".docx":
        text, method = extract_docx(input_str)
    elif ext == ".rtf":
        text, method = extract_rtf(input_str)
    else:
        raise ExtractionError(
            f"Unsupported format '{ext}'. Supported: {supported_formats_message()}"
        )

    text, removed_invisible = sanitize_extracted_text(text)
    if not text.strip():
        raise ExtractionError(
            f"Extracted text from {input_path.name} contained no visible content after sanitization."
        )

    try:
        file_size_mb = os.path.getsize(input_str) / (1024 * 1024)
        file_sha256 = _sha256_file(input_str)
    except OSError as exc:
        raise ExtractionError(f"Could not read {input_path.name}: {exc}") from exc

    structure = detect_structure(text)
    result = {
        "source_file": str(input_path.resolve()),
        "filename": input_path.name,
        "format": document_format,
        "extraction_method": method,
        "file_size_mb": round(file_size_mb, 2),
        "sha256": file_sha256,
        pages_label: pages,
        "pages_label": pages_label,
        "pages": pages,
        "chars": len(text),
        "words": len(text.split()),
        "estimated_tokens": estimate_tokens(text),
        "images_dropped": images_dropped,
        "removed_invisible": removed_invisible,
        "text": text,
        **structure,
    }
    return result


def fetch_url(url: str, dest_dir: Path) -> Path:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ExtractionError(f"Not a fetchable URL: {url}")
    req = Request(url, headers={"User-Agent": "convert-as-skill/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:  # noqa: S310 — user-supplied URL, http(s) only
            data = resp.read(MAX_URL_BYTES + 1)
            ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
    except Exception as exc:
        raise ExtractionError(f"Failed to fetch {url}: {exc}") from exc
    if len(data) > MAX_URL_BYTES:
        raise ExtractionError(f"URL body exceeds {MAX_URL_BYTES} bytes; not fetching further.")
    ext = Path(parsed.path).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS | HTML_EXTENSIONS:
        if ctype in {"text/html", "application/xhtml+xml"}:
            ext = ".html"
        elif ctype == "application/pdf":
            ext = ".pdf"
        elif ctype in {"text/plain", "text/markdown"}:
            ext = ".txt"
        else:
            ext = ".html"
    name = Path(parsed.path).name or "downloaded"
    if not Path(name).suffix:
        name = f"{name}{ext}"
    dest = dest_dir / name
    dest.write_bytes(data)
    return dest


def iter_inputs(raw: str, fetch_dir: Path) -> list[Path]:
    if re.match(r"^https?://", raw, re.I):
        return [fetch_url(raw, fetch_dir)]
    path = Path(raw).expanduser()
    if path.is_dir():
        blocked = refuse_layout(path)
        if blocked:
            raise ExtractionError(blocked)
        files = sorted(
            p for p in path.rglob("*")
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS - CALIBRE_EBOOK_EXTENSIONS
        )
        if not files:
            raise ExtractionError(f"No supported documents under {path}")
        return files
    return [path]


def parse_argv(argv: list[str]) -> dict:
    args = {"mode": "text", "json": False, "out": None, "check": False, "inputs": []}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--check":
            args["check"] = True
        elif a == "--json":
            args["json"] = True
        elif a == "--mode":
            i += 1
            if i >= len(argv) or argv[i] not in {"text", "technical"}:
                raise SystemExit("extract_document.py: --mode must be text or technical")
            args["mode"] = argv[i]
        elif a == "--out":
            i += 1
            if i >= len(argv):
                raise SystemExit("extract_document.py: --out needs a directory")
            args["out"] = Path(argv[i])
        elif a.startswith("--"):
            raise SystemExit(f"extract_document.py: unknown flag {a}")
        else:
            args["inputs"].append(a)
        i += 1
    return args


def strip_install_flags(argv: list[str]) -> list[str]:
    cleaned: list[str] = []
    i = 0
    while i < len(argv):
        if argv[i] == "--no-install-missing":
            i += 1
            continue
        if argv[i] == "--install-missing":
            i += 1
            if i < len(argv) and not argv[i].startswith("--"):
                i += 1
            continue
        cleaned.append(argv[i])
        i += 1
    return cleaned


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    install_mode = normalize_install_mode(argv)
    try:
        args = parse_argv(strip_install_flags(argv))
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        return 2

    if args["check"]:
        return run_dependency_check()
    if not args["inputs"]:
        print(
            "usage: extract_document.py [--check] [--mode text|technical] [--json] [--out DIR] <file-or-url...>",
            file=sys.stderr,
        )
        return 2

    out_dir = args["out"] or Path(tempfile.mkdtemp(prefix="convert-as-skill-"))
    out_dir.mkdir(parents=True, exist_ok=True)
    fetch_dir = out_dir / "_fetched"
    fetch_dir.mkdir(exist_ok=True)

    results = []
    failed = 0
    for raw in args["inputs"]:
        try:
            paths = iter_inputs(raw, fetch_dir)
            for path in paths:
                extracted = extract_single_file(path, args["mode"], install_mode)
                text = extracted.pop("text")
                stem = Path(extracted["filename"]).stem
                text_path = out_dir / f"{stem}.txt"
                meta_path = out_dir / f"{stem}.meta.json"
                text_path.write_text(text, encoding="utf-8")
                extracted["text_path"] = str(text_path)
                meta_path.write_text(json.dumps(extracted, indent=2) + "\n", encoding="utf-8")
                results.append(extracted)
                print(
                    f"extracted {path} -> {text_path} "
                    f"({extracted['extraction_method']}, "
                    f"{extracted['chapters_detected']} chapters via {extracted['chapters_method']})"
                )
        except ExtractionError as exc:
            print(f"error   {raw}: {exc}", file=sys.stderr)
            failed += 1

    if args["json"]:
        print(json.dumps(results, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
