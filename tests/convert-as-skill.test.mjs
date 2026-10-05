import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { classify } from '../skills/agent-authoring/convert-as-skill/scripts/classify.mjs';
import { convertSource } from '../skills/agent-authoring/convert-as-skill/scripts/convert.mjs';
import { mergeSkills } from '../skills/agent-authoring/convert-as-skill/scripts/merge.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const scripts = join(root, 'skills/agent-authoring/convert-as-skill/scripts');

function kinds(result) {
  return result.jobs.map((j) => j.kind);
}

test('classify: example table', () => {
  assert.deepEqual(kinds(classify({ paths: ['.cursor/rules/api.mdc'] })), ['from-rule']);
  assert.deepEqual(kinds(classify({ paths: ['agents/reviewer.md'] })), ['from-agent']);
  const convo = classify({ text: 'save this conversation as a skill' });
  assert.equal(convo.status, 'ok');
  assert.deepEqual(kinds(convo), ['from-conversation']);
  assert.deepEqual(kinds(classify({ paths: ['book.pdf'] })), ['from-document']);
  assert.equal(classify({ text: 'convert this' }).status, 'ask');
  const scratch = classify({ text: 'write a skill from scratch' });
  assert.equal(scratch.status, 'reject');
  assert.equal(scratch.redirect, 'create-skill');
  const mixed = classify({ paths: ['rules/a.mdc', 'chapter.pdf'] });
  assert.equal(mixed.status, 'ok');
  assert.deepEqual(kinds(mixed), ['from-rule', 'from-document']);
});

test('classify: merge vs ask vs conversation', () => {
  const dir = mkdtempSync(join(tmpdir(), 'cas-merge-'));
  try {
    const foo = join(dir, 'foo');
    const bar = join(dir, 'bar');
    mkdirSync(foo);
    mkdirSync(bar);
    writeFileSync(join(foo, 'SKILL.md'), '---\nname: foo\ndescription: "Foo. Use when foo."\n---\n# Foo\n');
    writeFileSync(join(bar, 'SKILL.md'), '---\nname: bar\ndescription: "Bar. Use when bar."\n---\n# Bar\n');
    const merged = classify({ paths: [foo, bar], text: 'merge these into one skill' });
    assert.equal(merged.status, 'ok');
    assert.deepEqual(kinds(merged), ['merge-skills']);
    const askMerge = classify({ paths: [foo, bar] });
    assert.equal(askMerge.status, 'ask');
    assert.match(askMerge.question, /Merge these into one skill/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
  assert.equal(classify({ paths: ['book.pdf'], text: 'and this conversation' }).status, 'ask');
  assert.equal(classify({ text: 'new rule for the repo' }).redirect, 'create-rule');
});

test('classify: files beat chat; no files is not conversation unless named', () => {
  const rule = classify({ paths: ['.cursor/rules/api.mdc'], text: 'convert this' });
  assert.deepEqual(kinds(rule), ['from-rule']);
  assert.equal(classify({ text: 'please convert this' }).status, 'ask');
  const url = classify({ text: 'convert https://example.com/guide.html' });
  assert.deepEqual(kinds(url), ['from-document']);
});

test('convert: refuses documents', () => {
  const r = convertSource({ file: '/tmp/book.pdf', text: '%PDF' });
  assert.equal(r.status, 'error');
  assert.match(r.reason, /from-document/);
});

test('merge: refuses a non-skill path and outlines two skills', () => {
  const dir = mkdtempSync(join(tmpdir(), 'cas-outline-'));
  try {
    assert.equal(mergeSkills({ sources: [dir, dir] }).status, 'error');
    const a = join(dir, 'a');
    const b = join(dir, 'b');
    mkdirSync(a);
    mkdirSync(b);
    writeFileSync(join(a, 'SKILL.md'), '---\nname: alpha\ndescription: "A. Use when a."\n---\nSee [n.md](n.md)\n');
    writeFileSync(join(a, 'n.md'), '# note\n');
    writeFileSync(join(b, 'SKILL.md'), '---\nname: beta\ndescription: "B. Use when b."\n---\n# B\n');
    const r = mergeSkills({ sources: [a, b], name: 'alpha-beta' });
    assert.equal(r.status, 'ok');
    assert.equal(r.proposedName, 'alpha-beta');
    assert.deepEqual(r.sources.map((s) => s.name), ['alpha', 'beta']);
    assert.ok(r.sources[0].linked.includes('n.md'));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('extract_document: --check exits 0', () => {
  const r = spawnSync('python3', [join(scripts, 'extract_document.py'), '--check'], { encoding: 'utf8', cwd: scripts });
  assert.equal(r.status, 0, r.stderr || r.stdout);
  assert.match(r.stdout, /document extractor check/);
});

test('extract_document: extracts HTML, refuses rules layout', () => {
  const dir = mkdtempSync(join(tmpdir(), 'cas-doc-'));
  try {
    const html = join(dir, 'page.html');
    writeFileSync(html, '<html><body><h1>Chapter 1 Intro</h1><p>Hello</p><h1>Chapter 2 Next</h1></body></html>');
    const out = join(dir, 'out');
    mkdirSync(out);
    const ok = spawnSync('python3', [join(scripts, 'extract_document.py'), '--json', '--out', out, html], { encoding: 'utf8', cwd: scripts });
    assert.equal(ok.status, 0, ok.stderr || ok.stdout);
    assert.match(ok.stdout, /extracted /);
    const rulesDir = join(dir, 'rules');
    mkdirSync(rulesDir);
    const banned = join(rulesDir, 'note.txt');
    writeFileSync(banned, 'not a document to extract');
    const bad = spawnSync('python3', [join(scripts, 'extract_document.py'), banned], { encoding: 'utf8', cwd: scripts });
    assert.notEqual(bad.status, 0);
    assert.match(bad.stderr, /from-rule or from-agent/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
