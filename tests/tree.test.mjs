import assert from 'node:assert/strict';
import { cpSync, mkdtempSync, rmSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { diffClaudeCursorLinks, diffGenerated, writeGenerated } from '../scripts/sync.mjs';
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
    writeFileSync(join(dir, 'skills/focus/parking-lot/SKILL.md'), '---\nname: wrong\ndescription: ok.\n---\nbody\n');
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
    const skill = join(dir, 'skills/focus/parking-lot/SKILL.md');
    writeFileSync(skill, '---\nname: parking-lot\ndescription: ok.\n---\nsee /Users/someone/x, ' + 'go' + 'jek and teamharness\n');
    const soft = validateTree(dir);
    assert.deepEqual([...soft], [], 'soft hits are warnings by default');
    assert.equal(soft.warnings.filter((w) => w.includes('focus/parking-lot')).length, 3);
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
    writeFileSync(join(dir, 'skills/focus/parking-lot/SKILL.md'), '---\nname: parking-lot\ndescription: Use when stuck: do x.\n---\nbody\n');
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
    writeFileSync(join(dir, 'skills/focus/parking-lot/SKILL.md'), '---\nname: parking-lot\ndescription: ok.\n---\napi_key = "abcd1234abcd1234abcd1234"\n');
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
