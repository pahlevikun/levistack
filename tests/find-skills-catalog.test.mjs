import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { collect, rank, readSkill } from '../skills/workflow/find-skills/scripts/catalog.mjs';

function tree(files) {
  const root = mkdtempSync(join(tmpdir(), 'find-skills-'));
  for (const [rel, content] of Object.entries(files)) {
    const p = join(root, rel);
    mkdirSync(dirname(p), { recursive: true });
    writeFileSync(p, content);
  }
  return root;
}
const skill = (name, description) => `---\nname: ${name}\ndescription: "${description}"\n---\n\n# ${name}\n`;

test('collect reads grouped and flat roots, and skips skills nested inside a skill', () => {
  const root = tree({
    'catalog/writing/copy/SKILL.md': skill('copy', 'Write prose. Use when writing.'),
    'catalog/writing/copy/inner/SKILL.md': skill('inner', 'Nested helper.'),
    'flat/review/SKILL.md': skill('review', 'Review a diff. Use when reviewing.'),
  });
  try {
    const names = collect([join(root, 'catalog'), join(root, 'flat')]).map((s) => s.name);
    assert.deepEqual(names, ['copy', 'review']);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('collect dedupes by name (first root wins) and by symlink target', () => {
  const root = tree({
    'a/same/SKILL.md': skill('same', 'First copy.'),
    'b/same/SKILL.md': skill('same', 'Second copy.'),
    'c/other/SKILL.md': skill('other', 'Other skill.'),
  });
  symlinkSync(join(root, 'c'), join(root, 'c-link'));
  try {
    const found = collect([join(root, 'a'), join(root, 'b'), join(root, 'c'), join(root, 'c-link')]);
    assert.deepEqual(found.map((s) => [s.name, s.description]), [['same', 'First copy.'], ['other', 'Other skill.']]);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('readSkill handles quoted, plain and folded descriptions', () => {
  const root = tree({
    'q/SKILL.md': '---\nname: q\ndescription: "Quoted one."\n---\n',
    'p/SKILL.md': '---\nname: p\ndescription: Plain one.\n---\n',
    'f/SKILL.md': '---\nname: f\ndescription: >\n  Folded\n  one.\n---\n',
    'n/SKILL.md': '# no frontmatter\n',
  });
  try {
    assert.equal(readSkill(join(root, 'q/SKILL.md')).description, 'Quoted one.');
    assert.equal(readSkill(join(root, 'p/SKILL.md')).description, 'Plain one.');
    assert.equal(readSkill(join(root, 'f/SKILL.md')).description, 'Folded one.');
    assert.equal(readSkill(join(root, 'n/SKILL.md')), null);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('rank prefers name hits over description hits and drops non-matches', () => {
  const skills = [
    { name: 'plain-writing', description: 'Edit text.' },
    { name: 'polyglot-copywriter', description: 'Rewrite and humanize emails.' },
    { name: 'elixir-tdd', description: 'Test first in Elixir.' },
  ];
  assert.deepEqual(rank(skills, 'rewrite emails').map((s) => s.name), ['polyglot-copywriter']);
  assert.deepEqual(rank(skills, 'plain').map((s) => s.name), ['plain-writing']);
  assert.deepEqual(rank(skills, 'humanize writing').map((s) => s.name), ['polyglot-copywriter', 'plain-writing']);
  assert.deepEqual(rank(skills, 'kubernetes'), []);
});

test('loaded roots mark skills invokable; a symlink into a loaded root upgrades a file-only skill', () => {
  const root = tree({
    'catalog/g/solo/SKILL.md': skill('solo', 'Only in the catalog.'),
    'catalog/g/both/SKILL.md': skill('both', 'In catalog and linked.'),
    'host/registered/SKILL.md': skill('registered', 'Host skill.'),
  });
  symlinkSync(join(root, 'catalog/g/both'), join(root, 'host/both'));
  try {
    const found = collect([{ dir: join(root, 'catalog'), loaded: false }, { dir: join(root, 'host'), loaded: true }]);
    const by = Object.fromEntries(found.map((s) => [s.name, s]));
    assert.equal(by.solo.loaded, false);
    assert.match(by.solo.invoke, /^read .*SKILL\.md and follow it$/);
    assert.equal(by.both.loaded, true);
    assert.equal(by.registered.invoke, 'Skill tool: registered');
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('plain string roots are file-only', () => {
  const root = tree({ 'r/a/SKILL.md': skill('a', 'A skill.') });
  try {
    assert.equal(collect([join(root, 'r')])[0].loaded, false);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('rank with only filler words returns every skill unscored', () => {
  const skills = [{ name: 'a', description: 'x' }, { name: 'b', description: 'y' }];
  assert.equal(rank(skills, 'I want to').length, 2);
});
