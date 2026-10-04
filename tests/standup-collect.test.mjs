import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import {
  browserDbs, chromiumToUnix, classifyUrl, dayRange, findRepos, hostMatches, looksSecret, parseSessionLines,
  parseShellHistory, summarizeShell, summarizeVisits, toolOf,
} from '../skills/workflow/standup/scripts/collect.mjs';

const script = join(dirname(fileURLToPath(import.meta.url)), '../skills/workflow/standup/scripts/collect.mjs');
const hasSqlite = spawnSync('sqlite3', ['-version']).status === 0;

test('range: a mid-week day reports yesterday only', () => {
  const r = dayRange({ today: '2026-10-07' }); // Wednesday
  assert.equal(r.start, '2026-10-06');
  assert.equal(r.end, '2026-10-06');
  assert.equal(r.label, 'yesterday (2026-10-06)');
});

test('range: Monday covers Friday through Sunday', () => {
  const r = dayRange({ today: '2026-10-05' });
  assert.equal(r.start, '2026-10-02');
  assert.equal(r.end, '2026-10-04');
  assert.deepEqual(r.days.map((d) => d.working), [true, false, false]);
  assert.equal(r.label, 'Fri 2026-10-02 – Sun 2026-10-04');
});

test('range: walks back over a holiday to the last working day', () => {
  const r = dayRange({ today: '2026-10-07', holidays: ['2026-10-06', '2026-10-05'] }); // Wed after a Mon+Tue holiday
  assert.equal(r.start, '2026-10-02');
  assert.equal(r.end, '2026-10-06');
});

test('range: honours a custom work week and survives month and year boundaries', () => {
  const sunThu = dayRange({ today: '2026-10-04', workdays: [7, 1, 2, 3, 4] }); // Sunday, week runs Sun-Thu
  assert.equal(sunThu.start, '2026-10-01');
  assert.equal(sunThu.end, '2026-10-03');
  const newYear = dayRange({ today: '2027-01-04' });
  assert.equal(newYear.start, '2027-01-01');
  assert.equal(newYear.end, '2027-01-03');
});

test('range: carries unix bounds and a local offset', () => {
  const r = dayRange({ today: '2026-10-07' });
  assert.equal(r.endTs - r.startTs, 86399);
  assert.match(r.startIso, /^2026-10-06T00:00:00[+-]\d\d:\d\d$/);
});

test('shell history: parses zsh, bash and fish, and counts untimed lines', () => {
  const zsh = ': 1760000000:0;git commit -m x\n: 1760000100:0;echo a \\\nb\n';
  assert.deepEqual(parseShellHistory(zsh).entries, [
    { ts: 1760000000, cmd: 'git commit -m x' },
    { ts: 1760000100, cmd: 'echo a \nb' },
  ]);
  const bash = '#1760000000\nmake test\n#1760000200\nnpm ci\n';
  assert.equal(parseShellHistory(bash).entries.length, 2);
  const fish = '- cmd: cargo build\n  when: 1760000300\n- cmd: ls\n  when: 1760000400\n';
  assert.equal(parseShellHistory(fish).entries[0].cmd, 'cargo build');
  const plain = parseShellHistory('git status\nls\n');
  assert.equal(plain.entries.length, 0);
  assert.equal(plain.untimed, 2);
});

test('shell history: filters to the window, drops noise, withholds anything secret-looking', () => {
  const entries = [
    { ts: 100, cmd: 'git rebase -i main' },
    { ts: 110, cmd: 'ls -la' },
    { ts: 120, cmd: 'export GITLAB_TOKEN=glpat-abcdefghijklmnop' },
    { ts: 130, cmd: 'curl -u me:hunter2 https://example.com' },
    { ts: 140, cmd: 'git rebase -i main' },
    { ts: 999, cmd: 'npm test' },
  ];
  const s = summarizeShell(entries, { startTs: 0, endTs: 500 });
  assert.equal(s.inRange, 5);
  assert.equal(s.redacted, 2);
  assert.deepEqual(s.commands.map((c) => c.cmd), ['git rebase -i main']);
  assert.deepEqual(s.tools, [{ tool: 'git rebase', count: 2 }]);
});

test('secret detection: flags tokens and long mixed strings but not commit hashes', () => {
  assert.ok(looksSecret('curl -H "Authorization: x" https://a.b'));
  assert.ok(looksSecret('deploy --key aB3dE5gH7jK9mN1pQ3sT5vW7yZ9bC1dE3fG'));
  assert.ok(!looksSecret('git show 4f3c2b1a9e8d7c6b5a4f3c2b1a9e8d7c6b5a4f3c'));
  assert.ok(!looksSecret('npm run build'));
});

test('toolOf: skips env assignments and sudo, keeps the subcommand for known tools', () => {
  assert.equal(toolOf('FOO=1 sudo git -C x log'), 'git');
  assert.equal(toolOf('git push origin main'), 'git push');
  assert.equal(toolOf('/usr/local/bin/terraform plan'), 'terraform plan');
  assert.equal(toolOf(''), null);
});

