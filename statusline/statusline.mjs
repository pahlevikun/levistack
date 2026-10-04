#!/usr/bin/env node
// levistack statusline: one line for Claude Code and the Cursor CLI agent.
// Reads the session JSON on stdin and prints the line. Self-contained (Node only, no dependencies),
// so the installer can copy this single file anywhere.
//
//   node statusline.mjs [--runtime=claude|cursor]
//
// Env: LEVISTACK_STATUSLINE_SEGMENTS  comma list to choose and order segments
//                                     (email,dir,branch,model,5h,1w,ctx)
//      LEVISTACK_EMAIL                show this account label (Cursor payloads carry none)
//      NO_COLOR / LEVISTACK_STATUSLINE_COLOR=0  disable ANSI colors
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { basename, join } from 'node:path';
import { fileURLToPath } from 'node:url';

export const DEFAULT_SEGMENTS = ['email', 'dir', 'branch', 'model', '5h', '1w', 'ctx'];
// Dropped first when the terminal is narrow. Model and context are kept longest.
const DROP_ORDER = ['email', '1w', '5h', 'dir', 'branch', 'ctx', 'model'];
const BAR_CELLS = 8;
const EFFORTS = ['low', 'medium', 'high', 'xhigh', 'max'];

const num = (v) => (typeof v === 'number' && Number.isFinite(v) ? v : null);
const str = (v) => (typeof v === 'string' && v.trim() ? v.trim() : null);

export function detectRuntime(p) {
  return 'autorun' in p || 'render_width_chars' in p || p.model?.param_summary !== undefined ? 'cursor' : 'claude';
}

function readEmail(runtime) {
  if (process.env.LEVISTACK_EMAIL) return process.env.LEVISTACK_EMAIL;
  if (runtime !== 'claude') return null;
  const dirs = [process.env.CLAUDE_CONFIG_DIR, homedir()].filter(Boolean);
  for (const d of dirs) {
    try {
      const cfg = JSON.parse(readFileSync(join(d, '.claude.json'), 'utf8'));
      const e = str(cfg?.oauthAccount?.emailAddress);
      if (e) return e;
    } catch {
      // try the next location
    }
  }
  return null;
}

function gitBranch(cwd) {
  const run = (args) =>
    execFileSync('git', ['--no-optional-locks', '-C', cwd, ...args], {
      timeout: 800,
      stdio: ['ignore', 'pipe', 'ignore'],
      encoding: 'utf8',
    }).trim();
  try {
    return run(['symbolic-ref', '--short', 'HEAD']) || null;
  } catch {
    try {
      return run(['rev-parse', '--short', 'HEAD']) || null;
    } catch {
      return null;
    }
  }
}

// Turn either runtime's payload into one shape. Anything a runtime does not provide stays null.
export function normalize(p, runtime = detectRuntime(p), deps = {}) {
  const cwd = str(p.workspace?.current_dir) ?? str(p.cwd) ?? process.cwd();
  const model = str(p.model?.display_name) ?? str(p.model?.id);
  let effort = null;
  let thinking = false;
  let max = false;
  if (runtime === 'cursor') {
    const summary = str(p.model?.param_summary) ?? '';
    thinking = /thinking/i.test(summary);
    effort = summary.match(/\b(low|medium|high|xhigh|max)\b/i)?.[1]?.toLowerCase() ?? null;
    max = p.model?.max_mode === true;
  } else {
    const lvl = str(p.effort?.level)?.toLowerCase();
    effort = EFFORTS.includes(lvl) ? lvl : null;
    thinking = p.thinking?.enabled === true;
  }
  return {
    runtime,
    cwd,
    email: (deps.email ?? readEmail)(runtime),
    dir: basename(cwd) || cwd,
    branch: (deps.branch ?? gitBranch)(cwd),
    model,
    effort,
    thinking,
    max,
    fiveHour: num(p.rate_limits?.five_hour?.used_percentage),
    sevenDay: num(p.rate_limits?.seven_day?.used_percentage),
    ctx: num(p.context_window?.used_percentage),
    width: num(p.render_width_chars),
  };
}

