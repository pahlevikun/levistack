import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const kit = join(root, 'skills', 'product', 'design-system-kit', 'specialities', 'design-system');

const python = spawnSync('python3', ['--version'], { encoding: 'utf8' });
const hasPython = python.status === 0;

test('design-system theme builder: python tests pass', { skip: !hasPython && 'python3 not found' }, () => {
  const r = spawnSync('python3', ['-I', '-B', '-m', 'unittest', 'discover', '-s', 'scripts/tests', '-p', 'test_theme*.py'], { cwd: kit, encoding: 'utf8' });
  assert.equal(r.status, 0, r.stdout + r.stderr);
});

test('design-system theme CLI: explore lists directions', { skip: !hasPython && 'python3 not found' }, () => {
  const r = spawnSync('python3', ['-I', '-B', join(kit, 'scripts', 'theme', 'theme.py'), 'explore', '--brief', 'a calming meditation app', '--count', '3'], { cwd: kit, encoding: 'utf8' });
  assert.equal(r.status, 0, r.stdout + r.stderr);
  assert.match(r.stdout, /^3\. /m);
});
