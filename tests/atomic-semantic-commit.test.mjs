import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { checkMessage } from '../skills/delivery/atomic-semantic-commit/scripts/check-message.mjs';
import { analyze, classify, scopeOf } from '../skills/delivery/atomic-semantic-commit/scripts/group-changes.mjs';

const repo = join(dirname(fileURLToPath(import.meta.url)), '..');
const checkCli = join(repo, 'skills/delivery/atomic-semantic-commit/scripts/check-message.mjs');
const codes = (msg, opts) => checkMessage(msg, opts).filter((f) => f.severity !== 'info').map((f) => f.code);
const all = (msg, opts) => checkMessage(msg, opts).map((f) => f.code);

// ---- check-message ---------------------------------------------------------------------------

test('accepts the gist example and a normal scoped message', () => {
  assert.deepEqual(codes('feat: add hat wobble'), []);
  assert.deepEqual(codes('fix(auth): retry token refresh on 401'), []);
  assert.deepEqual(codes('feat(api)!: rename /v1/orders to /v1/checkout\n\nBREAKING CHANGE: use /v1/checkout. The old route returns 410.'), []);
});

test('rejects a message that is not in the semantic format', () => {
  assert.ok(codes('Fixed the bug').includes('format'));
  assert.ok(codes('fix login').includes('format'));
  assert.ok(codes('fix(): empty scope') .includes('scope-empty'));
});

test('type checks: unknown, uppercase, and extra types', () => {
  assert.ok(codes('feature: add x').includes('type'));
  assert.ok(codes('Feat: add x').includes('type-case'));
  assert.deepEqual(codes('perf(search): cache the index'), []);
  assert.ok(all('perf(search): cache the index').includes('extra-type'));
  assert.ok(codes('perf(search): cache the index', { baseOnly: true }).includes('type'));
});

test('subject rules: mood, case, period, length, vague words, two actions, punctuation', () => {
  assert.ok(codes('feat: added login page').includes('mood'));
  assert.ok(codes('feat: adds login page').includes('mood'));
  assert.ok(codes('feat: Add login page').includes('case'));
  assert.ok(!codes('feat: OAuth2 login').includes('case'), 'identifiers keep their case');
  assert.ok(codes('feat: add login page.').includes('subject-period'));
  assert.ok(codes(`feat: ${'a'.repeat(80)}`).includes('subject-length'));
  assert.ok(codes(`feat: ${'word '.repeat(12).trim()}`).includes('subject-long'));
  assert.ok(codes('chore: misc cleanup').includes('vague'));
  assert.ok(codes('fix(cart): improve stuff').includes('vague'));
  assert.ok(codes('feat(login): add form and fix validation bug').includes('two-actions'));
  assert.ok(!codes('feat(delivery): add STE rules and helper scripts').includes('two-actions'), 'a compound object is one action');
  assert.ok(codes('feat: add login — with validation').includes('punctuation'));
});

test('body rules: blank line, wrap, sentence length, dashes, voice, attribution', () => {
  assert.ok(codes('fix(a): fix b\nno blank line').includes('blank-line'));
  assert.ok(codes(`fix(a): fix b\n\n${'x'.repeat(90)}`).includes('wrap'));
  assert.ok(codes(`fix(a): fix b\n\n${'word '.repeat(25).trim()}.`).includes('sentence-length'));
  assert.ok(codes('fix(a): fix b\n\nThe cache is stale; delete the key.').includes('punctuation'));
  assert.ok(codes('fix(a): fix b\n\nThis commit fixes the cache.').includes('voice'));
  assert.ok(codes('fix(a): fix b\n\nNow the cache works.').includes('voice'));
  assert.ok(codes('fix(a): fix b\n\nBody.\n\nCo-Authored-By: Someone <a@b.c>').includes('attribution'));
  assert.deepEqual(codes('fix(a): fix b\n\nThe cache kept old data. Delete the key on update.\n\nCloses #42'), []);
});

test('body checks skip code blocks, URLs, trailers and comment lines', () => {
  const msg = 'fix(a): fix b\n\nSee https://example.com/' + 'x'.repeat(80) + '\n\n```\n' + 'y'.repeat(100) + '\n```\n\n# a git comment; with — dashes\nCloses #1';
  assert.deepEqual(codes(msg), []);
});

