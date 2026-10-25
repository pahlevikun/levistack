import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { classify } from '../skills/agent-authoring/convert-as-skill/scripts/classify.mjs';
import { convertSource } from '../skills/agent-authoring/convert-as-skill/scripts/convert.mjs';
import { mergeSkills } from '../skills/agent-authoring/convert-as-skill/scripts/merge.mjs';
import { parseSource, plan, scratchStatus } from '../skills/agent-authoring/convert-as-skill/scripts/enhance.mjs';
import { existsSync } from 'node:fs';

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

// ---- enhance-skill ---------------------------------------------------------------------------

function makeSkill(dir, name, extra = '') {
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, 'SKILL.md'), `---\nname: ${name}\ndescription: "A skill. Use when needed."\n---\n# ${name}\n${extra}\n`);
}

test('classify: one skill folder with enhance wording is the enhance-skill use case', () => {
  const dir = mkdtempSync(join(tmpdir(), 'cas-enh-'));
  try {
    const target = join(dir, 'target');
    const other = join(dir, 'other');
    makeSkill(target, 'target');
    makeSkill(other, 'other');
    const r = classify({ paths: [target], text: 'enhance this skill using https://github.com/a/b/tree/main/skills/x' });
    assert.equal(r.status, 'ok');
    assert.deepEqual(kinds(r), ['enhance-skill']);
    assert.equal(r.jobs[0].files[0], target);
    assert.ok(r.jobs[0].files.includes('https://github.com/a/b/tree/main/skills/x'));
    assert.equal(r.jobs[0].guide, 'specialities/enhance-skill/GUIDE.md');
    assert.ok(existsSync(join(scripts, '..', r.jobs[0].guide)), 'the guide exists');
    assert.deepEqual(kinds(classify({ paths: [target], text: 'improve it by learning from upstream' })), ['enhance-skill']);
    assert.equal(classify({ paths: [target, other], text: 'enhance the first with the second' }).status, 'ask');
    assert.deepEqual(kinds(classify({ paths: [target, other], text: 'merge these into one skill' })), ['merge-skills']);
    assert.equal(classify({ text: 'improve the skill from https://github.com/a/b' }).status, 'ask');
    assert.equal(classify({ paths: [target] }).status, 'ask', 'a skill folder alone still asks');
    assert.match(classify({ paths: [target] }).question, /Enhance it/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('enhance: parseSource builds a safe fetch command for each kind of source', () => {
  const gh = parseSource('https://github.com/acme-corp/skills/tree/main/skills/engineering/prototype', 'scratch/x');
  assert.equal(gh.kind, 'github');
  assert.equal(gh.fetch, 'git clone --depth 1 https://github.com/acme-corp/skills.git scratch/x/acme-corp__skills');
  assert.equal(gh.focus, 'skills/engineering/prototype');
  const sk = parseSource('https://www.skills.sh/meodai/skill.color-expert/color-expert', 'scratch/x');
  assert.equal(sk.kind, 'skills.sh');
  assert.equal(sk.focus, 'color-expert');
  assert.match(sk.fetch, /meodai\/skill\.color-expert\.git/);
  const page = parseSource('https://bencho.dev/', 'scratch/x');
  assert.equal(page.kind, 'page');
  assert.match(page.fetch, /^curl -sL https:\/\/bencho\.dev\/ -o scratch\/x\/singles\//);
  assert.equal(parseSource('/definitely/not/here', 'scratch/x').kind, 'missing');
  assert.equal(parseSource('/definitely/not/here', 'scratch/x').fetch, null);
  assert.equal(parseSource(root, 'scratch/x').kind, 'dir');
});

test('enhance: plan inventories the target and refuses a scratch folder that git does not ignore', () => {
  const dir = mkdtempSync(join(tmpdir(), 'cas-plan-'));
  try {
    const g = (...a) => execFileSync('git', ['-C', dir, ...a], { encoding: 'utf8' });
    g('init', '-q');
    const target = join(dir, 'skills', 'demo');
    makeSkill(target, 'demo', 'See [r](references/r.md)');
    mkdirSync(join(target, 'references'));
    writeFileSync(join(target, 'references', 'r.md'), '# r\n');
    const bad = plan({ target, sources: ['https://github.com/a/b'], scratch: join(dir, 'scratch', 'demo-sources') });
    assert.equal(bad.status, 'ok');
    assert.equal(bad.target.name, 'demo');
    assert.equal(bad.scratch.ignored, false);
    assert.ok(bad.warnings.some((w) => /NOT ignored/.test(w)));
    writeFileSync(join(dir, '.gitignore'), 'scratch/\n');
    const good = plan({ target, sources: ['https://github.com/a/b'], scratch: join(dir, 'scratch', 'demo-sources') });
    assert.equal(good.scratch.ignored, true);
    assert.ok(!good.warnings.some((w) => /NOT ignored/.test(w)));
    assert.ok(plan({ target, sources: [] }).warnings.some((w) => /no source/.test(w)));
    assert.equal(plan({ target: dir }).status, 'error');
    assert.equal(scratchStatus('/tmp/elsewhere', dir).ok, true);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('enhance.mjs: cli prints the plan, is read-only and rejects two targets', () => {
  const dir = mkdtempSync(join(tmpdir(), 'cas-cli-'));
  try {
    const target = join(dir, 'demo');
    makeSkill(target, 'demo');
    const run = (...a) => spawnSync('node', [join(scripts, 'enhance.mjs'), ...a], { encoding: 'utf8' });
    const r = run(target, '--source', 'https://github.com/a/b', '--scratch', join(dir, 'scratch'));
    assert.equal(r.status, 0, r.stderr);
    assert.match(r.stdout, /git clone --depth 1 https:\/\/github\.com\/a\/b\.git/);
    assert.ok(!existsSync(join(dir, 'scratch')), 'the script must not create the scratch folder');
    assert.equal(run(target, target).status, 2);
    assert.equal(run().status, 2);
    assert.ok(Array.isArray(JSON.parse(run(target, '--json').stdout).warnings));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
