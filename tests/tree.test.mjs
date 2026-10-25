import assert from 'node:assert/strict';
import { cpSync, mkdtempSync, rmSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { build, diffClaudeCursorLinks, diffGenerated, writeGenerated } from '../scripts/sync.mjs';
import { validateTree } from '../scripts/validate.mjs';

const repo = join(dirname(fileURLToPath(import.meta.url)), '..');

function fixture() {
  const dir = mkdtempSync(join(tmpdir(), 'levistack-'));
  cpSync(join(repo, 'package.json'), join(dir, 'package.json'));
  cpSync(join(repo, 'README.md'), join(dir, 'README.md'));
  cpSync(join(repo, 'skills'), join(dir, 'skills'), { recursive: true });
  cpSync(join(repo, 'rules'), join(dir, 'rules'), { recursive: true });
  return dir;
}

test('sync is idempotent: second run produces no drift', () => {
  const dir = fixture();
  try {
    writeGenerated(dir);
    assert.deepEqual(diffGenerated(dir), []);
    writeGenerated(dir);
    assert.deepEqual(diffGenerated(dir), []);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('validator rejects a skill whose name does not match its folder', () => {
  const dir = fixture();
  try {
    writeGenerated(dir);
    writeFileSync(join(dir, 'skills/focus/later-list/SKILL.md'), '---\nname: wrong\ndescription: ok.\n---\nbody\n');
    const errors = validateTree(dir);
    assert.ok(errors.some((e) => e.includes('must equal folder name')), errors.join('\n'));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('validator rejects employer references and local paths', () => {
  const dir = fixture();
  try {
    writeGenerated(dir);
    const skill = join(dir, 'skills/focus/later-list/SKILL.md');
    writeFileSync(skill, '---\nname: later-list\ndescription: ok.\n---\nsee /Users/someone/x, ' + 'go' + 'jek and teamharness\n');
    const soft = validateTree(dir);
    assert.deepEqual([...soft], [], 'soft hits are warnings by default');
    assert.equal(soft.warnings.filter((w) => w.includes('focus/later-list')).length, 3);
    const strict = validateTree(dir, { strict: true });
    assert.ok(strict.some((e) => e.includes('absolute local path')));
    assert.ok(strict.some((e) => e.includes('employer identifier')));
    assert.ok(strict.some((e) => e.includes('teamonia tooling')));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('validator flags a group without DESCRIPTION.md and stale generated files', () => {
  const dir = fixture();
  try {
    writeGenerated(dir);
    rmSync(join(dir, 'skills/focus/DESCRIPTION.md'));
    mkdirSync(join(dir, 'skills/empty-group'), { recursive: true });
    const errors = validateTree(dir);
    assert.ok(errors.some((e) => e.includes('missing DESCRIPTION.md')));
    assert.ok(errors.some((e) => e.includes('no skills')));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('validator rejects unquoted ": " in frontmatter (breaks strict YAML)', () => {
  const dir = fixture();
  try {
    writeGenerated(dir);
    writeFileSync(join(dir, 'skills/focus/later-list/SKILL.md'), '---\nname: later-list\ndescription: Use when stuck: do x.\n---\nbody\n');
    const errors = validateTree(dir);
    assert.ok(errors.some((e) => e.includes('must be quoted')), errors.join('\n'));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('validator always rejects a hard-coded secret, even without --strict', () => {
  const dir = fixture();
  try {
    writeGenerated(dir);
    writeFileSync(join(dir, 'skills/focus/later-list/SKILL.md'), '---\nname: later-list\ndescription: ok.\n---\napi_key = "abcd1234abcd1234abcd1234"\n');
    assert.ok(validateTree(dir).some((e) => e.includes('possible secret')));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('block-scalar descriptions parse as one string', async () => {
  const { parseFrontmatter } = await import('../scripts/lib/frontmatter.mjs');
  const { data } = parseFrontmatter('---\nname: x\ndescription: >-\n  line one\n  line two\n---\nbody');
  assert.equal(data.description, 'line one line two');
});

test('real repo has no errors (warnings allowed during import cleanup)', () => {
  assert.deepEqual([...validateTree(repo)], []);
});

test('real repo: .claude agents, rules and skills symlink .cursor', () => {
  assert.deepEqual(diffClaudeCursorLinks(repo), []);
});

test('upstream.json becomes github marketplace entries and root plugin dependencies', () => {
  const dir = fixture();
  try {
    writeFileSync(
      join(dir, 'upstream.json'),
      JSON.stringify({ plugins: [{ name: 'ext-skill', repo: 'someone/ext-skill', description: 'An external skill.' }] }),
    );
    const out = build(dir);
    const market = JSON.parse(out.get('.claude-plugin/marketplace.json'));
    const entry = market.plugins.find((p) => p.name === 'ext-skill');
    assert.deepEqual(entry.source, { source: 'github', repo: 'someone/ext-skill' });
    assert.equal(entry.category, 'upstream');
    assert.deepEqual(JSON.parse(out.get('.claude-plugin/plugin.json')).dependencies, ['ext-skill']);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('no upstream.json: root plugin has no dependencies', () => {
  const dir = fixture();
  try {
    assert.equal(JSON.parse(build(dir).get('.claude-plugin/plugin.json')).dependencies, undefined);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('root plugin.json for Antigravity has only name and description', () => {
  const dir = fixture();
  try {
    const manifest = JSON.parse(build(dir).get('plugin.json'));
    assert.deepEqual(Object.keys(manifest).sort(), ['description', 'name']);
    assert.match(manifest.name, /^[a-zA-Z0-9-_]+$/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('Cursor manifest lists every nested skill explicitly', () => {
  const dir = fixture();
  try {
    const out = build(dir);
    const cursor = JSON.parse(out.get('.cursor-plugin/plugin.json'));
    const claude = JSON.parse(out.get('.claude-plugin/plugin.json'));
    assert.ok(Array.isArray(cursor.skills));
    assert.deepEqual(cursor.skills, claude.skills);
    assert.equal(JSON.parse(out.get('.antigravity-plugin/plugin.json')).name, 'levistack');
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
