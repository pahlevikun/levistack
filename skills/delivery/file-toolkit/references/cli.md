# Command-line contract

`files.py` accepts `capabilities`, `inspect`, `extract`, `create`, `convert` and
`animate`. JSON goes to stdout; a JSON error goes to stderr with exit 2. A failed
command is not a completed output. Help is available on every subcommand.

Inputs are local regular files up to 64 MiB. Symlink inputs are rejected. ZIP
packages have at most 10,000 members and 64 MiB total declared expansion; XML
parts are bounded to 8 MiB and reject DTD/entity declarations. Package members
are read in place, never extracted onto the filesystem. Unsafe archive paths and
symlink members are rejected. Processing an untrusted file still needs the normal
OS sandbox and patched native backends; these checks are not a complete parser
security boundary.

Output directories must exist. Existing files require `--overwrite`; symlink
outputs are refused even with that flag. Work is generated in a temporary directory
next to the destination. Failed backend output is discarded. Without overwrite,
publication uses exclusive creation and cannot replace a file that appeared
concurrently. With overwrite, a successful result replaces the selected file.
Do not run concurrent writers against the same output path.

Subprocesses receive argument arrays, no shell expansion. Paths become absolute
before external tools see them. Tools run with a 45-second timeout. No backend is
installed automatically. Usual optional commands are ImageMagick `magick`, FFmpeg
`ffmpeg`/`ffprobe`, Poppler `pdftotext`, Tesseract `tesseract`, and LibreOffice
`soffice`. `capabilities` also reports Pandoc availability for a separately chosen
native workflow; this script does not currently invoke Pandoc.

`extract` returns the normalized model; `inspect` wraps it with extension and byte
size. They print content intentionally: redirect private output to an appropriate
local file and keep it out of shared logs. `--output` writes the JSON result to a
file as well. `--ocr` only adds OCR text for an image; PDF OCR is a separate
render-and-OCR workflow.

`create` and `convert` accept `--backend office` to select installed LibreOffice
explicitly. This uses a fresh per-run profile and a temporary output directory;
it is not a silent fallback. Native reconstruction is the default. For a Unicode
PDF, create with `--backend office` from the document model when LibreOffice is
available. The office backend still needs its own visual/content verification.

`create` expects an explicit model with `kind`. Use the bundled template for that
kind or edit an extracted model. `convert --allow-lossy` invokes actual image/audio
transcoding, office conversion for legacy inputs, or extracts then reconstructs
normalized content. The flag acknowledges possible loss; it does not certify it
acceptable for the user's task. Unsupported model-to-format pairs fail.

`animate` takes an exact ordered frame list, not a glob, with 1–300 frames and
1–60 requested FPS. Every input must decode to one frame, and all dimensions must
match. GIF timing is quantized to hundredths of a second. It needs ImageMagick.
The command re-reads the produced GIF, checks count and dimensions, and returns
`delays_centiseconds`, `duration_seconds` and `fps_effective` alongside
`fps_requested`. For example, an 8 FPS request may produce 12-centisecond delays
and an effective rate of about 8.33 FPS. Playback software may impose additional
minimum delays. Use the observed receipt for duration/rate claims.
