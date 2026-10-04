import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { diffHooks } from '../hooks/lib/generate.mjs';
import { loadHooks } from '../hooks/lib/registry.mjs';
import { allow, ask, deny, note, render, toResult } from '../hooks/lib/result.mjs';
import { validateTree } from '../scripts/validate.mjs';

const repo = join(dirname(fileURLToPath(import.meta.url)), '..');
const hooksDir = join(repo, 'hooks');
const launcher = join(hooksDir, 'lib/launcher.mjs');

function tmp(fn) {
  const dir = mkdtempSync(join(tmpdir(), 'levistack-'));
  try {
    return fn(dir);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

function run(hook, input, { optIn = true, runtime, env = {} } = {}) {
  return tmp((home) => {
    if (optIn) writeFileSync(join(home, `${hook}.on`), '');
    const args = [launcher, ...(runtime ? [`--runtime=${runtime}`] : []), hook];
    const r = spawnSync('node', args, {
      input: JSON.stringify(input),
      encoding: 'utf8',
      env: { ...process.env, LEVISTACK_HOME: home, CLAUDE_PLUGIN_ROOT: repo, ...env },
    });
    return { status: r.status, stdout: r.stdout, stderr: r.stderr };
  });
}

const decision = (r) => JSON.parse(r.stdout).hookSpecificOutput.permissionDecision;
const hookNames = readdirSync(hooksDir).filter((f) => f.endsWith('.mjs')).map((f) => f.slice(0, -4));

// --- registry and generated files ---

test('every hook exports valid meta and a handler', async () => {
  const hooks = await loadHooks(hooksDir);
  assert.deepEqual(hooks.map((h) => h.name).sort(), hookNames.sort());
  for (const h of hooks) assert.deepEqual(h.problems, [], h.name);
});

test('hooks.json and the hooks README table are generated from meta and in sync', async () => {
  assert.deepEqual(await diffHooks(repo), []);
});

test('validator rejects shell scripts under hooks/', () => {
  tmp((dir) => {
    mkdirSync(join(dir, 'hooks'));
    writeFileSync(join(dir, 'hooks/x.sh'), '#!/bin/bash\n');
    writeFileSync(join(dir, 'package.json'), '{}');
    const errors = validateTree(dir);
    assert.ok(errors.some((e) => e.includes('hooks/x.sh') && e.includes('not shell')), errors.join('\n'));
  });
});

// --- result rendering ---

test('render: claude PreToolUse uses permissionDecision JSON, exit 0', () => {
  const r = render(deny('no'), { runtime: 'claude', event: 'PreToolUse' });
  assert.equal(r.exitCode, 0);
  assert.deepEqual(JSON.parse(r.stdout).hookSpecificOutput, { hookEventName: 'PreToolUse', permissionDecision: 'deny', permissionDecisionReason: 'no' });
  assert.equal(JSON.parse(render(ask('hm'), { event: 'PreToolUse' }).stdout).hookSpecificOutput.permissionDecision, 'ask');
});

test('render: claude notes go where the event reads them', () => {
  assert.equal(render(note('hi'), { event: 'SessionStart' }).stdout, 'hi');
  assert.equal(JSON.parse(render(note('hi'), { event: 'PostToolUse' }).stdout).hookSpecificOutput.additionalContext, 'hi');
  assert.equal(JSON.parse(render(note('hi'), { event: 'Stop' }).stdout).systemMessage, 'hi');
  assert.equal(JSON.parse(render(deny('no'), { event: 'PostToolUse' }).stdout).decision, 'block');
  assert.equal(render(allow(), { event: 'Stop' }).stdout, '');
});

test('render: cursor shapes, and deny exits 2', () => {
  assert.deepEqual(JSON.parse(render(allow(), { runtime: 'cursor', event: 'beforeShellExecution' }).stdout), { permission: 'allow' });
  assert.deepEqual(JSON.parse(render(allow(), { runtime: 'cursor', event: 'afterFileEdit' }).stdout), { continue: true });
  assert.equal(JSON.parse(render(note('hi'), { runtime: 'cursor', event: 'beforeShellExecution' }).stdout).agent_message, 'hi');
  const denied = render(deny('no'), { runtime: 'cursor', event: 'beforeReadFile' });
  assert.equal(denied.exitCode, 2);
  assert.equal(JSON.parse(denied.stdout).permission, 'deny');
});

test('toResult: nothing, a string and a result are all accepted', () => {
  assert.equal(toResult('').kind, 'allow');
  assert.deepEqual(toResult('ctx'), note('ctx'));
  assert.deepEqual(toResult(deny('x')), deny('x'));
});

// --- launcher ---

for (const hook of hookNames) {
  test(`${hook}: silent and exit 0 without the opt-in flag`, () => {
    const r = run(hook, { tool_name: 'Bash', tool_input: { command: 'rm -rf /' } }, { optIn: false });
    assert.equal(r.status, 0);
    assert.equal(r.stdout, '');
  });
}

test('launcher: garbage stdin, bad names and unknown hooks still exit 0', () => {
  tmp((home) => {
    writeFileSync(join(home, 'careful-guard.on'), '');
    const env = { ...process.env, LEVISTACK_HOME: home, CLAUDE_PLUGIN_ROOT: repo };
    for (const [name, input] of [['careful-guard', 'not json'], ['../etc/passwd', '{}'], ['does-not-exist', '{}'], ['lib/launcher', '{}'], ['', '{}']]) {
      const r = spawnSync('node', [launcher, name].filter(Boolean), { input, env });
      assert.equal(r.status, 0, name);
    }
  });
});

// --- hooks ---

test('session-start: opted in, prints the rules digest without frontmatter', () => {
  const r = run('session-start', { hook_event_name: 'SessionStart' });
  assert.equal(r.status, 0);
  assert.match(r.stdout, /Levistack rules/);
  assert.match(r.stdout, /commit-messages/);
  assert.ok(!r.stdout.includes('alwaysApply'), 'frontmatter must be stripped');
});

test('careful-guard: asks before destructive commands', () => {
  for (const command of ['rm -rf /', 'git push --force origin main', 'git reset --hard HEAD~1', 'psql -c "DROP TABLE users"']) {
    const r = run('careful-guard', { hook_event_name: 'PreToolUse', tool_name: 'Bash', tool_input: { command } });
    assert.equal(r.status, 0);
    assert.equal(decision(r), 'ask', command);
  }
});

test('careful-guard: stays quiet for safe commands and force-with-lease', () => {
  for (const command of ['ls -la', 'git status', 'git push --force-with-lease origin feature', 'rm -rf ./build']) {
    const r = run('careful-guard', { hook_event_name: 'PreToolUse', tool_name: 'Bash', tool_input: { command } });
    assert.equal(r.status, 0);
    assert.equal(r.stdout, '', command);
  }
});

test('careful-guard: also works for Cursor-shaped input and output', () => {
  const r = run('careful-guard', { hook_event_name: 'beforeShellExecution', command: 'git reset --hard' }, { runtime: 'cursor' });
  assert.equal(r.status, 0);
  assert.equal(JSON.parse(r.stdout).permission, 'ask');
});

test('large-read-guard: blocks an untargeted Read of a big file, lets targeted and small reads pass', () => {
  tmp((dir) => {
    const big = join(dir, 'big.txt');
    const small = join(dir, 'small.txt');
    writeFileSync(big, 'line\n'.repeat(400));
    writeFileSync(small, 'line\n'.repeat(10));
    const env = { LEVISTACK_METRICS_DIR: join(dir, 'metrics') };
    const read = (file_path, extra = {}) => run('large-read-guard', { hook_event_name: 'PreToolUse', tool_name: 'Read', cwd: dir, tool_input: { file_path, ...extra } }, { env });

    const blocked = read(big);
    assert.equal(blocked.status, 0);
    assert.equal(decision(blocked), 'deny');
    assert.match(JSON.parse(blocked.stdout).hookSpecificOutput.permissionDecisionReason, /400 lines.*bulk-reader/);
    assert.equal(read('big.txt').stdout.includes('deny'), true, 'relative paths resolve against cwd');
    assert.equal(read(big, { offset: 1, limit: 50 }).stdout, '');
    assert.equal(read(small).stdout, '');
    assert.equal(read(join(dir, 'missing.txt')).stdout, '');
    assert.equal(run('large-read-guard', { tool_name: 'Read', cwd: dir, tool_input: { file_path: big } }, { env: { ...env, LEVISTACK_MAX_READ_LINES: '1000' } }).stdout, '');
  });
});

test('large-read-guard: blocks bare cat of a big file, not piped or targeted shell reads', () => {
  tmp((dir) => {
    writeFileSync(join(dir, 'big.txt'), 'line\n'.repeat(400));
    const bash = (command, opts) => run('large-read-guard', { hook_event_name: 'PreToolUse', tool_name: 'Bash', cwd: dir, tool_input: { command } }, opts);
    const env = { LEVISTACK_METRICS_DIR: join(dir, 'metrics') };
    assert.equal(decision(bash('cat big.txt', { env })), 'deny');
    assert.equal(decision(bash('head "big.txt"', { env })), 'deny');
    for (const command of ['cat big.txt | head -5', 'grep x big.txt', 'sed -n 1,5p big.txt', 'cat big.txt > out.txt', 'ls big.txt', 'cat nope.txt']) {
      assert.equal(bash(command, { env }).stdout, '', command);
    }
    const cursor = bash('cat big.txt', { runtime: 'cursor', env });
    assert.equal(cursor.status, 2);
    assert.equal(JSON.parse(cursor.stdout).permission, 'deny');
  });
});

test('generated-file-guard: asks for generated files and coverage artifacts only', () => {
  tmp((dir) => {
    writeFileSync(join(dir, 'gen.go'), '// Code generated by mockery. DO NOT EDIT.\npackage x\n');
    writeFileSync(join(dir, 'api.ts'), '/* @generated */\nexport {};\n');
    writeFileSync(join(dir, 'real.go'), `package x\n${'\n'.repeat(10)}// do not edit this lower down\n`);
    const edit = (file_path, tool_name = 'Edit') => run('generated-file-guard', { hook_event_name: 'PreToolUse', tool_name, cwd: dir, tool_input: { file_path } });
    assert.equal(decision(edit('gen.go')), 'ask');
    assert.equal(decision(edit(join(dir, 'api.ts'), 'Write')), 'ask');
    assert.equal(decision(edit('coverage.out', 'Write')), 'ask');
    assert.equal(decision(edit('lcov.info', 'Write')), 'ask');
    assert.equal(edit('new-file.go', 'Write').stdout, '', 'a new file cannot be generated output yet');
    assert.equal(edit('real.go').stdout, '', 'only the header counts');
  });
});
