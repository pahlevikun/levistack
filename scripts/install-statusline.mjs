#!/usr/bin/env node
// Install the levistack status line into Claude Code, the Cursor CLI agent and Codex.
//
//   node scripts/install-statusline.mjs [--runtime=claude,cursor,codex|all] [--dry-run] [--force] [--uninstall]
//
// - Claude Code: `statusLine` in settings.json            (custom command)
// - Cursor CLI:  `statusLine` in cli-config.json           (custom command)
// - Codex:       `[tui].status_line` in config.toml        (built-in items only; Codex has no custom command)
//
// Safe by default: merges into existing config, keeps a timestamped backup, and will not replace a
// status line it did not write unless --force is given.
import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const MARKER = '# managed by levistack: statusline';
// Closest built-in Codex items to the levistack layout. Every id is present in codex-cli 0.154.0.
// Codex cannot show the account email or a custom label.
export const CODEX_ITEMS = ['current-dir', 'git-branch', 'model-with-reasoning', 'context-used', 'five-hour-limit', 'weekly-limit'];
export const RUNTIMES = ['claude', 'cursor', 'codex'];

export function paths(env = process.env) {
  const home = homedir();
  return {
    levistackHome: env.LEVISTACK_HOME || join(home, '.levistack'),
    claude: join(env.CLAUDE_CONFIG_DIR || join(home, '.claude'), 'settings.json'),
    cursor: join(env.CURSOR_CONFIG_DIR || join(home, '.cursor'), 'cli-config.json'),
    codex: join(env.CODEX_HOME || join(home, '.codex'), 'config.toml'),
  };
}

const quote = (p) => (/^[\w./@+:-]+$/.test(p) ? p : JSON.stringify(p));
export const commandFor = (script, runtime) => `node ${quote(script)} --runtime=${runtime}`;
export const isOurs = (cmd) => typeof cmd === 'string' && /levistack/.test(cmd) && /statusline\.mjs/.test(cmd);

const stamp = () => new Date().toISOString().replace(/[-:T]/g, '').slice(0, 14);

function backup(file) {
  const dest = `${file}.levistack-${stamp()}.bak`;
  copyFileSync(file, dest);
  return dest;
}

// ---- TOML (just enough to own one key under [tui]) -------------------------------------------

const tomlArray = (items) => `status_line = [${items.map((i) => JSON.stringify(i)).join(', ')}]`;