function painter(color) {
  const wrap = (code) => (s) => (color ? `\x1b[${code}m${s}\x1b[0m` : s);
  return {
    dim: wrap('90'),
    blue: wrap('94'),
    boldBlue: wrap('1;34'),
    green: wrap('32'),
    yellow: wrap('33'),
    red: wrap('31'),
    magenta: wrap('35'),
    boldCyan: wrap('1;36'),
    brightRed: wrap('91'),
  };
}

const gaugeColor = (pct) => (pct >= 85 ? 'red' : pct >= 60 ? 'yellow' : 'green');
const effortColor = { low: 'green', medium: 'yellow', high: 'magenta', xhigh: 'brightRed', max: 'red' };

function gauge(c, label, pct) {
  const clamped = Math.max(0, Math.min(100, pct));
  const filled = Math.round((clamped / 100) * BAR_CELLS);
  const bar = '▰'.repeat(filled) + '▱'.repeat(BAR_CELLS - filled);
  return `${label} ${c[gaugeColor(clamped)](`${bar} ${Math.round(clamped)}%`)}`;
}

export function segments(n, c) {
  const out = {};
  if (n.email) out.email = c.blue(n.email);
  if (n.dir) out.dir = c.boldBlue(n.dir);
  if (n.branch) out.branch = c.green(n.branch);
  if (n.model) {
    const parts = [c.boldCyan(n.model)];
    if (n.max) parts.push(c.yellow('Max'));
    if (n.effort) parts.push(c[effortColor[n.effort]](n.effort[0].toUpperCase() + n.effort.slice(1)));
    if (n.thinking) parts.push(c.magenta('Thinking'));
    out.model = parts.join(' ');
  }
  if (n.fiveHour !== null) out['5h'] = gauge(c, '5h', n.fiveHour);
  if (n.sevenDay !== null) out['1w'] = gauge(c, '1w', n.sevenDay);
  if (n.ctx !== null) out.ctx = gauge(c, 'ctx', n.ctx);
  return out;
}

const visibleLength = (s) => s.replace(/\x1b\[[0-9;]*m/g, '').length;

export function render(payload, opts = {}) {
  const color = opts.color ?? (!process.env.NO_COLOR && process.env.LEVISTACK_STATUSLINE_COLOR !== '0');
  const c = painter(color);
  const n = normalize(payload, opts.runtime, opts.deps);
  const available = segments(n, c);
  const wanted = (opts.segments ?? DEFAULT_SEGMENTS).filter((id) => available[id]);
  const sep = c.dim(' | ');
  const width = opts.width ?? n.width ?? Number(process.env.COLUMNS) ?? Infinity;
  const build = (ids) => ids.map((id) => available[id]).join(sep);

  let ids = [...wanted];
  for (const drop of DROP_ORDER) {
    if (!Number.isFinite(width) || width <= 0 || visibleLength(build(ids)) <= width) break;
    if (ids.length > 1) ids = ids.filter((id) => id !== drop);
  }
  return build(ids);
}

function parseArgs(argv) {
  const out = { runtime: null };
  for (const a of argv) if (a.startsWith('--runtime=')) out.runtime = a.slice('--runtime='.length);
  if (!['claude', 'cursor'].includes(out.runtime)) out.runtime = null;
  return out;
}

async function main() {
  try {
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    const raw = Buffer.concat(chunks).toString('utf8').trim();
    const payload = raw ? JSON.parse(raw) : {};
    const { runtime } = parseArgs(process.argv.slice(2));
    const segs = process.env.LEVISTACK_STATUSLINE_SEGMENTS?.split(',').map((s) => s.trim()).filter(Boolean);
    const line = render(payload && typeof payload === 'object' ? payload : {}, {
      runtime: runtime ?? undefined,
      segments: segs?.length ? segs : undefined,
    });
    if (line) process.stdout.write(line);
  } catch {
    // never fail the host: print nothing and exit 0
  }
  process.exit(0);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) await main();
