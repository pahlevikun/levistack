#!/usr/bin/env node
// PostToolUse on Edit|Write: format the file that was just written, by extension.
// Never blocks: a missing formatter or a formatter error is ignored.
import { readFileSync } from 'node:fs';
import { extname } from 'node:path';
import { spawnSync } from 'node:child_process';

const FORMATTERS = {
  '.ts': ['npx', '--no-install', 'prettier', '--write'],
  '.tsx': ['npx', '--no-install', 'prettier', '--write'],
  '.js': ['npx', '--no-install', 'prettier', '--write'],
  '.json': ['npx', '--no-install', 'prettier', '--write'],
  '.py': ['black', '--quiet'],
  '.go': ['gofmt', '-w'],
};

try {
  const file = JSON.parse(readFileSync(0, 'utf8')).tool_input?.file_path;
  const cmd = file && FORMATTERS[extname(file)];
  if (cmd) spawnSync(cmd[0], [...cmd.slice(1), file], { stdio: 'ignore', timeout: 8000 });
} catch {
  // ignore
}
