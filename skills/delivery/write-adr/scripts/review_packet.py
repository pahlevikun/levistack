#!/usr/bin/env python3
"""Create an offline section-feedback page without starting a server."""
import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path


PAGE = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Proposal review</title><style>body{max-width:62rem;margin:2rem auto;padding:1rem;font:17px system-ui;line-height:1.5}article{border:1px solid #999;padding:1rem;margin:1rem 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}textarea{box-sizing:border-box;width:100%;min-height:6rem}select,input,button{font:inherit;padding:.4rem}label{display:block;margin:.5rem 0}</style>
<h1>Proposal review</h1><p>Review each section. Download feedback when finished. Nothing is sent over the network or written into the original proposal.</p>
<label>Reviewer <input id="reviewer" maxlength="200"></label>__SECTIONS__
<button id="download">Download feedback</button><p id="notice" role="status"></p>
<script id="context" type="application/json">__CONTEXT__</script>
<script>const context=JSON.parse(document.getElementById('context').textContent);
document.getElementById('download').addEventListener('click',()=>{
const sections=Array.from(document.querySelectorAll('article')).map((e,i)=>({id:context.sections[i].id,heading:context.sections[i].heading,decision:e.querySelector('select').value,comment:e.querySelector('textarea').value}));
const packet={schema:1,source_sha256:context.source_sha256,reviewer:document.getElementById('reviewer').value,reviewed_at:new Date().toISOString(),sections};
const url=URL.createObjectURL(new Blob([JSON.stringify(packet,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='proposal-feedback.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
document.getElementById('notice').textContent='Feedback downloaded. Compare its source hash before applying comments.';
});</script></html>'''


def sections(text):
    result = []
    heading = 'Introduction'
    lines = []
    fence = None
    saw_heading = False
    for line in text.splitlines():
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence is not None:
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + r'{' + str(fence[1]) + r',}\s*', line):
                fence = None
            lines.append(line)
            continue
        if marker:
            token = marker.group(1)
            fence = (token[0], len(token))
            lines.append(line)
            continue
        match = re.match(r'^#{1,6}\s+(.+?)\s*#*$', line)
        if match:
            if lines or saw_heading:
                result.append((heading, '\n'.join(lines)))
            heading = match.group(1); lines = []; saw_heading = True
        else:
            lines.append(line)
    if lines or saw_heading or not result:
        result.append((heading, '\n'.join(lines)))
    return result


def build(source):
    raw = source.read_bytes()
    if len(raw) > 2_000_000:
        raise ValueError('proposal exceeds the 2 MB input bound')
    parts = sections(raw.decode('utf-8'))
    context = {'source_sha256': hashlib.sha256(raw).hexdigest(), 'sections': []}
    cards = []
    for index, (heading, content) in enumerate(parts):
        context['sections'].append({'id': index + 1, 'heading': heading})
        cards.append('<article><h2>{}</h2><pre>{}</pre><label>Assessment <select><option value="unreviewed">Unreviewed</option><option value="agree">Agree</option><option value="revise">Needs revision</option><option value="question">Question</option></select></label><label>Feedback<textarea maxlength="20000"></textarea></label></article>'.format(html.escape(heading), html.escape(content)))
    encoded = json.dumps(context).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    return re.sub(r'__SECTIONS__|__CONTEXT__', lambda match: ''.join(cards) if match.group() == '__SECTIONS__' else encoded, PAGE)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        if args.input.resolve() == args.output.resolve() or (args.output.exists() and args.input.samefile(args.output)):
            raise ValueError('output must differ from input')
        if args.output.is_symlink():
            raise ValueError('output must not be a symlink')
        page = build(args.input)
        with args.output.open('w' if args.overwrite else 'x', encoding='utf-8') as target:
            target.write(page)
        print(json.dumps({'output': str(args.output), 'source_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest()}))
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(2, 'error: {}\n'.format(error))


if __name__ == '__main__':
    main()
