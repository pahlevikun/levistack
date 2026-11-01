#!/usr/bin/env python3
"""Local format inspection, normalized content, creation and explicit conversion."""
import argparse
import contextlib
import functools
import csv
import html
from html.parser import HTMLParser
import io
import json
import math
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import textwrap
import wave
import xml.etree.ElementTree as ET
import zipfile

LIMIT = 64 * 1024 * 1024
XML_LIMIT = 8 * 1024 * 1024
TIMEOUT = 45
TEXT = {'txt', 'md', 'markdown', 'html', 'htm', 'json', 'csv', 'tsv', 'xml', 'rtf', 'rst', 'tex', 'adoc'}
LEGACY = {'doc': 'docx', 'xls': 'xlsx', 'ppt': 'pptx'}
DOC = {'docx', 'odt', 'pdf', 'epub'}
SHEET = {'xlsx', 'ods'}
SLIDE = {'pptx', 'odp'}
IMAGES = {'png', 'jpg', 'jpeg', 'webp', 'gif', 'tif', 'tiff', 'bmp', 'svg', 'avif', 'heic', 'heif', 'ico', 'jxl', 'exr', 'pnm', 'ppm', 'pbm', 'pgm', 'psd', 'eps'}
AUDIO = {'wav', 'mp3', 'flac', 'ogg', 'aac', 'm4a', 'opus', 'aiff', 'aif', 'wma'}
N = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
     'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
     'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
     's': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
     'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
     'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
     'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
     'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
     'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0'}


class FormatError(ValueError):
    pass


