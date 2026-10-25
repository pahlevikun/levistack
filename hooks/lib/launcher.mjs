#!/usr/bin/env node
// Single entry for every levistack hook: `node launcher.mjs [--runtime=claude|cursor] <hook-name> [args...]`.
// Opt-in: does nothing unless ~/.levistack/<hook-name>.on exists (unless the hook sets `meta.optIn = false`).
// Fail-open: any error exits 0, so a broken hook never breaks a session.
import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { levistackHome } from './files.mjs';
import { normalize } from './input.mjs';
import { resolveHook } from './registry.mjs';
import { render, RUNTIMES, toResult } from './result.mjs';

const hooksDir = join(dirname(fileURLToPath(import.meta.url)), '..');
const root = process.env.CLAUDE_PLUGIN_ROOT || process.env.PLUGIN_ROOT || join(hooksDir, '..');

function parseArgs(argv) {
  const out = { runtime: process.env.LEVISTACK_RUNTIME || 'claude', name: '', args: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--runtime=')) out.runtime = a.slice('--runtime='.length);
    else if (a === '--runtime') out.runtime = argv[++i] ?? out.runtime;
    else if (!out.name) out.name = a;
    else out.args.push(a);
  }
  if (!RUNTIMES.includes(out.runtime)) out.runtime = 'claude';
  return out;
}

async function readStdin() {
  if (process.stdin.isTTY) return '';
  const chunks = [];
  for await (const c of process.stdin) chunks.push(c);
  return Buffer.concat(chunks).toString('utf8');
}

function parseJson(text) {
  try {
    return JSON.parse(text);
  } catch {
    return {};
  }
}

let exitCode = 0;
try {
  const { runtime, name, args } = parseArgs(process.argv.slice(2));
  const file = resolveHook(hooksDir, name);
  if (file) {
    const mod = await import(pathToFileURL(file).href);
    const optedIn = mod.meta?.optIn === false || existsSync(join(levistackHome(), `${name}.on`));
    if (optedIn) {
      const rawStdin = await readStdin();
      const input = normalize(parseJson(rawStdin));
      const event = input.event || mod.meta?.event;
      const result = toResult(await mod.default({ input, root, args, rawStdin, runtime, event }));
      const out = render(result, { runtime, event });
      if (out.stderr) process.stderr.write(out.stderr);
      if (out.stdout) process.stdout.write(out.stdout);
      exitCode = out.exitCode;
    }
  }
} catch {
  exitCode = 0;
}
process.exit(exitCode);