test('findRepos: finds repos at the root and below, skips node_modules, stops at a repo', () => {
  const root = mkdtempSync(join(tmpdir(), 'standup-repos-'));
  try {
    for (const p of ['a/.git', 'b/c/.git', 'node_modules/x/.git', 'a/nested/.git']) mkdirSync(join(root, p), { recursive: true });
    const found = findRepos([root]).map((p) => p.slice(root.length + 1)).sort();
    assert.deepEqual(found, ['a', 'b/c']);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('AI sessions: keeps only real user prompts inside the window', () => {
  const line = (o) => JSON.stringify(o);
  const lines = [
    line({ type: 'user', timestamp: '2026-10-03T03:00:00Z', cwd: '/work/app', message: { role: 'user', content: 'fix the flaky retry test' } }),
    line({ type: 'user', timestamp: '2026-10-03T03:01:00Z', message: { content: [{ type: 'tool_result', content: 'ok' }] } }),
    line({ type: 'user', timestamp: '2026-10-03T03:02:00Z', message: { content: '<system-reminder>x</system-reminder>' } }),
    line({ type: 'user', timestamp: '2026-10-03T03:03:00Z', isSidechain: true, message: { content: 'subagent prompt' } }),
    line({ type: 'user', timestamp: '2026-10-09T03:00:00Z', message: { content: 'outside window' } }),
    line({ type: 'user', timestamp: '2026-10-03T04:00:00Z', message: { content: 'use token abcdefghijklmnopqrstuvwxyz0123456789ABCD' } }),
    'not json',
  ];
  const { cwd, prompts } = parseSessionLines(lines, { startTs: Date.parse('2026-10-03T00:00:00Z') / 1000, endTs: Date.parse('2026-10-04T00:00:00Z') / 1000 });
  assert.equal(cwd, '/work/app');
  assert.deepEqual(prompts, ['fix the flaky retry test', '[redacted]']);
});

test('browser: host matching, URL cleaning and work detection on self-hosted tools', () => {
  assert.ok(hostMatches('gist.github.com', ['github.com']));
  assert.ok(hostMatches('team.atlassian.net', ['*.atlassian.net']));
  assert.ok(!hostMatches('notgithub.com', ['github.com']));
  const c = classifyUrl('https://git.example.org/group/app/-/merge_requests/42?token=abc#note_1', ['github.com']);
  assert.equal(c.clean, 'https://git.example.org/group/app/-/merge_requests/42');
  assert.ok(c.work);
  assert.ok(!classifyUrl('https://news.example.com/story', ['github.com']).work);
  assert.equal(classifyUrl('chrome://settings', []), null);
});

test('browser: groups work visits by host and reports other sites as domain counts only', () => {
  const rows = [
    { url: 'https://github.com/o/r/pull/7?x=1', title: 'Fix retry · PR 7', ts: 10 },
    { url: 'https://github.com/o/r/pull/7', title: 'Fix retry · PR 7', ts: 20 },
    { url: 'https://github.com/o/r/issues/3', title: '', ts: 30 },
    { url: 'https://news.example.com/secret-article-title', title: 'private', ts: 40 },
  ];
  const s = summarizeVisits(rows, { patterns: ['github.com'], includeAll: true });
  assert.equal(s.hosts.length, 1);
  assert.equal(s.hosts[0].visits, 3);
  assert.equal(s.hosts[0].pages[0].visits, 2);
  assert.equal(s.filteredOut, 1);
  assert.deepEqual(s.otherDomains, [{ host: 'news.example.com', visits: 1 }]);
  assert.ok(!JSON.stringify(s).includes('secret-article-title'));
  assert.equal(summarizeVisits(rows, { patterns: ['github.com'] }).otherDomains.length, 0);
});

test('browser: Chromium epoch converts to unix time', () => {
  assert.equal(chromiumToUnix((1760000000 + 11644473600) * 1e6), 1760000000);
});

test('browser: locates Chromium, Firefox and Safari profiles under a fake home', () => {
  const home = mkdtempSync(join(tmpdir(), 'standup-home-'));
  try {
    for (const p of [
      'Library/Application Support/Google/Chrome/Default', 'Library/Application Support/Google/Chrome/Profile 2',
      'Library/Application Support/Firefox/Profiles/abc.default', 'Library/Safari',
    ]) mkdirSync(join(home, p), { recursive: true });
    for (const f of [
      'Library/Application Support/Google/Chrome/Default/History', 'Library/Application Support/Google/Chrome/Profile 2/History',
      'Library/Application Support/Firefox/Profiles/abc.default/places.sqlite', 'Library/Safari/History.db',
    ]) writeFileSync(join(home, f), '');
    const { dbs } = browserDbs(home, 'darwin');
    assert.deepEqual(dbs.map((d) => `${d.browser}:${d.profile}`).sort(), ['chrome:Default', 'chrome:Profile 2', 'firefox:abc.default', 'safari:default']);
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

test('cli: range prints a window and rejects missing flags', () => {
  const out = execFileSync('node', [script, 'range', '--today', '2026-10-05', '--json'], { encoding: 'utf8', env: { ...process.env, STANDUP_CONFIG: '/nonexistent.json' } });
  assert.equal(JSON.parse(out).start, '2026-10-02');
  const bad = spawnSync('node', [script, 'machine'], { encoding: 'utf8', env: { ...process.env, STANDUP_CONFIG: '/nonexistent.json' } });
  assert.equal(bad.status, 1);
  assert.match(bad.stderr, /--start and --end/);
});

test('cli: reads a Chromium-format history database end to end', { skip: !hasSqlite && 'sqlite3 CLI not installed' }, () => {
  const home = mkdtempSync(join(tmpdir(), 'standup-e2e-'));
  try {
    const dir = join(home, process.platform === 'darwin' ? 'Library/Application Support/Google/Chrome/Default' : '.config/google-chrome/Default');
    mkdirSync(dir, { recursive: true });
    const when = Math.floor(new Date(2026, 9, 6, 11, 0, 0).getTime() / 1000);
    const t = (when + 11644473600) * 1e6;
    execFileSync('sqlite3', [join(dir, 'History'), `CREATE TABLE urls(id INTEGER PRIMARY KEY, url TEXT, title TEXT);
      CREATE TABLE visits(id INTEGER PRIMARY KEY, url INTEGER, visit_time INTEGER);
      INSERT INTO urls VALUES (1,'https://github.com/o/r/pull/9?a=b','Add retry · PR 9'),(2,'https://shop.example.com/cart','cart');
      INSERT INTO visits VALUES (1,1,${t}),(2,2,${t});`]);
    const out = spawnSync('node', [script, 'browser', '--start', '2026-10-06', '--end', '2026-10-06', '--json'], {
      encoding: 'utf8', env: { ...process.env, HOME: home, STANDUP_CONFIG: '/nonexistent.json' },
    });
    const data = JSON.parse(out.stdout);
    assert.deepEqual(data.browsers, ['chrome:Default']);
    assert.equal(data.hosts[0].pages[0].url, 'https://github.com/o/r/pull/9');
    assert.equal(data.filteredOut, 1);
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

function runBrowser(home) {
  const out = spawnSync('node', [script, 'browser', '--start', '2026-10-06', '--end', '2026-10-06', '--json'], {
    encoding: 'utf8', env: { ...process.env, HOME: home, STANDUP_CONFIG: '/nonexistent.json' },
  });
  return JSON.parse(out.stdout);
}
const noon = Math.floor(new Date(2026, 9, 6, 12, 0, 0).getTime() / 1000);

test('cli: reads a Firefox-format history database', { skip: !hasSqlite && 'sqlite3 CLI not installed' }, () => {
  const home = mkdtempSync(join(tmpdir(), 'standup-ff-'));
  try {
    const dir = join(home, process.platform === 'darwin' ? 'Library/Application Support/Firefox/Profiles/x.default' : '.mozilla/firefox/x.default');
    mkdirSync(dir, { recursive: true });
    execFileSync('sqlite3', [join(dir, 'places.sqlite'), `CREATE TABLE moz_places(id INTEGER PRIMARY KEY, url TEXT, title TEXT);
      CREATE TABLE moz_historyvisits(id INTEGER PRIMARY KEY, place_id INTEGER, visit_date INTEGER);
      INSERT INTO moz_places VALUES (1,'https://gitlab.com/g/p/-/merge_requests/5','MR 5');
      INSERT INTO moz_historyvisits VALUES (1,1,${noon * 1e6});`]);
    const data = runBrowser(home);
    assert.deepEqual(data.browsers, ['firefox:x.default']);
    assert.equal(data.hosts[0].pages[0].title, 'MR 5');
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

test('cli: reads a Safari-format history database', { skip: (!hasSqlite && 'sqlite3 CLI not installed') || (process.platform !== 'darwin' && 'Safari is macOS only') }, () => {
  const home = mkdtempSync(join(tmpdir(), 'standup-safari-'));
  try {
    mkdirSync(join(home, 'Library/Safari'), { recursive: true });
    execFileSync('sqlite3', [join(home, 'Library/Safari/History.db'), `CREATE TABLE history_items(id INTEGER PRIMARY KEY, url TEXT);
      CREATE TABLE history_visits(id INTEGER PRIMARY KEY, history_item INTEGER, visit_time REAL, title TEXT);
      INSERT INTO history_items VALUES (1,'https://team.atlassian.net/browse/ABC-12');
      INSERT INTO history_visits VALUES (1,1,${noon - 978307200},'ABC-12 Retry bug');`]);
    const data = runBrowser(home);
    assert.deepEqual(data.browsers, ['safari:default']);
    assert.equal(data.hosts[0].pages[0].title, 'ABC-12 Retry bug');
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});