def run(args, timeout=TIMEOUT):
    try:
        result = subprocess.run([str(a) for a in args], capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise FormatError('backend timed out after %s seconds' % timeout)
    except OSError:
        raise FormatError('required backend executable is unavailable: ' + str(args[0]))
    if result.returncode:
        # Backend errors can include user content. Keep output out of routine logs.
        raise FormatError('%s failed with exit %s; inspect the source and backend policy' % (Path(str(args[0])).name, result.returncode))
    if len(result.stdout) > LIMIT:
        raise FormatError('backend output exceeds size bound')
    return result.stdout.decode('utf-8', errors='replace')


def source(path):
    p = Path(path).expanduser().absolute()
    if p.is_symlink() or not p.is_file():
        raise FormatError('input must be an existing regular file, not a symlink')
    if p.stat().st_size > LIMIT:
        raise FormatError('input exceeds 64 MiB bound')
    return p


def xml(data):
    if len(data) > XML_LIMIT or b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        raise FormatError('XML exceeds bounds or contains a forbidden declaration')
    try:
        return ET.fromstring(data)
    except ET.ParseError as error:
        raise FormatError('malformed XML: ' + str(error))


@contextlib.contextmanager
def package(path):
    try:
        with zipfile.ZipFile(path) as z:
            infos = z.infolist()
            if len(infos) > 10000 or sum(i.file_size for i in infos) > LIMIT:
                raise FormatError('archive expansion exceeds bounds')
            for i in infos:
                if i.filename.startswith('/') or '..' in Path(i.filename).parts or ((i.external_attr >> 16) & 0o170000) == 0o120000:
                    raise FormatError('archive contains an unsafe path or symlink')
            yield z
    except (zipfile.BadZipFile, KeyError) as error:
        raise FormatError('invalid or incomplete document package: ' + str(error))


def ext(path):
    return Path(path).suffix.lower().lstrip('.')


def require(name):
    exe = shutil.which(name)
    if not exe:
        raise FormatError('missing optional backend: ' + name + '; run capabilities for alternatives')
    return exe


def output(path, writer, overwrite=False):
    p = Path(path).expanduser().absolute()
    if p.is_symlink() or (p.exists() and not overwrite):
        raise FormatError('output already exists or is a symlink; choose another path or use --overwrite')
    if not p.parent.is_dir():
        raise FormatError('output directory must already exist')
    with tempfile.TemporaryDirectory(prefix='.file-toolkit-', dir=str(p.parent)) as d:
        temp = Path(d) / ('result.' + ext(p))
        writer(temp)
        if not temp.is_file() or temp.stat().st_size == 0:
            raise FormatError('backend produced no output')
        if temp.stat().st_size > LIMIT:
            raise FormatError('output exceeds 64 MiB bound')
        if overwrite:
            if p.is_symlink():
                raise FormatError('output changed to a symlink')
            os.replace(str(temp), str(p))
        else:
            # O_EXCL publication protects against an output created after preflight.
            try:
                with p.open('xb') as dest, temp.open('rb') as src:
                    shutil.copyfileobj(src, dest)
            except FileExistsError:
                raise FormatError('output appeared during processing; nothing overwritten')
    return p


class PlainHTML(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []; self.hidden = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.hidden += 1
        if tag in ('p', 'div', 'br', 'h1', 'h2', 'h3', 'li', 'tr'): self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.hidden: self.hidden -= 1
    def handle_data(self, data):
        if not self.hidden: self.parts.append(data)


def plain_html(text):
    parser = PlainHTML(); parser.feed(text)
    return '\n'.join(s.strip() for s in ''.join(parser.parts).splitlines() if s.strip())


def elements_text(root, tag):
    return ''.join(e.text or '' for e in root.iter(tag))


def col(index):
    text = ''
    while index:
        index, rem = divmod(index - 1, 26); text = chr(65 + rem) + text
    return text


def uncol(text):
    n = 0
    for c in text: n = n * 26 + ord(c) - 64
    return n


def read_office(path):
    extension = ext(path)
    with package(path) as z:
        if extension == 'docx':
            root = xml(z.read('word/document.xml'))
            paragraphs = [elements_text(p, '{%s}t' % N['w']) for p in root.iter('{%s}p' % N['w'])]
            return {'kind': 'document', 'title': '', 'paragraphs': paragraphs, 'warnings': ['Text extraction does not preserve page layout, fields or tracked changes.']}
        if extension == 'pptx':
            names = sorted((n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)), key=lambda n: int(re.search(r'(\d+)\.xml', n).group(1)))
            slides = []
            for name in names:
                root = xml(z.read(name)); paras = [elements_text(p, '{%s}t' % N['a']) for p in root.iter('{%s}p' % N['a'])]
                slides.append({'title': paras[0] if paras else '', 'paragraphs': paras[1:]})
            return {'kind': 'presentation', 'slides': slides, 'warnings': ['Text-only slide extraction; shapes, charts, notes and order changes in custom relationships are not reconstructed.']}
        shared = []
        if 'xl/sharedStrings.xml' in z.namelist():
            shared = [elements_text(si, '{%s}t' % N['s']) for si in xml(z.read('xl/sharedStrings.xml')).iter('{%s}si' % N['s'])]
        workbook = xml(z.read('xl/workbook.xml'))
        rels = xml(z.read('xl/_rels/workbook.xml.rels'))
        targets = {r.get('Id'): r.get('Target') for r in rels}
        sheets = []
        for sheet in workbook.findall('s:sheets/s:sheet', N):
            target = targets.get(sheet.get('{%s}id' % N['r']), '')
            name = target.lstrip('/') if target.startswith('/') else 'xl/' + target
            if '..' in Path(name).parts: raise FormatError('unsupported parent-relative worksheet relationship')
            data = xml(z.read(name)); cells = []
            for c in data.iter('{%s}c' % N['s']):
                ref = c.get('r', ''); value = c.find('s:v', N); formula = c.find('s:f', N)
                if formula is not None:
                    v = '=' + (formula.text or '')
                elif c.get('t') == 'inlineStr': v = elements_text(c, '{%s}t' % N['s'])
                elif c.get('t') == 's': v = shared[int(value.text)] if value is not None else ''
                elif c.get('t') == 'b': v = value is not None and value.text == '1'
                else:
                    raw = value.text if value is not None else ''
                    try: v = float(raw) if '.' in raw else int(raw)
                    except (ValueError, TypeError): v = raw or ''
                cells.append({'cell': ref, 'value': v})
            sheets.append({'name': sheet.get('name', ''), 'cells': cells})
        return {'kind': 'spreadsheet', 'sheets': sheets, 'formulas_evaluated': False,
                'warnings': ['Formulas are retained, not recalculated. Styles, charts and external links are not reconstructed.']}


def read_odf(path):
    with package(path) as z: root = xml(z.read('content.xml'))
    extension = ext(path)
    if extension == 'odt':
        return {'kind': 'document', 'title': '', 'paragraphs': [''.join(e.itertext()) for e in root.iter() if e.tag in ('{%s}p' % N['text'], '{%s}h' % N['text'])]}
    if extension == 'odp':
        return {'kind': 'presentation', 'slides': [{'title': page.get('{%s}name' % N['draw'], ''), 'paragraphs': [''.join(e.itertext()) for e in page.iter('{%s}p' % N['text'])]} for page in root.iter('{%s}page' % N['draw'])]}
    sheets = []
    for table in root.iter('{%s}table' % N['table']):
        rows = []
        for row in table.findall('table:table-row', N):
            repeat = int(row.get('{%s}number-rows-repeated' % N['table'], '1'))
            if repeat > 10000: raise FormatError('ODF row repetition exceeds bound')
            values = []
            for c in row:
                times = int(c.get('{%s}number-columns-repeated' % N['table'], '1'))
                if times > 10000: raise FormatError('ODF column repetition exceeds bound')
                formula = c.get('{%s}formula' % N['table'])
                val = c.get('{%s}value' % N['office'])
                v = '=' + formula.split('=', 1)[-1] if formula else (float(val) if val is not None else ''.join(c.itertext()))
                values.extend([v] * times)
            if len(rows) + repeat > 10000: raise FormatError('ODF expanded rows exceed bound')
            rows.extend([list(values) for _ in range(repeat)])
        sheets.append({'name': table.get('{%s}name' % N['table'], ''), 'rows': rows})
    return {'kind': 'spreadsheet', 'sheets': sheets, 'formulas_evaluated': False}


def validate_svg(path):
    root = xml(path.read_bytes())
    for e in root.iter():
        if e.tag.split('}')[-1] in ('script', 'foreignObject'):
            raise FormatError('active SVG content is not supported')
        for key, value in e.attrib.items():
            if key.lower().startswith('on') or key.split('}')[-1] == 'href' or 'url(' in value.lower():
                raise FormatError('SVG event handlers and linked resources are not supported')
    return root


def rtf_text(text):
    parts=[]; depth=0; hidden=None
    tokens=re.findall(r"\\'[0-9a-fA-F]{2}|\\u-?\d+\??|\\[A-Za-z]+-?\d* ?|\\[\\{}]|[{}]|[^\\{}]+|\\.",text)
    for token in tokens:
        if token=='{': depth+=1;continue
        if token=='}':
            if hidden==depth:hidden=None
            depth-=1;continue
        if token.strip() in ('\\fonttbl','\\colortbl','\\stylesheet','\\info','\\pict','\\object'):
            hidden=depth
        if hidden is not None:continue
        if token.startswith("\\'"):parts.append(bytes([int(token[2:],16)]).decode('cp1252'))
        elif re.fullmatch(r'\\u-?\d+\??',token):parts.append(chr(int(token[2:].rstrip('?'))%65536))
        elif token in ('\\\\','\\{','\\}'):parts.append(token[1:])
        elif token.strip() in ('\\par','\\line'):parts.append('\n')
        elif token.strip()=='\\tab':parts.append('\t')
        elif not token.startswith('\\'):parts.append(token)
    return ''.join(parts).encode('utf-16-le',errors='surrogatepass').decode('utf-16-le',errors='replace')


def extract(path, ocr=False):
    path = source(path); extension = ext(path)
    if extension in LEGACY:
        with tempfile.TemporaryDirectory() as d:
            made = office_convert(path, LEGACY[extension], d)
            return extract(made)
    if extension in ('docx', 'pptx', 'xlsx'): return read_office(path)
    if extension in ('odt', 'odp', 'ods'): return read_odf(path)
    if extension == 'epub':
        with package(path) as z:
            container = xml(z.read('META-INF/container.xml'))
            opf_name = next(e.get('full-path') for e in container.iter() if e.tag.endswith('}rootfile'))
            opf = xml(z.read(opf_name))
            manifest = {e.get('id'): e.get('href') for e in opf.iter() if e.tag.endswith('}item')}
            names = [str(Path(opf_name).parent / manifest[e.get('idref')]) for e in opf.iter() if e.tag.endswith('}itemref')]
            if any('..' in Path(n).parts or ':' in n or n.startswith('/') for n in names): raise FormatError('unsupported EPUB content path')
            paragraphs = [plain_html(z.read(n).decode('utf-8')) for n in names]
        return {'kind': 'document', 'title': '', 'paragraphs': paragraphs, 'warnings': ['Text-only EPUB extraction; reading order and layout may differ.']}
    if extension == 'pdf':
        result = run([require('pdftotext'), '-layout', str(path), '-'])
        return {'kind': 'document', 'title': '', 'paragraphs': result.splitlines(), 'warnings': ['No OCR performed. Empty text may indicate scanned pages. Layout is not reconstructed.']}
    if extension in AUDIO:
        if extension == 'wav':
            with wave.open(str(path)) as f:
                return {'kind': 'audio', 'channels': f.getnchannels(), 'sample_rate': f.getframerate(), 'sample_width': f.getsampwidth(), 'frames': f.getnframes(), 'duration_seconds': f.getnframes() / f.getframerate(), 'transcription': 'not performed'}
        return {'kind': 'audio', 'probe': json.loads(run([require('ffprobe'), '-v', 'error', '-show_format', '-show_streams', '-of', 'json', path])), 'transcription': 'not performed'}
    if is_image(extension):
        if extension == 'svg':
            r = validate_svg(path); result = {'kind': 'image', 'format': 'SVG', 'width': r.get('width'), 'height': r.get('height'), 'viewBox': r.get('viewBox')}
        else:
            result = {'kind': 'image', 'frames': run([require('magick'), 'identify', '-format', '%m %w %h %n\n', path]).splitlines()}
        if ocr: result['text'] = run([require('tesseract'), str(path), 'stdout'])
        return result
    if extension not in TEXT: raise FormatError('unsupported extraction format: ' + extension)
    text = path.read_text(encoding='utf-8')
    if extension == 'json': return json.loads(text)
    if extension in ('csv', 'tsv'):
        return {'kind': 'spreadsheet', 'sheets': [{'name': 'Sheet1', 'rows': list(csv.reader(io.StringIO(text), delimiter='\t' if extension == 'tsv' else ','))}]}
    if extension in ('html', 'htm'): text = plain_html(text)
    if extension == 'xml': xml(path.read_bytes())
    if extension == 'rtf': text = rtf_text(text)
    return {'kind': 'document', 'title': '', 'paragraphs': text.splitlines(), 'warnings': ['Plain content extraction; source formatting may not survive recreation.']}


def sheet_rows(sheet):
    if 'cells' not in sheet: return sheet.get('rows', [])
    values = {}
    for cell in sheet['cells']:
        match = re.fullmatch(r'([A-Z]{1,3})([1-9]\d*)', cell.get('cell', ''))
        if not match: raise FormatError('invalid sparse cell')
        row, column = int(match.group(2)), uncol(match.group(1))
        if row > 10000 or column > 1024: raise FormatError('dense conversion exceeds bounds')
        values[(row,column)] = cell.get('value','')
    max_row = max((r for r,c in values), default=0); max_col = max((c for r,c in values), default=0)
    if max_row * max_col > 100000: raise FormatError('dense conversion exceeds 100,000 cells')
    return [[values.get((r,c),'') for c in range(1,max_col+1)] for r in range(1,max_row+1)]


def document_lines(spec):
    if spec.get('kind') == 'presentation':
        return [line for slide in spec.get('slides', []) for line in [slide.get('title', '')] + slide.get('paragraphs', [])]
    if spec.get('kind') == 'spreadsheet':
        return ['\t'.join(str(v) for v in row) for sheet in spec.get('sheets', []) for row in sheet_rows(sheet)]
    return ([spec['title']] if spec.get('title') else []) + spec.get('paragraphs', [])


def escaped(s): return html.escape(str(s), quote=True)


def zip_write(path, members):
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in members.items(): z.writestr(name, data)


def rels(entries):
    return '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join('<Relationship Id="%s" Type="%s" Target="%s"/>' % (escaped(i), escaped(t), escaped(p)) for i, t, p in entries) + '</Relationships>'


def office_write(spec, path):
    extension = ext(path)
    main_type = {'docx': 'wordprocessingml.document', 'xlsx': 'spreadsheetml.sheet', 'pptx': 'presentationml.presentation'}[extension]
    main_path = {'docx': 'word/document.xml', 'xlsx': 'xl/workbook.xml', 'pptx': 'ppt/presentation.xml'}[extension]
    members = {'_rels/.rels': rels([('rId1', N['r'] + '/officeDocument', main_path)])}
    types = {main_path: 'application/vnd.openxmlformats-officedocument.' + main_type + '.main+xml'}
    if extension == 'docx':
        paras = ''.join('<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % escaped(s) for s in document_lines(spec))
        members[main_path] = '<w:document xmlns:w="%s"><w:body>%s<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr></w:body></w:document>' % (N['w'], paras)
    elif extension == 'xlsx':
        sheets = spec.get('sheets', [])
        if not sheets: raise FormatError('spreadsheet needs at least one sheet')
        names = [s.get('name', 'Sheet%s' % (i + 1)) for i, s in enumerate(sheets)]
        if len(names) != len(set(names)) or any(not n or len(n) > 31 or re.search(r'[\\/*?:\[\]]', n) for n in names): raise FormatError('sheet names must be unique valid names of at most 31 characters')
        members[main_path] = '<workbook xmlns="%s" xmlns:r="%s"><sheets>%s</sheets><calcPr fullCalcOnLoad="1"/></workbook>' % (N['s'], N['r'], ''.join('<sheet name="%s" sheetId="%s" r:id="rId%s"/>' % (escaped(n), i, i) for i, n in enumerate(names, 1)))
        members['xl/_rels/workbook.xml.rels'] = rels([('rId%s' % i, N['r'] + '/worksheet', 'worksheets/sheet%s.xml' % i) for i in range(1, len(sheets) + 1)])
        for i, sheet in enumerate(sheets, 1):
            cells = sheet.get('cells')
            if cells is None: cells = [{'cell': col(c) + str(r), 'value': v} for r, row in enumerate(sheet.get('rows', []), 1) for c, v in enumerate(row, 1)]
            grouped = {}
            for cell in cells:
                ref = cell.get('cell', ''); v = cell.get('value', '')
                m = re.fullmatch(r'([A-Z]{1,3})([1-9]\d{0,6})', ref)
                if not m or uncol(m.group(1)) > 16384 or int(m.group(2)) > 1048576: raise FormatError('invalid cell reference')
                if isinstance(v, bool): node = '<c r="%s" t="b"><v>%s</v></c>' % (ref, int(v))
                elif isinstance(v, (int, float)) and math.isfinite(v): node = '<c r="%s"><v>%s</v></c>' % (ref, v)
                elif isinstance(v, str) and v.startswith('='): node = '<c r="%s"><f>%s</f></c>' % (ref, escaped(v[1:]))
                else: node = '<c r="%s" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>' % (ref, escaped(v))
                grouped.setdefault(int(m.group(2)), []).append(node)
            part = 'xl/worksheets/sheet%s.xml' % i
            members[part] = '<worksheet xmlns="%s"><sheetData>%s</sheetData></worksheet>' % (N['s'], ''.join('<row r="%s">%s</row>' % (r, ''.join(grouped[r])) for r in sorted(grouped)))
            types[part] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml'
    else:
        slides = spec.get('slides', [])
        if not slides: raise FormatError('presentation needs at least one slide')
        members[main_path] = '<p:presentation xmlns:p="%s" xmlns:r="%s"><p:sldIdLst>%s</p:sldIdLst><p:sldSz cx="9144000" cy="5143500"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>' % (N['p'], N['r'], ''.join('<p:sldId id="%s" r:id="rId%s"/>' % (255 + i, i) for i in range(1, len(slides) + 1)))
        members['ppt/_rels/presentation.xml.rels'] = rels([('rId%s' % i, N['r'] + '/slide', 'slides/slide%s.xml' % i) for i in range(1, len(slides) + 1)])
        for i, slide in enumerate(slides, 1):
            texts = [slide.get('title', '')] + slide.get('paragraphs', [])
            shapes = []
            for j, text in enumerate(texts, 1):
                shapes.append('<p:sp><p:nvSpPr><p:cNvPr id="%s" name="Text %s"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="600000" y="%s"/><a:ext cx="7900000" cy="500000"/></a:xfrm></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="%s"/><a:t>%s</a:t></a:r></a:p></p:txBody></p:sp>' % (j + 1, j, 400000 + (j - 1) * 550000, 2800 if j == 1 else 1800, escaped(text)))
            part = 'ppt/slides/slide%s.xml' % i
            members[part] = '<p:sld xmlns:p="%s" xmlns:a="%s"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>%s</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>' % (N['p'], N['a'], ''.join(shapes))
            types[part] = 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml'
    members['[Content_Types].xml'] = '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>%s</Types>' % ''.join('<Override PartName="/%s" ContentType="%s"/>' % item for item in types.items())
    for name, data in members.items():
        if name.endswith(('.xml','.rels')): xml(data.encode())
    zip_write(path, members)


def odf_write(spec, path):
    extension = ext(path); subtype = {'odt': 'text', 'ods': 'spreadsheet', 'odp': 'presentation'}[extension]
    if subtype == 'text': body = ''.join('<text:p>%s</text:p>' % escaped(s) for s in document_lines(spec))
    elif subtype == 'presentation':
        body = ''.join('<draw:page draw:name="%s"><draw:frame><draw:text-box>%s</draw:text-box></draw:frame></draw:page>' % (escaped(s.get('title', 'Slide')), ''.join('<text:p>%s</text:p>' % escaped(t) for t in s.get('paragraphs', []))) for s in spec.get('slides', []))
    else:
        body = ''
        for sheet in spec.get('sheets', []):
            rows = []
            for row in sheet_rows(sheet):
                cells = []
                for value in row:
                    if isinstance(value, (int, float)) and not isinstance(value, bool): attrs = 'office:value-type="float" office:value="%s"' % value
                    elif isinstance(value, str) and value.startswith('='): attrs = 'table:formula="of:%s" office:value-type="float"' % escaped(value)
                    else: attrs = 'office:value-type="string"'
                    cells.append('<table:table-cell %s><text:p>%s</text:p></table:table-cell>' % (attrs, escaped(value)))
                rows.append('<table:table-row>%s</table:table-row>' % ''.join(cells))
            body += '<table:table table:name="%s">%s</table:table>' % (escaped(sheet.get('name', 'Sheet1')), ''.join(rows))
    namespaces = ' '.join('xmlns:%s="%s"' % (k, N[k]) for k in ('office', 'text', 'table', 'draw'))
    content = '<office:document-content %s xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" office:version="1.2"><office:body><office:%s>%s</office:%s></office:body></office:document-content>' % (namespaces, subtype, body, subtype)
    xml(content.encode())
    mime = 'application/vnd.oasis.opendocument.' + subtype
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('mimetype', mime, compress_type=zipfile.ZIP_STORED)
        z.writestr('content.xml', content)
        z.writestr('META-INF/manifest.xml', '<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2"><manifest:file-entry manifest:full-path="/" manifest:media-type="%s"/><manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/></manifest:manifest>' % mime)


def pdf_write(spec, path):
    lines = [part for line in document_lines(spec) for part in (textwrap.wrap(line, width=82) or [''])]
    try: lines = [s.encode('cp1252') for s in lines]
    except (UnicodeEncodeError, AttributeError): raise FormatError('native PDF supports plain Windows-1252 text; use a Unicode-capable document backend for other scripts')
    # Fixed simple text pages. Reflow is explicit content reconstruction, not layout cloning.
    pages = [lines[i:i + 45] for i in range(0, len(lines), 45)] or [[]]
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>', b'', b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>']
    kids = []
    for page in pages:
        page_id = len(objects) + 1; content_id = page_id + 1; kids.append('%s 0 R' % page_id)
        stream = b'BT /F1 12 Tf 50 790 Td 16 TL\n' + b'\n'.join(b'(' + s.replace(b'\\', b'\\\\').replace(b'(', b'\\(').replace(b')', b'\\)') + b') Tj T*' for s in page) + b'\nET'
        objects.extend([('<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents %s 0 R >>' % content_id).encode(), b'<< /Length %d >>\nstream\n' % len(stream) + stream + b'\nendstream'])
    objects[1] = ('<< /Type /Pages /Kids [%s] /Count %s >>' % (' '.join(kids), len(pages))).encode()
    result = bytearray(b'%PDF-1.4\n'); offsets = [0]
    for i, obj in enumerate(objects, 1): offsets.append(len(result)); result.extend(('%s 0 obj\n' % i).encode() + obj + b'\nendobj\n')
    start = len(result); result.extend(('xref\n0 %s\n0000000000 65535 f \n' % (len(objects) + 1)).encode())
    for offset in offsets[1:]: result.extend(('%010d 00000 n \n' % offset).encode())
    result.extend(('trailer\n<< /Size %s /Root 1 0 R >>\nstartxref\n%s\n%%%%EOF\n' % (len(objects) + 1, start)).encode()); path.write_bytes(result)


def svg_write(spec, path):
    width, height = int(spec.get('width', 640)), int(spec.get('height', 480))
    if not 1 <= width <= 8192 or not 1 <= height <= 8192: raise FormatError('image dimensions must be 1..8192')
    def color(value):
        if not re.fullmatch(r'#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?|none|transparent', str(value)): raise FormatError('use hex, none or transparent colors')
        return value
    shapes = ['<rect width="100%%" height="100%%" fill="%s"/>' % color(spec.get('background', '#ffffff'))]
    for s in spec.get('shapes', []):
        kind = s.get('type'); attrs = {'rect': ('x','y','width','height','rx'), 'circle': ('cx','cy','r'), 'line': ('x1','y1','x2','y2'), 'text': ('x','y','font-size')}.get(kind)
        if attrs is None: raise FormatError('supported shapes: rect, circle, line, text')
        values = []
        for key in attrs:
            if key in s:
                value = float(s[key])
                if not math.isfinite(value) or abs(value) > 100000: raise FormatError('invalid shape coordinate')
                values.append('%s="%s"' % (key, value))
        values.extend(['fill="%s"' % color(s.get('fill','#000000')), 'stroke="%s"' % color(s.get('stroke','none'))])
        shapes.append('<%s %s>%s</%s>' % (kind, ' '.join(values), escaped(s.get('text','')) if kind == 'text' else '', kind))
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" viewBox="0 0 %s %s">%s</svg>' % (width,height,width,height,''.join(shapes)), encoding='utf-8')
    validate_svg(path)


def validate_spec(spec):
    if not isinstance(spec, dict) or spec.get('kind') not in ('document', 'spreadsheet', 'presentation', 'image', 'audio'):
        raise FormatError('content spec needs kind document, spreadsheet, presentation, image or audio')
    fields = {'document': {'title','paragraphs'}, 'spreadsheet': {'sheets','formulas_evaluated'},
              'presentation': {'slides'}, 'image': {'width','height','background','shapes'},
              'audio': {'duration_seconds','sample_rate','frequency_hz','amplitude'}}
    allowed = fields[spec['kind']] | {'kind','warnings'}
    if set(spec) - allowed: raise FormatError('unsupported model features: ' + ', '.join(sorted(set(spec)-allowed)))
    def strings(values):
        if not isinstance(values,list) or not all(isinstance(v,str) for v in values): raise FormatError('paragraphs must be a list of strings')
    if spec['kind']=='document':
        strings(spec.get('paragraphs',[]))
        if not isinstance(spec.get('title',''),str): raise FormatError('title must be a string')
    if spec['kind']=='presentation':
        slides=spec.get('slides',[])
        if not isinstance(slides,list) or len(slides)>1000: raise FormatError('presentation exceeds 1000-slide bound')
        for slide in slides:
            if not isinstance(slide,dict) or set(slide)-{'title','paragraphs'}: raise FormatError('unsupported slide features')
            strings(slide.get('paragraphs',[]))
    if spec['kind']=='spreadsheet':
        sheets=spec.get('sheets',[])
        if not isinstance(sheets,list) or len(sheets)>1000: raise FormatError('spreadsheet exceeds 1000-sheet bound')
        for sheet in sheets:
            if not isinstance(sheet,dict) or set(sheet)-{'name','rows','cells'}: raise FormatError('unsupported sheet features')
            if 'rows' in sheet and 'cells' in sheet: raise FormatError('choose rows or cells per sheet')
            values=[c.get('value','') for c in sheet.get('cells',[])] if 'cells' in sheet else [v for row in sheet.get('rows',[]) for v in row]
            if len(values)>100000: raise FormatError('sheet exceeds 100,000-cell bound')
            if any(not isinstance(v,(str,int,float,bool)) or (isinstance(v,float) and not math.isfinite(v)) for v in values): raise FormatError('cell values must be finite scalar values')
    if spec['kind']=='image':
        shapes=spec.get('shapes',[])
        if not isinstance(shapes,list) or len(shapes)>10000: raise FormatError('image exceeds 10,000-shape bound')
    if spec['kind']=='audio' and 'duration_seconds' not in spec:
        raise FormatError('audio creation needs a tone/silence spec, not extracted metadata')


def write_spec(spec, path):
    validate_spec(spec)
    extension = ext(path); kind = spec['kind']
    expected = 'spreadsheet' if extension in SHEET or extension in ('csv','tsv') else 'presentation' if extension in SLIDE else 'image' if is_image(extension) else 'audio' if extension in AUDIO else None
    if expected and expected != kind: raise FormatError('output format requires kind ' + expected)
    if extension in LEGACY:
        with tempfile.TemporaryDirectory() as d:
            modern = Path(d) / ('source.' + LEGACY[extension])
            write_spec(spec, modern)
            converted = office_convert(modern, extension, d)
            shutil.copyfile(converted, path)
        return
    if kind in ('image', 'audio') and not (is_image(extension) or extension in AUDIO or extension=='json'):
        raise FormatError('media content cannot be reconstructed as a text document')
    if extension in ('docx','xlsx','pptx'): return office_write(spec,path)
    if extension in ('odt','ods','odp'): return odf_write(spec,path)
    if extension == 'pdf': return pdf_write(spec,path)
    if extension == 'epub':
        body = ''.join('<p>%s</p>' % escaped(s) for s in document_lines(spec))
        with zipfile.ZipFile(path, 'w') as z:
            z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
            z.writestr('META-INF/container.xml','<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="book.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
            z.writestr('book.opf','<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book-id">local-generated</dc:identifier><dc:title>%s</dc:title><dc:language>en</dc:language><meta property="dcterms:modified">2000-01-01T00:00:00Z</meta></metadata><manifest><item id="content" href="content.xhtml" media-type="application/xhtml+xml"/><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/></manifest><spine><itemref idref="content"/></spine></package>' % escaped(spec.get('title','Untitled')))
            z.writestr('content.xhtml','<html xmlns="http://www.w3.org/1999/xhtml"><head><title>%s</title></head><body>%s</body></html>' % (escaped(spec.get('title','Untitled')),body))
            z.writestr('nav.xhtml','<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title>Contents</title></head><body><nav epub:type="toc"><ol><li><a href="content.xhtml">Contents</a></li></ol></nav></body></html>')
        return
    if is_image(extension):
        if extension == 'svg': return svg_write(spec,path)
        with tempfile.TemporaryDirectory() as d:
            svg = Path(d)/'scene.svg';svg_write(spec,svg);run([require('magick'),svg,path]);return
    if extension in AUDIO:
        duration = float(spec.get('duration_seconds',1)); rate = int(spec.get('sample_rate',16000)); frequency = float(spec.get('frequency_hz',440)); amplitude = float(spec.get('amplitude',0.2))
        if not 0 < duration <= 60 or not 8000 <= rate <= 96000 or not 0 <= frequency < rate/2 or not 0 <= amplitude <= 1: raise FormatError('audio bounds: duration 0..60, sample rate 8000..96000, amplitude 0..1, frequency below Nyquist')
        def tone(wav):
            with wave.open(str(wav),'wb') as f:
                f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate)
                f.writeframes(b''.join(struct.pack('<h',round(32767*amplitude*math.sin(2*math.pi*frequency*i/rate))) for i in range(int(duration*rate))))
        if extension == 'wav': return tone(path)
        with tempfile.TemporaryDirectory() as d:
            wav=Path(d)/'tone.wav';tone(wav);run([require('ffmpeg'),'-v','error','-nostdin','-i',wav,'-y',path]);return
    if extension in ('csv','tsv'):
        sheets=spec.get('sheets',[])
        if len(sheets)!=1: raise FormatError('CSV/TSV creation requires exactly one sheet')
        with path.open('w',encoding='utf-8',newline='') as f: csv.writer(f,delimiter='\t' if extension=='tsv' else ',').writerows(sheet_rows(sheets[0]))
        return
    if extension == 'json': path.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return
    lines=document_lines(spec)
    if not all(isinstance(s,str) for s in lines): raise FormatError('paragraphs must be strings')
    if extension in ('html','htm'): text='<!doctype html><html><head><meta charset="utf-8"><title>%s</title></head><body>%s</body></html>' % (escaped(spec.get('title','')), ''.join('<p>%s</p>'%escaped(s) for s in lines))
    elif extension=='xml': text='<document>'+''.join('<paragraph>%s</paragraph>'%escaped(s) for s in lines)+'</document>'
    elif extension=='rtf':
        def rtf(s):
            result=[]
            for c in s:
                if ord(c)>127:
                    units=struct.unpack('<'+'H'*(len(c.encode('utf-16-le'))//2),c.encode('utf-16-le'))
                    result.extend('\\u%s?'%(u if u<32768 else u-65536) for u in units)
                else:result.append('\\'+c if c in '\\{}' else c)
            return ''.join(result)
        text='{\\rtf1\\ansi '+ '\\par\n'.join(rtf(s) for s in lines)+'}'
    elif extension in ('txt','md','markdown','rst','tex','adoc'): text='\n'.join(lines)+'\n'
    else: raise FormatError('unsupported creation format: '+extension)
    path.write_text(text,encoding='utf-8')


@functools.lru_cache(maxsize=1)
def image_formats():
    if not shutil.which('magick'): return {}
    result={}
    for line in run(['magick','-list','format']).splitlines():
        match=re.match(r'^\s*(\w+)\*?\s+\S+\s+([r-])([w-])([+-])',line)
        if match: result[match.group(1).lower()]={'read':match.group(2)=='r','write':match.group(3)=='w'}
    return result


def is_image(extension):
    if extension in TEXT | DOC | SHEET | SLIDE | AUDIO | set(LEGACY): return False
    return extension in IMAGES or extension in image_formats()


def office_convert(src, extension, directory):
    require('soffice')
    directory=Path(directory)
    run(['soffice','-env:UserInstallation='+(directory/'profile').as_uri(),'--headless','--convert-to',extension,'--outdir',directory,src])
    made=directory/(Path(src).stem+'.'+extension)
    if not made.is_file(): raise FormatError('office backend produced no target')
    return made


def capabilities():
    codecs=image_formats()
    return {'native':{'documents':['txt','md','html','json','xml','rtf','rst','tex','adoc','docx','odt','epub'],'spreadsheets':['csv','tsv','xlsx','ods'],'presentations':['pptx','odp'],'images':['svg'],'audio':['wav'],'pdf_creation':'plain Windows-1252 text'},
            'backends':{x:bool(shutil.which(x)) for x in ['magick','ffmpeg','ffprobe','pdftotext','pdftoppm','tesseract','pandoc','soffice']},
            'image_codecs':codecs,'image_requested_formats':sorted(IMAGES),'audio_requested_formats':sorted(AUDIO),
            'notes':['Codec discovery is not a successful conversion receipt; delegates/policies can still reject a specific file.','Audio formats depend on the installed ffmpeg build; use capabilities --details for encoder/muxer listings.','Recreation preserves only the normalized model, not exact original layout, macros, signatures, tracked changes or cached formula values.']}


def convert(src, dest, lossy=False, backend='native'):
    a,b=ext(src),ext(dest)
    if backend=='office':
        if a not in DOC | SHEET | SLIDE | set(LEGACY) or b not in DOC | SHEET | SLIDE | set(LEGACY):
            raise FormatError('office conversion needs office/document input and output formats')
        if not lossy: raise FormatError('office conversion can change layout/features; pass --allow-lossy')
        with tempfile.TemporaryDirectory() as d:
            made=office_convert(src,b,d);shutil.copyfile(made,dest)
        return
    if is_image(a) and is_image(b):
        if a=='svg': validate_svg(src)
        if a==b: raise FormatError('same-format rewriting needs an explicit transform, not conversion')
        if not lossy: raise FormatError('image conversion can lose frames, metadata, color or alpha; pass --allow-lossy after reviewing the target')
        run([require('magick'),src,dest]);return
    if a in AUDIO and b in AUDIO:
        if not lossy: raise FormatError('audio transcoding may change metadata or samples; pass --allow-lossy')
        run([require('ffmpeg'),'-v','error','-nostdin','-i',src,'-y',dest]);return
    # Explicit content-model conversion. Never imply native fidelity.
    if not lossy: raise FormatError('content conversion can lose layout/features; pass --allow-lossy or extract and review the spec first')
    if b in ('doc','xls','ppt','odt','ods','odp','docx','xlsx','pptx','pdf') and a in ('doc','xls','ppt'):
        with tempfile.TemporaryDirectory() as d:
            made=office_convert(src,b,d)
            shutil.copyfile(made,dest);return
    spec=extract(src)
    if a=='json' and not isinstance(spec,dict): raise FormatError('JSON content is not a content spec')
    write_spec(spec,dest)


def frame_inventory(path):
    lines=run([require('magick'),'identify','-ping','-format','%w %h %T\n',path]).splitlines()
    rows=[]
    for line in lines:
        if not re.fullmatch(r'[1-9]\d* [1-9]\d* \d+',line):
            raise FormatError('image backend returned an invalid frame inventory')
        width,height,delay=(int(value) for value in line.split())
        rows.append({'width':width,'height':height,'delay_centiseconds':delay})
    if not rows:raise FormatError('image backend reported no decoded frames')
    return rows


def animate(frames,path,fps):
    if ext(path)!='gif' or not 1<=fps<=60 or not 1<=len(frames)<=300: raise FormatError('animation requires GIF, 1..300 frames and FPS 1..60')
    frames=[source(f) for f in frames]
    if any(not is_image(ext(f)) for f in frames): raise FormatError('animation frames must be supported images')
    dimensions=None
    for p in frames:
        if ext(p)=='svg': validate_svg(p)
        inventory=frame_inventory(p)
        if len(inventory)!=1:raise FormatError('animation inputs must each decode to a single-frame image')
        size=(inventory[0]['width'],inventory[0]['height'])
        if dimensions is None:dimensions=size
        elif size!=dimensions:raise FormatError('animation inputs must have equal frame dimensions')
    run([require('magick'),'-delay',str(round(100/fps)),'-loop','0']+frames+[path])
    actual=frame_inventory(path)
    if len(actual)!=len(frames):raise FormatError('GIF output frame count differs from the input list')
    if any((frame['width'],frame['height'])!=dimensions for frame in actual):
        raise FormatError('GIF output frame dimensions differ from the input images')
    delays=[frame['delay_centiseconds'] for frame in actual]
    if any(delay<=0 for delay in delays):raise FormatError('GIF output has zero frame delay; actual playback rate is not established')
    duration=sum(delays)/100
    return {'frames':len(actual),'width':dimensions[0],'height':dimensions[1],
            'fps_requested':fps,'delays_centiseconds':delays,
            'duration_seconds':duration,'fps_effective':len(actual)/duration,
            'timing':'GIF delays decoded from the generated file; playback software may impose its own minimum delay'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    cap=sub.add_parser('capabilities');cap.add_argument('--details',action='store_true')
    for command in ['inspect','extract']:
        sp=sub.add_parser(command);sp.add_argument('input');sp.add_argument('--output');sp.add_argument('--ocr',action='store_true');sp.add_argument('--overwrite',action='store_true')
    for command in ['create','convert']:
        sp=sub.add_parser(command);sp.add_argument('input');sp.add_argument('--output',required=True);sp.add_argument('--overwrite',action='store_true');sp.add_argument('--allow-lossy',action='store_true');sp.add_argument('--backend',choices=['native','office'],default='native')
    ani=sub.add_parser('animate');ani.add_argument('frames',nargs='+');ani.add_argument('--output',required=True);ani.add_argument('--fps',type=int,default=12);ani.add_argument('--overwrite',action='store_true')
    args=p.parse_args(argv)
    try:
        if args.command=='capabilities':
            data=capabilities()
            if args.details and shutil.which('ffmpeg'):
                data['ffmpeg_encoders']=run(['ffmpeg','-hide_banner','-encoders']);data['ffmpeg_muxers']=run(['ffmpeg','-hide_banner','-muxers'])
        elif args.command in ('inspect','extract'):
            src=source(args.input);data=extract(src,args.ocr)
            if args.command=='inspect': data={'extension':ext(src),'size_bytes':src.stat().st_size,'content':data}
            if args.output: output(args.output,lambda q:q.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'),args.overwrite)
        elif args.command=='create':
            src=source(args.input);spec=json.loads(src.read_text(encoding='utf-8'))
            if src.resolve()==Path(args.output).expanduser().resolve():raise FormatError('input and output must differ')
            def create_target(q):
                if args.backend=='native': return write_spec(spec,q)
                if spec.get('kind') not in ('document','spreadsheet','presentation'): raise FormatError('office creation requires a document, spreadsheet or presentation spec')
                intermediate={'document':'docx','spreadsheet':'xlsx','presentation':'pptx'}[spec['kind']]
                with tempfile.TemporaryDirectory() as d:
                    original=Path(d)/('source.'+intermediate);write_spec(spec,original)
                    made=office_convert(original,ext(q),d);shutil.copyfile(made,q)
            target=output(args.output,create_target,args.overwrite);data={'output':str(target),'format':ext(target),'recreated_features':'normalized content only'}
        elif args.command=='convert':
            src=source(args.input)
            if src.resolve()==Path(args.output).expanduser().resolve():raise FormatError('input and output must differ')
            target=output(args.output,lambda q:convert(src,q,args.allow_lossy,args.backend),args.overwrite);data={'output':str(target),'format':ext(target),'fidelity':'content/codec conversion; inspect target'}
        else:
            receipt={}
            def build_animation(q):receipt.update(animate(args.frames,q,args.fps))
            target=output(args.output,build_animation,args.overwrite);data={'output':str(target),**receipt}
        print(json.dumps(data,ensure_ascii=False,indent=2));return 0
    except (FormatError,ValueError,OSError,TypeError,IndexError,KeyError,StopIteration,EOFError,wave.Error,ET.ParseError) as error:
        print(json.dumps({'error':str(error)}),file=sys.stderr);return 2


if __name__=='__main__':sys.exit(main())
