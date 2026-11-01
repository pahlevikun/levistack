# Format coverage and fidelity

Use the installed machine's `capabilities` result. This table describes the
implementation paths, not a promise that optional tools are installed.

| Family | Native operations | Optional operations | Important limit |
|---|---|---|---|
| Text/data | UTF-8 TXT, MD, raw RST/TeX/AsciiDoc, JSON, XML, CSV/TSV, basic RTF | User-selected external typesetters | Markup is retained as raw content unless a supported parser handles it |
| Word processing | Create/extract simple DOCX and ODT | Legacy DOC via LibreOffice | Reconstruction loses styles, fields, edits, media and page layout |
| Slides | Create/extract basic text PPTX and ODP | Legacy PPT via LibreOffice | No charts, shapes/media reconstruction or theme cloning |
| Sheets | Create/extract XLSX and ODS; sparse cells to CSV/TSV | Legacy XLS via LibreOffice | No formula evaluation, chart recreation, style retention or cached-value guarantee |
| PDF | Create simple text PDF with built-in font | Extract text through Poppler; office PDF export for Unicode/layout via explicit office backend | Native creation supports Windows-1252; no OCR, exact reflow, forms or signing |
| EPUB | Create a simple EPUB and extract spine text | Native readers for visual check | No media, complex CSS or exact reading-layout recreation |
| Images | Create/inspect safe simple SVG scenes | ImageMagick codec registry for inspection, creation and conversion | Alpha, profiles, layers, metadata and animation may change |
| Audio | Create/inspect uncompressed PCM WAV tones/silence | FFmpeg conversion, FFprobe metadata | No speech transcription, denoising promise or perceptual-quality certification |

Common image targets include PNG, JPEG, WebP, GIF, TIFF, BMP, ICO, SVG, AVIF,
HEIC/HEIF and additional formats present in the ImageMagick registry. `capabilities`
returns its actual read/write flags. A listed codec may require an unavailable
delegate or be blocked by the installed policy. RAW cameras, layered PSD, HDR and
vector formats need file-specific verification. Source SVGs with scripts, event
handlers, external references or CSS resource URLs are refused.

Common audio targets include WAV, MP3, FLAC, OGG, AAC, M4A, OPUS, AIFF and WMA.
`capabilities --details` includes the installed FFmpeg encoder/muxer lists. The
container, audio encoder and sample representation must all be available. Native
WAV inspection supports Python's PCM wave reader; other encodings need FFprobe or
transcoding. Changing extension alone changes no samples.

Extraction and recreation are intentionally separate. A parsed sheet retains
formula strings and coordinates; a new workbook marks itself for recalculation
when opened in a suitable application. That does not create cached results now.
PDF-to-DOCX is a text reconstruction, not preservation of original page objects.
An image metadata read is not an OCR result. An audio metadata read is not a
transcript. Keep those differences visible in the delivery report.

Native document packages are checked through their parsed structure and synthetic
round trips. They still need a real target viewer for visual acceptance. Exact
editing of an arbitrary existing file should use a format-aware editor that
preserves unsupported features rather than round-tripping through the reduced model.
