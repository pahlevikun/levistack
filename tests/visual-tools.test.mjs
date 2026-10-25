import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const hasPython = spawnSync('python3', ['--version'], { encoding: 'utf8' }).status === 0;

for (const path of ['skills/product/diagram/scripts', 'skills/product/infographic/scripts']) {
  test(`${path}: native and rendered artifact checks`, { skip: !hasPython && 'python3 not found' }, () => {
    const result = spawnSync('python3', ['-I', '-B', '-m', 'unittest', 'discover', '-s', path, '-p', 'test_*.py', '-v'], {
      cwd: root,
      encoding: 'utf8',
    });
    assert.equal(result.status, 0, result.stdout + result.stderr);
  });
}
