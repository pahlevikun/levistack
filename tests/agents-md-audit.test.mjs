import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { audit, CODEX_LIMIT } from '../skills/agent-authoring/create-agents-md/scripts/audit.mjs';

const repo = join(dirname(fileURLToPath(import.meta.url)), '..');
const codes = (r) => r.findings.map((f) => f.code);

function fixture(files) {
  const root = mkdtempSync(join(tmpdir(), 'agents-md-'));
  for (const [rel, content] of Object.entries(files)) {
    const p = join(root, rel);
    mkdirSync(dirname(p), { recursive: true });
    if (content && typeof content === 'object') symlinkSync(content.link, p);
    else writeFileSync(p, content);
  }
  return root;
}

test('clean root file has no findings', () => {
  const root = fixture({ 'AGENTS.md': '# App\n\n- Test: `npm test`\n', 'src/index.js': '' });
  try {
    assert.deepEqual(audit(root).findings, []);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('flags a CLAUDE.md that hides AGENTS.md, but not a symlink or an @import', () => {
  const hidden = fixture({ 'AGENTS.md': '# a\n', 'CLAUDE.md': '# separate\n' });
  const linked = fixture({ 'AGENTS.md': '# a\n' });
  const imported = fixture({ 'AGENTS.md': '# a\n', 'CLAUDE.md': '@AGENTS.md\n\n- Claude only\n' });
  try {
    symlinkSync(join(linked, 'AGENTS.md'), join(linked, 'CLAUDE.md'));
    assert.ok(codes(audit(hidden)).includes('claude-hides'));
    assert.ok(!codes(audit(linked)).includes('claude-hides'));
    assert.ok(!codes(audit(imported)).includes('claude-hides'));
  } finally {
    for (const r of [hidden, linked, imported]) rmSync(r, { recursive: true, force: true });
  }
});

test('flags CLAUDE.local.md that would hide AGENTS.md', () => {
  const root = fixture({ 'AGENTS.md': '# a\n', 'CLAUDE.local.md': '- mine\n' });
  try {
    assert.ok(codes(audit(root)).includes('local-hides'));
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('flags long, empty, secret-like files and missing paths', () => {
  const root = fixture({
    'AGENTS.md': `${'line\n'.repeat(250)}See \`docs/missing.md\` and \`src/real.js\`. token = "abcd1234abcd1234abcd1234"\n`,
    'src/real.js': '',
    'pkg/AGENTS.md': '   \n',
  });
  try {
    const c = codes(audit(root));
    for (const code of ['too-long', 'secret-like', 'missing-path', 'empty']) assert.ok(c.includes(code), code);
    const missing = audit(root).findings.filter((f) => f.code === 'missing-path');
    assert.equal(missing.length, 1);
    assert.match(missing[0].message, /docs\/missing\.md/);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('ignores paths inside fenced blocks and glob-like tokens', () => {
  const root = fixture({ 'AGENTS.md': '```\nnode ghost/file.js\n```\nUse `src/**/*.ts` and `$HOME/x.md`.\n' });
  try {
    assert.ok(!codes(audit(root)).includes('missing-path'));
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('counts the root-to-leaf chain against the Codex budget and honors override files', () => {
  const big = 'x'.repeat(CODEX_LIMIT / 2 + 10);
  const root = fixture({ 'AGENTS.md': big, 'a/AGENTS.md': big, 'a/AGENTS.override.md': 'tiny\n', 'b/AGENTS.md': big });
  try {
    const r = audit(root);
    const flagged = r.findings.filter((f) => f.code === 'chain-too-large').map((f) => f.file);
    assert.deepEqual(flagged, ['b/AGENTS.md']);
    assert.ok(codes(r).includes('override'));
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('skips node_modules and .git', () => {
  const root = fixture({ 'node_modules/x/AGENTS.md': '# dep\n', '.git/AGENTS.md': '# g\n', 'AGENTS.md': '# a\n' });
  try {
    assert.deepEqual(audit(root).files.map((f) => f.path), ['AGENTS.md']);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('this repository has no blocking instruction-file findings', () => {
  const blocking = audit(repo).findings.filter((f) => ['claude-hides', 'local-hides', 'chain-too-large', 'secret-like', 'empty'].includes(f.code));
  assert.deepEqual(blocking, []);
});