test('a breaking change or a revert needs a body', () => {
  assert.ok(codes('feat(api)!: rename the route').includes('breaking-body'));
  assert.ok(codes('revert: remove the cache').includes('revert-body'));
});

test('merge, fixup and revert-generated messages are not checked', () => {
  assert.deepEqual(codes('Merge branch main into feature'), []);
  assert.deepEqual(codes('fixup! fix(auth): retry token refresh'), []);
  assert.deepEqual(codes('Revert "feat: add x"'), []);
  assert.ok(codes('').includes('empty'));
});

test('cli: exit codes, --file, --range and --json', () => {
  const dir = mkdtempSync(join(tmpdir(), 'ac-msg-'));
  try {
    const run = (...a) => spawnSync('node', [checkCli, ...a], { encoding: 'utf8', cwd: dir });
    assert.equal(run('feat: add hat wobble').status, 0);
    assert.equal(run('Fixed the bug').status, 1);
    assert.equal(run('feat: add login page.', '--strict').status, 1);
    assert.equal(run('feat: Add login', '--strict').status, 1, 'warnings fail under --strict');
    assert.equal(run('feat: Add login').status, 0, 'warnings pass by default');
    assert.equal(run().status, 2);
    writeFileSync(join(dir, 'MSG'), 'fix(auth): retry token refresh\n\n# Please enter the commit message\n');
    assert.equal(run('--file', join(dir, 'MSG')).status, 0);
    assert.equal(JSON.parse(run('Fixed it', '--json').stdout)[0].findings[0].code, 'format');

    const g = (...a) => execFileSync('git', ['-c', 'user.name=t', '-c', 'user.email=t@t', ...a], { cwd: dir, encoding: 'utf8' });
    g('init', '-q');
    writeFileSync(join(dir, 'a.txt'), '1');
    g('add', '.');
    g('commit', '-q', '-m', 'feat: add a');
    writeFileSync(join(dir, 'a.txt'), '2');
    g('commit', '-qam', 'Fixed the thing.');
    const r = run('--range', 'HEAD~1..HEAD');
    assert.equal(r.status, 1);
    assert.match(r.stdout, /FAIL/);
    assert.equal(run('--range', 'HEAD~1').status, 0, 'the first commit alone is fine');
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

// ---- group-changes ---------------------------------------------------------------------------

test('classify: kinds by path', () => {
  const k = (p) => classify(p);
  assert.equal(k('src/auth/login.ts'), 'source');
  assert.equal(k('test/auth/login.test.ts'), 'test');
  assert.equal(k('lib/a_test.exs'), 'test');
  assert.equal(k('README.md'), 'docs');
  assert.equal(k('docs/guide.md'), 'docs');
  assert.equal(k('package.json'), 'build');
  assert.equal(k('mix.lock'), 'build');
  assert.equal(k('.github/workflows/ci.yml'), 'ci');
  assert.equal(k('.gitignore'), 'chore');
  assert.equal(k('.env'), 'danger');
  assert.equal(k('config/.env.local'), 'danger');
  assert.equal(k('node_modules/x/index.js'), 'danger');
  assert.equal(k('server.log'), 'danger');
});

test('scopeOf: the context a path belongs to', () => {
  assert.equal(scopeOf('src/auth/login.ts'), 'auth');
  assert.equal(scopeOf('test/auth/login.test.ts'), 'auth');
  assert.equal(scopeOf('packages/ui/src/button.ts'), 'ui');
  assert.equal(scopeOf('apps/web/lib/x.ex'), 'web');
  assert.equal(scopeOf('lib/my_app/accounts/user.ex', 'my-app'), 'accounts');
  assert.equal(scopeOf('src/login.ts'), 'login');
  assert.equal(scopeOf('src/login.test.ts'), 'login');
  assert.equal(scopeOf('index.js'), null);
});

function gitRepo() {
  const dir = mkdtempSync(join(tmpdir(), 'ac-grp-'));
  const g = (...a) => execFileSync('git', ['-c', 'user.name=t', '-c', 'user.email=t@t', ...a], { cwd: dir, encoding: 'utf8' });
  const put = (rel, text) => {
    mkdirSync(dirname(join(dir, rel)), { recursive: true });
    writeFileSync(join(dir, rel), text);
  };
  g('init', '-q');
  put('src/auth/login.ts', 'one\n');
  put('package.json', '{}\n');
  g('add', '.');
  g('commit', '-q', '-m', 'chore: init');
  return { dir, g, put };
}

test('analyze: groups by context and kind, orders them, and skips junk', () => {
  const { dir, put } = gitRepo();
  try {
    put('src/auth/login.ts', 'one\ntwo\nthree\n');
    put('test/auth/login.test.ts', 'a\nb\n');
    put('src/cart/price.ts', 'x\n');
    put('README.md', '# hi\n');
    put('package.json', '{"a":1}\n');
    put('package-lock.json', '{}\n');
    put('.github/workflows/ci.yml', 'on: push\n');
    put('.env', 'SECRET=1\n');
    const r = analyze(dir);
    assert.equal(r.changed, 8);
    assert.deepEqual(r.groups.map((g) => g.group), ['build', 'ci', 'code:auth', 'code:cart', 'docs']);
    const auth = r.groups.find((g) => g.group === 'code:auth');
    assert.equal(auth.files.length, 2, 'the test stays with the code it tests');
    assert.equal(auth.suggestedType, '?');
    assert.equal(r.groups.find((g) => g.group === 'docs').suggestedType, 'docs');
    assert.equal(r.groups.find((g) => g.group === 'build').files.length, 2);
    assert.deepEqual(r.skipped, ['.env']);
    assert.ok(auth.added > 0);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('analyze: a big group is split by its deeper context', () => {
  const { dir, put } = gitRepo();
  try {
    for (let i = 0; i < 6; i++) put(`skills/alpha/s${i}.ts`, 'a\n');
    for (let i = 0; i < 6; i++) put(`skills/beta/s${i}.ts`, 'b\n');
    const r = analyze(dir);
    assert.deepEqual(r.groups.map((g) => g.group).sort(), ['code:skills/alpha', 'code:skills/beta']);
    assert.equal(r.groups[0].scope, r.groups[0].context.split('/').pop());
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('analyze: only edited files get the two-purposes note, not whole-file additions', () => {
  const { dir, put } = gitRepo();
  try {
    put('src/auth/new.ts', Array.from({ length: 500 }, (_, i) => `l${i}`).join('\n'));
    assert.deepEqual(analyze(dir).groups[0].notes, []);
    put('src/auth/login.ts', Array.from({ length: 400 }, (_, i) => `changed ${i}`).join('\n'));
    assert.match(analyze(dir).groups.find((g) => g.files.some((f) => f.path === 'src/auth/login.ts')).notes.join(' '), /edited, not moved/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('analyze: warns when a docs group is huge', () => {
  const { dir, put } = gitRepo();
  try {
    for (let i = 0; i < 22; i++) put(`content/page${i}.md`, 'x\n');
    const docs = analyze(dir).groups.find((g) => g.kind === 'docs');
    assert.match(docs.notes.join(' '), /Markdown files/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('analyze: test-only groups are test commits; a clean tree has no groups', () => {
  const { dir, put } = gitRepo();
  try {
    assert.deepEqual(analyze(dir).groups, []);
    put('test/billing/invoice.test.ts', 'a\n');
    const g = analyze(dir).groups;
    assert.equal(g.length, 1);
    assert.equal(g[0].suggestedType, 'test');
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('analyze: notes large files and partly staged files', () => {
  const { dir, g, put } = gitRepo();
  try {
    put('src/auth/login.ts', Array.from({ length: 400 }, (_, i) => `line ${i}`).join('\n'));
    g('add', 'src/auth/login.ts');
    put('src/auth/login.ts', Array.from({ length: 401 }, (_, i) => `line ${i}`).join('\n') + '\nextra\n');
    const notes = analyze(dir).groups[0].notes.join('\n');
    assert.match(notes, /changed lines/);
    assert.match(notes, /part is staged/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('the atomic-semantic-commit skill passes the repo skill linter', async () => {
  const { lintPath } = await import('../skills/agent-authoring/create-agent/scripts/lint.mjs');
  const bad = lintPath(join(repo, 'skills/delivery/atomic-semantic-commit')).findings.filter((f) => f.severity === 'error' || f.severity === 'warn');
  assert.deepEqual(bad, []);
});
