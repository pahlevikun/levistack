import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { TOOLS, check, defaultNotePath, probe, render } from '../skills/foundation/setup-levistack/scripts/check.mjs';

const script = fileURLToPath(new URL('../skills/foundation/setup-levistack/scripts/check.mjs', import.meta.url));
const ok = () => ({ status: 0, out: 'v1.0.0' });

test('every tool names who uses it and how to install it on both platforms', () => {
  for (const tool of TOOLS) {
    assert.ok(tool.usedBy, tool.name);
    assert.ok(tool.install.darwin && tool.install.linux, tool.name);
  }
  assert.deepEqual(TOOLS.filter((t) => t.required).map((t) => t.name), ['node', 'python3']);
});

test('a missing optional tool is a named gap with an install hint, and status stays ready', () => {
  const results = check({ find: (name) => (name === 'ffmpeg' ? null : `/bin/${name}`), exec: ok, nodeVersion: '22.1.0' });
  const note = render(results, { date: '2026-10-31', os: 'darwin' });
  assert.match(note, /Status: ready with 1 named gap/);
  assert.match(note, /- `ffmpeg`: brew install ffmpeg/);
  assert.match(note, /Nothing was installed/);
});

test('a missing required runtime blocks, and an old node counts as missing', () => {
  const node = probe(TOOLS[0], { find: (n) => `/bin/${n}`, exec: ok, nodeVersion: '18.19.0' });
  assert.equal(node.found, false);
  assert.match(node.detail, /needs 20\+/);
  const results = check({ find: (n) => (n === 'python3' ? null : `/bin/${n}`), exec: ok, nodeVersion: '22.0.0' });
  assert.match(render(results, { os: 'linux' }), /Status: blocked, python3 missing/);
  assert.equal(results.find((r) => r.name === 'playwright').detail, 'python3 missing');
});

test('the Python package probe uses the import result', () => {
  const playwright = TOOLS.find((t) => t.name === 'playwright');
  assert.equal(probe(playwright, { find: () => '/bin/python3', exec: () => ({ status: 1, out: '' }) }).found, false);
  assert.equal(probe(playwright, { find: () => '/bin/python3', exec: () => ({ status: 0, out: '1.48.0' }) }).detail, '1.48.0');
});

test('the CLI writes only with --write, to the path given', () => {
  const dir = mkdtempSync(join(tmpdir(), 'setup-levistack-'));
  try {
    const out = join(dir, 'nested', 'setup.md');
    const dry = spawnSync(process.execPath, [script, '--out', out], { encoding: 'utf8' });
    assert.match(dry.stdout, /# levistack setup/);
    assert.throws(() => readFileSync(out));
    spawnSync(process.execPath, [script, '--write', '--out', out], { encoding: 'utf8' });
    assert.match(readFileSync(out, 'utf8'), /\| `node` \| found \|/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('the default note lives under ~/.levistack', () => {
  assert.equal(defaultNotePath('/home/u'), join('/home/u', '.levistack', 'setup.md'));
});
