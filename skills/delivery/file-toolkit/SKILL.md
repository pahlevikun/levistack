---
name: file-toolkit
description: "Inspect, parse, extract, create, recreate and convert local documents, spreadsheets, presentations, images and audio through a reusable command-line toolkit. Use when a file format is the task: DOCX, PDF, PPTX, XLSX, ODF, EPUB, delimited data, text markup, raster/vector images, animated GIFs or sound files. Detects installed codecs and optional backends. Not for researching or drafting the document's facts (create-documentation), choosing visual art (visual-art), or editing a cloud file through a connector."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: delivery
  category: delivery
  department: delivery
  related_skills:
    - create-documentation
    - visual-art
    - verify
    - mcp-management
  tags:
    - files
    - document
    - image
    - audio
    - parse
    - create
    - convert
  capabilities:
    - format_capability_discovery
    - structured_file_extraction
    - document_creation
    - image_conversion
    - audio_conversion
    - frame_animation
  languages:
    - en

---

# File toolkit

Use the existing script before writing a custom conversion program. It works
locally, leaves source files untouched, and reports missing backends explicitly.
A successful conversion does not prove layout, formulas or meaning survived.

## Choose the operation

| Request | Command | What to check |
|---|---|---|
| What can this machine read/write? | `capabilities` or `capabilities --details` | Actual installed backend and codec support |
| Understand a file | `inspect INPUT` | Format, structure, metadata and warnings |
| Parse content into a reusable model | `extract INPUT --output parsed.json` | Extracted sections/cells/slides versus the original |
| Make or recreate a file | `create SPEC.json --output OUTPUT` | Supported content spec and output representation |
| Change representation | `convert INPUT --output OUTPUT --allow-lossy` | Expected losses and visual/content checks |
| Build a GIF from exact frames | `animate FRAME... --output OUTPUT.gif --fps 12` | Equal single-frame inputs, decoded timing/count and final size |

All commands use [scripts/files.py](scripts/files.py). The script requires Python
3.9 or later; it does not install dependencies or contact remote services.

```sh
python3 <skill-dir>/scripts/files.py capabilities
python3 <skill-dir>/scripts/files.py extract source.docx --output parsed.json
python3 <skill-dir>/scripts/files.py create parsed.json --output recreated.odt
python3 <skill-dir>/scripts/files.py convert source.png --output target.webp --allow-lossy
python3 <skill-dir>/scripts/files.py animate frame-1.png frame-2.png --output loop.gif --fps 10
```

Read [the CLI contract](references/cli.md) before mutation and
[format support and limits](references/formats.md) before promising a conversion.
Use [content models](references/content-models.md) to edit parsed content, then
recreate it without building a new generator.

## Execute and verify

1. Identify the requested source and output formats. Inspect the source and run
   capabilities. Keep a missing encoder, parser or renderer visible; never rename
   a file extension and call it conversion.
2. Establish what must survive: text, formulas, cell coordinates, slide ordering,
   transparency, animation, audio duration/channels, metadata or exact layout.
   If the normalized model cannot represent it, select a suitable installed native
   editor/backend or report the gap before reconstruction.
3. Read or create a content spec. Reuse templates:
   [document](templates/document.json), [sheet](templates/spreadsheet.json),
   [slides](templates/presentation.json), [image](templates/image.json),
   [audio](templates/audio.json). Retain real evidence and synthetic examples as
   distinct content; format conversion is not permission to invent missing data.
4. Write to a new output path. Overwrite requires `--overwrite`; a symlink output
   is refused. Source and destination must differ. Temporary output is published
   only after the backend succeeds. Do not enable macros, fetch embedded remote
   resources, or send private files to a third-party converter.
5. Re-extract the result and compare the important fields. Render and visually
   inspect documents/slides/images with an available appropriate viewer. Listen
   to audio when sound quality matters. A structural round trip is not a visual
   inspection; declare the latter unrun when a viewer is unavailable.
6. Report the output path, verified content/codec properties, known feature loss,
   and the exact unavailable backend. Keep tool diagnostics free of file contents
   and credentials. Stop after the requested artifact and its checks exist.

## Important boundaries

- Native reconstruction produces simple editable text documents, basic sheets
  and text slides. It does not preserve arbitrary formatting, macros, signatures,
  charts, embedded media, tracked changes or original pagination.
- Spreadsheet formulas are stored and extracted, not evaluated. Do not claim a
  workbook is recalculated or financially correct without an independent check.
- PDF text extraction needs `pdftotext`; scanned pages may produce no text. Image
  OCR is explicit with `extract IMAGE --ocr` and needs `tesseract`.
- Audio parsing means technical metadata. Transcription, speaker identification,
  speech synthesis and semantic reconstruction are not provided. Native audio
  creation is a bounded synthetic tone or silence.
- Image support comes from the installed codec registry. A listed codec can still
  fail because a delegate, policy, profile or file feature is unavailable. Do not
  promise every image or audio format on every machine.

## Verification

Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s <skill-dir>/tests -v`
for [tests/test_files.py](tests/test_files.py). Run the task scenarios in
[evals/evals.json](evals/evals.json) when changing routing or completion claims.

## Related skills

- `create-documentation`: facts, reader intent and document authoring.
- `visual-art`: art direction, reproducible scenes and creative motion.
- `infographic`: sourced data and visual explanations.
- `verify`: evidence for the artifact and its claimed properties.
