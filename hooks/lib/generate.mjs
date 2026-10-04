#!/usr/bin/env node
// Generates hooks/hooks.json and the table in hooks/README.md from each hook's `meta`.
// Run through `npm run sync` (which also runs `--check` in CI).
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { EVENT_ORDER, loadHooks } from './registry.mjs';

const START = '<!-- hooks:start -->';
const END = '<!-- hooks:end -->';
const json = (o) => JSON.stringify(o, null, 2) + '\n';

const eventRank = (e) => (EVENT_ORDER.includes(e) ? EVENT_ORDER.indexOf(e) : EVENT_ORDER.length);

export async function buildHookFiles(root) {
  const hooks = await loadHooks(join(root, 'hooks'));
  const problems = hooks.flatMap((h) => h.problems.map((p) => `hooks/${h.name}.mjs: ${p}`));
  if (problems.length) throw new Error(problems.join('\n'));

  // Only opt-in plugin hooks are wired; `meta.optIn = false` hooks are for projects to wire themselves.
  const wired = hooks.filter((h) => h.meta.optIn !== false);
  const byEvent = {};
  for (const h of [...wired].sort((a, b) => eventRank(a.meta.event) - eventRank(b.meta.event) || a.name.localeCompare(b.name))) {
    const entry = { ...(h.meta.matcher ? { matcher: h.meta.matcher } : {}), hooks: [{ type: 'command', command: `node "\${CLAUDE_PLUGIN_ROOT}/hooks/lib/launcher.mjs" ${h.name}`, ...(h.meta.timeout ? { timeout: h.meta.timeout } : {}) }] };
    (byEvent[h.meta.event] ??= []).push(entry);
  }
  const out = new Map([['hooks/hooks.json', json({ hooks: byEvent })]]);

  const readmePath = join(root, 'hooks/README.md');
  if (existsSync(readmePath)) {
    const readme = readFileSync(readmePath, 'utf8');
    const a = readme.indexOf(START);
    const b = readme.indexOf(END);
    if (a !== -1 && b > a) {
      const cell = (s) => s.replace(/\|/g, '\\|');
      const rows = hooks.map((h) => `| \`${h.name}\` | \`${h.meta.event}\`${h.meta.matcher ? ` (${cell(h.meta.matcher)})` : ''} | ${cell(h.meta.description)} |`);
      const table = ['| Hook | Claude Code event | What it does |', '|---|---|---|', ...rows].join('\n');
      out.set('hooks/README.md', `${readme.slice(0, a + START.length)}\n${table}\n${readme.slice(b)}`);
    }
  }
  return out;
}

// Human-readable drift lines; empty when hooks/ is in sync.
export async function diffHooks(root) {
  const drift = [];
  for (const [rel, content] of await buildHookFiles(root)) {
    const p = join(root, rel);
    if (!existsSync(p)) drift.push(`missing: ${rel}`);
    else if (readFileSync(p, 'utf8') !== content) drift.push(`out of date: ${rel}`);
  }
  return drift;
}

export async function writeHooks(root) {
  const out = await buildHookFiles(root);
  for (const [rel, content] of out) writeFileSync(join(root, rel), content);
  return out;
}

const root = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  if (process.argv.includes('--check')) {
    const drift = await diffHooks(root);
    if (drift.length) {
      console.error(`Hook files are out of sync. Run \`npm run sync\`.\n${drift.map((d) => `  ${d}`).join('\n')}`);
      process.exit(1);
    }
    console.log('hooks: up to date');
  } else {
    const out = await writeHooks(root);
    console.log(`hooks: wrote ${out.size} files`);
  }
}
