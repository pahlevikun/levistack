#!/usr/bin/env python3
"""Create reproducible art sources; delegate format rendering to file-toolkit."""
import argparse
import json
import random
import re
import subprocess
import sys
from pathlib import Path


def geometry(args):
    if not 16 <= args.width <= 4096 or not 16 <= args.height <= 4096:
        raise ValueError('dimensions must be 16..4096')
    if not 1 <= args.count <= 2000:
        raise ValueError('count must be 1..2000')
    palette = args.palette.split(',')
    if not 1 <= len(palette) <= 12 or any(not re.fullmatch(r'#[0-9a-fA-F]{6}', color) for color in palette):
        raise ValueError('palette must contain 1..12 comma-separated six-digit hex colors')
    return palette


def scene(args):
    colors = geometry(args)
    generator = random.Random(args.seed)
    shapes = []
    for _ in range(args.count):
        radius = generator.uniform(2, min(args.width, args.height) / 12)
        shapes.append({'type': 'circle', 'cx': round(generator.uniform(radius, args.width-radius), 3), 'cy': round(generator.uniform(radius, args.height-radius), 3), 'r': round(radius, 3), 'fill': generator.choice(colors)})
    return {'kind': 'image', 'width': args.width, 'height': args.height, 'background': colors[-1], 'shapes': shapes}


def interactive(args):
    colors = geometry(args)
    state = json.dumps({'seed': args.seed, 'count': args.count, 'width': args.width, 'height': args.height, 'palette': colors})
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Generative canvas</title>
<style>body{font:17px system-ui;max-width:65rem;margin:2rem auto;padding:1rem}canvas{max-width:100%;height:auto}label{display:block;margin:.6rem 0}button,input{font:inherit}</style>
<h1>Generative canvas</h1><p>Change the seed or count; the same settings rebuild the same canvas.</p><label>Seed <input id="seed" type="number" step="1"></label><label>Count <input id="count" type="range" min="1" max="2000"></label><button id="save">Download PNG</button><canvas id="art" role="img" aria-label="Seeded field of colored circles"></canvas><pre id="settings"></pre>
<script>const state=__STATE__;const canvas=document.getElementById('art'),ctx=canvas.getContext('2d');canvas.width=state.width;canvas.height=state.height;
const seed=document.getElementById('seed'),count=document.getElementById('count');seed.value=state.seed;count.value=state.count;
function draw(){let n=(Number(seed.value)||0)>>>0;const random=()=>{n=(Math.imul(n,1664525)+1013904223)>>>0;return n/4294967296};const total=Math.max(1,Math.min(2000,Number(count.value)||1));ctx.fillStyle=state.palette[state.palette.length-1];ctx.fillRect(0,0,canvas.width,canvas.height);for(let i=0;i<total;i++){const r=2+random()*(Math.min(canvas.width,canvas.height)/12-2),x=r+random()*(canvas.width-2*r),y=r+random()*(canvas.height-2*r);ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fillStyle=state.palette[Math.floor(random()*state.palette.length)];ctx.fill()}document.getElementById('settings').textContent=JSON.stringify({...state,seed:Number(seed.value)||0,count:total,algorithm:'lcg-circles-v1'},null,2)}
seed.addEventListener('input',draw);count.addEventListener('input',draw);document.getElementById('save').addEventListener('click',()=>{const a=document.createElement('a');a.download='canvas.png';a.href=canvas.toDataURL('image/png');a.click()});draw();</script></html>'''.replace('__STATE__', state)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ['scene', 'explore']:
        item = sub.add_parser(command)
        item.add_argument('--seed', type=int, default=42)
        item.add_argument('--count', type=int, default=80)
        item.add_argument('--width', type=int, default=640)
        item.add_argument('--height', type=int, default=480)
        item.add_argument('--palette', default='#17324d,#f6ae2d,#f3f0e8')
        item.add_argument('--output', required=True, type=Path)
        item.add_argument('--overwrite', action='store_true')
    for command in ['render', 'gif']:
        item = sub.add_parser(command)
        item.add_argument('inputs', nargs='+' if command == 'gif' else 1)
        item.add_argument('--toolkit', required=True, type=Path)
        item.add_argument('--output', required=True, type=Path)
        item.add_argument('--overwrite', action='store_true')
        if command == 'gif': item.add_argument('--fps', type=int, default=8)
    args = parser.parse_args()
    try:
        if args.output.is_symlink(): raise ValueError('output must not be a symlink')
        if args.command in ['scene', 'explore']:
            content = json.dumps(scene(args), indent=2)+'\n' if args.command == 'scene' else interactive(args)
            with args.output.open('w' if args.overwrite else 'x', encoding='utf-8') as target: target.write(content)
        else:
            if not args.toolkit.is_file(): raise ValueError('resolve the actual file-toolkit scripts/files.py first')
            command = [sys.executable, str(args.toolkit), 'create' if args.command == 'render' else 'animate'] + args.inputs + ['--output', str(args.output)]
            if args.command == 'gif': command += ['--fps', str(args.fps)]
            if args.overwrite: command.append('--overwrite')
            result = subprocess.run(command, timeout=120)
            if result.returncode: return result.returncode
        print(json.dumps({'output': str(args.output), 'mode': args.command}))
        return 0
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        parser.exit(2, 'error: {}\n'.format(error))


if __name__ == '__main__':
    sys.exit(main())
