import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { buildPayload, interpret } from '../skills/agent-authoring/create-hook/scripts/try-hook.mjs';

const recipes = join(dirname(fileURLToPath(import.meta.url)), '..', 'skills', 'agent-authoring', 'create-hook', 'scripts', 'recipes');

// Run a recipe the way a harness does: payload on stdin, then read exit code and stdout.
function run(script, payload, opts = {}) {
  const r = spawnSync('node', [join(recipes, script)], { input: typeof payload === 'string' ? payload : JSON.stringify(payload), encoding: 'utf8', timeout: 20000, ...opts });
  return interpret({ status: r.status, stdout: r.stdout ?? '', stderr: r.stderr ?? '' }, payload?.hook_event_name ?? 'PreToolUse');
}
const bash = (command) => buildPayload({ event: 'PreToolUse', tool: 'Bash', command, cwd: '/c' });

test('guard-bash: denies destructive commands, asks on force pushes, allows the rest', () => {
  assert.equal(run('guard-bash.mjs', bash('rm -rf /')).decision, 'block');
  assert.equal(run('guard-bash.mjs', bash('rm -rf ~/')).decision, 'block');
  assert.equal(run('guard-bash.mjs', bash('mkfs.ext4 /dev/sda1')).decision, 'block');
  assert.equal(run('guard-bash.mjs', bash('git push --force origin main')).decision, 'ask');
  assert.equal(run('guard-bash.mjs', bash('git reset --hard HEAD~1')).decision, 'ask');
  for (const c of ['rm -r -f /', 'rm -rf /*', 'sudo rm -rf $HOME', 'rm --recursive --force ~', 'cd x && rm -rf /']) assert.equal(run('guard-bash.mjs', bash(c)).decision, 'block', c);
  assert.equal(run('guard-bash.mjs', bash('rm -rf build')).decision, 'allow');
  assert.equal(run('guard-bash.mjs', bash('rm -rf ./node_modules')).decision, 'allow');
  assert.equal(run('guard-bash.mjs', bash('rm notes.txt')).decision, 'allow');
  assert.equal(run('guard-bash.mjs', bash('ls /')).decision, 'allow');
  assert.equal(run('guard-bash.mjs', bash('git push origin feature')).decision, 'allow');
});

test('every recipe fails open on unreadable input', () => {
  for (const s of ['guard-bash.mjs', 'protect-files.mjs', 'format-after-edit.mjs', 'stop-gate.mjs', 'session-context.mjs']) {
    assert.equal(run(s, 'not json').decision, 'allow', s);
    assert.equal(run(s, '').decision, 'allow', s);
  }
});

test('protect-files: denies generated and secret files, allows source files', () => {
  const write = (file) => buildPayload({ event: 'PreToolUse', tool: 'Write', filePath: file, cwd: '/c' });
  for (const f of ['package-lock.json', 'app/.env', 'app/.env.production', 'credentials.json', 'src/generated/api.ts']) assert.equal(run('protect-files.mjs', write(f)).decision, 'block', f);
  for (const f of ['src/a.ts', 'README.md', 'env.ts']) assert.equal(run('protect-files.mjs', write(f)).decision, 'allow', f);
});

test('stop-gate: blocks while tests fail, but never twice (stop_hook_active)', () => {
  const root = mkdtempSync(join(tmpdir(), 'stop-gate-'));
  try {
    const fail = join(root, 'fail');
    const ok = join(root, 'ok');
    mkdirSync(fail);
    mkdirSync(ok);
    writeFileSync(join(fail, 'package.json'), '{"name":"x","scripts":{"test":"echo boom >&2; exit 1"}}');
    writeFileSync(join(ok, 'package.json'), '{"name":"x","scripts":{"test":"exit 0"}}');
    const stop = (cwd, active) => ({ hook_event_name: 'Stop', cwd, stop_hook_active: active });
    const failing = run('stop-gate.mjs', stop(fail, false));
    assert.equal(failing.decision, 'block');
    assert.match(failing.reason, /boom/);
    assert.equal(run('stop-gate.mjs', stop(fail, true)).decision, 'allow');
    assert.equal(run('stop-gate.mjs', stop(ok, false)).decision, 'allow');
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('session-context: adds notes as additionalContext, and nothing when there is nothing to add', () => {
  const root = mkdtempSync(join(tmpdir(), 'session-ctx-'));
  try {
    const payload = { hook_event_name: 'SessionStart', cwd: root, source: 'startup' };
    assert.equal(run('session-context.mjs', payload).decision, 'allow');
    writeFileSync(join(root, '.agent-notes.md'), '- use pnpm\n');
    const r = run('session-context.mjs', payload);
    assert.equal(r.decision, 'context');
    assert.match(r.reason, /use pnpm/);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});
