import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
for (const path of [
  'skills/engineering/dev-cache-cleanup/tests',
  'skills/agent-authoring/mcp-management/tests',
  'skills/delivery/file-toolkit/tests',
  'skills/delivery/write-adr/scripts',
  'skills/product/visual-art/scripts',
]) {
  test(`${path}: helper behavior and boundary checks`, (context) => {
    const result = spawnSync('python3', ['-I', '-B', '-m', 'unittest', 'discover', '-s', path, '-p', 'test_*.py', '-v'], {
      cwd: root, encoding: 'utf8', timeout: 120000,
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1' },
    });
    assert.equal(result.status, 0, result.stdout + result.stderr + String(result.error ?? ''));
    const count = /Ran (\d+) tests?/.exec(result.stderr);
    assert.ok(count && Number(count[1]) > 0, 'helper suite must execute tests');
    context.diagnostic(path + ': ' + count[0] + '; ' + result.stderr.trim().split('\n').at(-1));
  });
}
test('period activity report: dates, attribution and file guards', () => {
  const result = spawnSync(process.execPath, ['--test', 'skills/focus/standup/scripts/period-report.test.mjs'], {
    cwd: root, encoding: 'utf8', timeout: 30000,
  });
  assert.equal(result.status, 0, result.stdout + result.stderr + String(result.error ?? ''));
});

// Discovery is part of making a capability usable from the stack.
for (const [query, expected] of [
  ['development cache cleanup disk usage', 'dev-cache-cleanup'],
  ['android apk aab gradle deriveddata cache', 'dev-cache-cleanup'],
  ['MCP server connection tools', 'mcp-management'],
  ['parse create convert images audio documents', 'file-toolkit'],
  ['seeded canvas generative animated GIF', 'visual-art'],
]) {
  test(`catalog discovers ${expected}`, async () => {
    const {collect, rank} = await import('../skills/workflow/find-skills/scripts/catalog.mjs');
    const names = rank(collect([root + 'skills']), query).slice(0, 3).map(row => row.name);
    assert.ok(names.includes(expected), `${expected} missing from ${names}`);
  });
}
