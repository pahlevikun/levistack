#!/usr/bin/env node
// Stop: keep the agent working while the test command fails. Checks stop_hook_active so it cannot loop.
import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';

const TEST = ['npm', ['test', '--silent']];

try {
  const input = JSON.parse(readFileSync(0, 'utf8'));
  if (input.stop_hook_active) process.exit(0); // already pushed once; let it stop
  const r = spawnSync(TEST[0], TEST[1], { cwd: input.cwd, encoding: 'utf8', timeout: 90000 });
  if (r.status !== 0 && r.status !== null) {
    const tail = `${r.stdout ?? ''}${r.stderr ?? ''}`.trim().split('\n').slice(-15).join('\n');
    console.log(JSON.stringify({ decision: 'block', reason: `Tests are failing. Fix them before stopping.\n${tail}` }));
  }
} catch {
  // allow stop
}
