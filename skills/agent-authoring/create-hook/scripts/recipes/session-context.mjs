#!/usr/bin/env node
// SessionStart: inject the current branch and the contents of a short local notes file.
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

try {
  const { cwd } = JSON.parse(readFileSync(0, 'utf8'));
  const branch = spawnSync('git', ['branch', '--show-current'], { cwd, encoding: 'utf8' }).stdout?.trim();
  const notesPath = join(cwd, '.agent-notes.md');
  const notes = existsSync(notesPath) ? readFileSync(notesPath, 'utf8').slice(0, 4000) : '';
  const parts = [branch && `Current branch: ${branch}`, notes].filter(Boolean);
  if (parts.length) console.log(JSON.stringify({ hookSpecificOutput: { hookEventName: 'SessionStart', additionalContext: parts.join('\n\n') } }));
} catch {
  // add nothing
}