// Index range [from, to) of the status_line assignment inside [tui], including a multi-line array.
function findStatusLine(lines) {
  const start = lines.findIndex((l) => /^\s*\[tui\]\s*(#.*)?$/.test(l));
  if (start === -1) return { tui: -1 };
  let end = lines.length;
  for (let i = start + 1; i < lines.length; i++) {
    if (/^\s*\[/.test(lines[i])) {
      end = i;
      break;
    }
  }
  for (let i = start + 1; i < end; i++) {
    if (!/^\s*status_line\s*=/.test(lines[i])) continue;
    let to = i + 1;
    const depth = (s) => (s.match(/\[/g) || []).length - (s.match(/\]/g) || []).length;
    let open = depth(lines[i].replace(/^[^=]*=/, ''));
    while (open > 0 && to < end) open += depth(lines[to++]);
    const hasMarker = i > 0 && lines[i - 1].trim() === MARKER;
    return { tui: start, from: hasMarker ? i - 1 : i, to, owned: hasMarker, current: lines.slice(i, to).join('\n') };
  }
  return { tui: start, end };
}

export function setTomlStatusLine(text, items, { force = false } = {}) {
  if (/^\s*tui\s*\.\s*status_line\s*=/m.test(text) || /^\s*tui\s*=\s*\{/m.test(text)) {
    return { error: 'config uses a dotted or inline `tui` form; edit status_line by hand' };
  }
  const lines = text.split('\n');
  const found = findStatusLine(lines);
  const block = [MARKER, tomlArray(items)];
  if (found.tui === -1) {
    const base = text.length && !text.endsWith('\n') ? `${text}\n` : text;
    return { text: `${base}${base.length ? '\n' : ''}[tui]\n${block.join('\n')}\n`, changed: true };
  }
  if (found.from === undefined) {
    lines.splice(found.tui + 1, 0, ...block);
    return { text: lines.join('\n'), changed: true };
  }
  if (!found.owned && !force) return { skipped: `existing status_line is not managed by levistack: ${found.current}` };
  const before = lines.slice(found.from, found.to).join('\n');
  lines.splice(found.from, found.to - found.from, ...block);
  const next = lines.join('\n');
  return { text: next, changed: before !== block.join('\n') };
}

export function removeTomlStatusLine(text) {
  const lines = text.split('\n');
  const found = findStatusLine(lines);
  if (found.from === undefined || !found.owned) return { changed: false, text };
  lines.splice(found.from, found.to - found.from);
  return { text: lines.join('\n'), changed: true };
}

// ---- JSON runtimes ---------------------------------------------------------------------------

function readJson(file) {
  if (!existsSync(file)) return { cfg: {}, existed: false };
  return { cfg: JSON.parse(readFileSync(file, 'utf8') || '{}'), existed: true };
}

function installJson(runtime, file, script, opts) {
  let parsed;
  try {
    parsed = readJson(file);
  } catch (e) {
    return { runtime, file, status: 'error', note: `invalid JSON (${e.message}); not touched` };
  }
  const { cfg, existed } = parsed;
  const desired = { type: 'command', command: commandFor(script, runtime) };
  const current = cfg.statusLine;
  if (opts.uninstall) {
    if (!current) return { runtime, file, status: 'unchanged', note: 'no statusLine set' };
    if (!isOurs(current.command)) return { runtime, file, status: 'skipped', note: 'statusLine is not levistack\'s; left alone' };
    if (!opts.dryRun) {
      const b = backup(file);
      delete cfg.statusLine;
      writeFileSync(file, `${JSON.stringify(cfg, null, 2)}\n`);
      return { runtime, file, status: 'removed', note: `backup: ${b}` };
    }
    return { runtime, file, status: 'removed', note: 'dry run' };
  }
  if (current && !isOurs(current.command) && !opts.force) {
    return { runtime, file, status: 'skipped', note: `existing statusLine (${String(current.command).slice(0, 60)}...) kept; pass --force to replace it` };
  }
  if (current && JSON.stringify(current) === JSON.stringify(desired)) {
    return { runtime, file, status: 'unchanged', note: 'already installed' };
  }
  if (opts.dryRun) return { runtime, file, status: 'would-install', note: desired.command };
  mkdirSync(dirname(file), { recursive: true });
  const b = existed ? backup(file) : null;
  writeFileSync(file, `${JSON.stringify({ ...cfg, statusLine: { ...desired, ...(current && isOurs(current.command) ? { padding: current.padding } : {}) } }, null, 2)}\n`);
  return { runtime, file, status: 'installed', note: b ? `backup: ${b}` : 'created' };
}

function installCodex(file, opts) {
  const existed = existsSync(file);
  const text = existed ? readFileSync(file, 'utf8') : '';
  if (opts.uninstall) {
    const r = removeTomlStatusLine(text);
    if (!r.changed) return { runtime: 'codex', file, status: 'unchanged', note: 'nothing managed by levistack' };
    if (opts.dryRun) return { runtime: 'codex', file, status: 'removed', note: 'dry run' };
    const b = backup(file);
    writeFileSync(file, r.text);
    return { runtime: 'codex', file, status: 'removed', note: `backup: ${b}` };
  }
  const r = setTomlStatusLine(text, CODEX_ITEMS, { force: opts.force });
  if (r.error) return { runtime: 'codex', file, status: 'error', note: r.error };
  if (r.skipped) return { runtime: 'codex', file, status: 'skipped', note: `${r.skipped}. Pass --force to replace it` };
  if (!r.changed) return { runtime: 'codex', file, status: 'unchanged', note: 'already installed' };
  if (opts.dryRun) return { runtime: 'codex', file, status: 'would-install', note: `[tui] ${tomlArray(CODEX_ITEMS)}` };
  mkdirSync(dirname(file), { recursive: true });
  const b = existed ? backup(file) : null;
  writeFileSync(file, r.text);
  return { runtime: 'codex', file, status: 'installed', note: b ? `backup: ${b}` : 'created' };
}

export function install(opts = {}) {
  const env = opts.env ?? process.env;
  const p = paths(env);
  const requested = opts.runtimes?.length ? opts.runtimes : null;
  const script = join(p.levistackHome, 'statusline.mjs');
  const results = [];

  const present = (runtime) => existsSync(dirname(p[runtime]));
  const targets = requested ?? RUNTIMES.filter(present);
  if (!targets.length) return [{ runtime: '-', status: 'skipped', note: 'no supported tool config directory found' }];

  if (!opts.uninstall && !opts.dryRun) {
    mkdirSync(p.levistackHome, { recursive: true });
    copyFileSync(join(here, '..', 'statusline', 'statusline.mjs'), script);
  }
  for (const runtime of targets) {
    if (!RUNTIMES.includes(runtime)) {
      results.push({ runtime, status: 'error', note: 'unknown runtime' });
      continue;
    }
    results.push(runtime === 'codex' ? installCodex(p.codex, opts) : installJson(runtime, p[runtime], script, opts));
  }
  return results;
}

function parseArgs(argv) {
  const o = { runtimes: [], dryRun: false, force: false, uninstall: false };
  for (const a of argv) {
    if (a === '--dry-run') o.dryRun = true;
    else if (a === '--force') o.force = true;
    else if (a === '--uninstall') o.uninstall = true;
    else if (a.startsWith('--runtime=')) {
      const v = a.slice('--runtime='.length);
      o.runtimes = v === 'all' ? [...RUNTIMES] : v.split(',').map((s) => s.trim()).filter(Boolean);
    }
  }
  return o;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const opts = parseArgs(process.argv.slice(2));
  const results = install(opts);
  for (const r of results) console.log(`${r.runtime.padEnd(7)} ${r.status.padEnd(13)} ${r.file ?? ''}\n        ${r.note}`);
  if (results.some((r) => r.status === 'error')) process.exitCode = 1;
}
