#!/usr/bin/env node
// Local collector for the daily standup skill. Read-only, no network, no npm deps.
// Browser history needs the `sqlite3` CLI (preinstalled on macOS, `apt install sqlite3` on Linux).
//
//   node collect.mjs range   [--today YYYY-MM-DD]
//   node collect.mjs machine --start YYYY-MM-DD --end YYYY-MM-DD [--sources shell,git,ai] [--repos dir,dir] [--author x]
//   node collect.mjs browser --start YYYY-MM-DD --end YYYY-MM-DD [--domains a.com,*.b.com] [--include-all]
//
// Add --json for structured output. Defaults come from a JSON config file, first hit wins:
//   --config <path> | $STANDUP_CONFIG | ~/.config/standup/config.json
// Keys read here: workdays (ISO 1-7), holidays (YYYY-MM-DD[]), repoRoots, gitAuthor, workDomains.
import { execFileSync } from 'node:child_process';
import { copyFileSync, existsSync, mkdtempSync, readdirSync, readFileSync, rmSync, statSync } from 'node:fs';
import { homedir, platform, tmpdir } from 'node:os';
import { basename, join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';

const DAY_MS = 86400000;
const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const pad = (n) => String(n).padStart(2, '0');

// ---------------------------------------------------------------- dates

function parseDay(s) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s ?? '');
  if (!m) throw new Error(`expected YYYY-MM-DD, got "${s}"`);
  return Date.UTC(+m[1], +m[2] - 1, +m[3]);
}
const addDays = (s, n) => new Date(parseDay(s) + n * DAY_MS).toISOString().slice(0, 10);
const isoWeekday = (s) => new Date(parseDay(s)).getUTCDay() || 7;
const weekdayName = (s) => WEEKDAYS[new Date(parseDay(s)).getUTCDay()];
export function localToday() {
  const d = new Date();
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

/** Wall-clock `day` + `hms` in the machine's timezone -> ISO string with offset and unix seconds. */
export function localTime(day, hms) {
  const [y, m, d] = day.split('-').map(Number);
  const [h, mi, s] = hms.split(':').map(Number);
  const dt = new Date(y, m - 1, d, h, mi, s);
  const off = -dt.getTimezoneOffset();
  const a = Math.abs(off);
  return { iso: `${day}T${hms}${off < 0 ? '-' : '+'}${pad(Math.floor(a / 60))}:${pad(a % 60)}`, ts: Math.floor(dt.getTime() / 1000) };
}

/**
 * The reporting window: from the last working day before `today` through yesterday.
 * Tue-Fri -> yesterday. Monday -> Fri..Sun. After a holiday -> back over the holiday to the last working day.
 */
export function dayRange({ today = localToday(), workdays = [1, 2, 3, 4, 5], holidays = [] } = {}) {
  const off = new Set(holidays);
  const working = (d) => workdays.includes(isoWeekday(d)) && !off.has(d);
  const end = addDays(today, -1);
  let start = end;
  for (let d = end, i = 0; i < 31; i++, d = addDays(d, -1)) {
    if (working(d)) { start = d; break; }
  }
  const days = [];
  for (let d = start; d <= end; d = addDays(d, 1)) days.push({ date: d, weekday: weekdayName(d), working: working(d) });
  const label = start === end ? `yesterday (${end})` : `${weekdayName(start)} ${start} – ${weekdayName(end)} ${end}`;
  const from = localTime(start, '00:00:00');
  const to = localTime(end, '23:59:59');
  return { today, start, end, label, days, startIso: from.iso, endIso: to.iso, startTs: from.ts, endTs: to.ts, tz: from.iso.slice(-6) };
}

const fmtTime = (ts) => {
  const d = new Date(ts * 1000);
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
};
const clip = (s, n) => (s.length > n ? `${s.slice(0, n - 1)}…` : s);

// ---------------------------------------------------------------- config

const expand = (p) => (typeof p === 'string' && (p === '~' || p.startsWith('~/')) ? join(homedir(), p.slice(1)) : p);

export function loadConfig(path) {
  const file = path || process.env.STANDUP_CONFIG || join(homedir(), '.config/standup/config.json');
  if (!existsSync(file)) return {};
  try {
    return JSON.parse(readFileSync(file, 'utf8'));
  } catch (e) {
    throw new Error(`config ${file} is not valid JSON: ${e.message}`);
  }
}

// ---------------------------------------------------------------- shell history

const SECRET_RE = new RegExp([
  '(token|secret|passw(or)?d|api[_-]?key|authorization|bearer|credential|private[_-]?key|aws_)',
  '(^|\\s)-u\\s+\\S+:\\S+',
  '\\b(?=[A-Za-z0-9_-]*[A-Za-z])(?=[A-Za-z0-9_-]*\\d)(?![0-9a-f]{32,}\\b)[A-Za-z0-9_-]{32,}\\b',
].join('|'), 'i');
export const looksSecret = (s) => SECRET_RE.test(s);

const NOISE = new Set(['ls', 'll', 'la', 'cd', 'pwd', 'clear', 'exit', 'history', 'which', 'whoami', 'man', 'z', 'open', 'echo', 'cat', 'less', 'true']);
const SUBCOMMAND_TOOLS = new Set(['git', 'npm', 'pnpm', 'yarn', 'docker', 'kubectl', 'gh', 'glab', 'go', 'cargo', 'make', 'terraform', 'brew', 'pip', 'helm']);

/** Zsh extended history, bash with HISTTIMEFORMAT, and fish. Untimed lines are counted, not returned. */
export function parseShellHistory(text) {
  const entries = [];
  let untimed = 0;
  if (/^- cmd: /m.test(text)) {
    let cmd = null;
    for (const line of text.split('\n')) {
      let m;
      if ((m = /^- cmd: (.*)$/.exec(line))) cmd = m[1];
      else if (cmd !== null && (m = /^\s+when: (\d+)/.exec(line))) { entries.push({ ts: +m[1], cmd }); cmd = null; }
    }
    return { entries, untimed };
  }
  let cur = null;
  let pending = null;
  for (const line of text.split('\n')) {
    let m;
    if ((m = /^: (\d+):\d+;(.*)$/.exec(line))) { cur = { ts: +m[1], cmd: m[2] }; entries.push(cur); }
    else if (cur && cur.cmd.endsWith('\\')) cur.cmd = `${cur.cmd.slice(0, -1)}\n${line}`;
    else if ((m = /^#(\d{9,})$/.exec(line))) { pending = +m[1]; cur = null; }
    else if (pending !== null && line.trim()) { entries.push({ ts: pending, cmd: line }); pending = null; }
    else if (line.trim()) untimed++;
  }
  return { entries, untimed };
}

export function toolOf(cmd) {
  const words = cmd.trim().split(/\s+/);
  let i = 0;
  while (i < words.length && (/^[A-Za-z_][A-Za-z0-9_]*=/.test(words[i]) || ['sudo', 'time', 'command', 'env', 'nohup'].includes(words[i]))) i++;
  if (!words[i]) return null;
  const bin = words[i].split('/').pop();
  const sub = words[i + 1];
  return SUBCOMMAND_TOOLS.has(bin) && sub && !sub.startsWith('-') ? `${bin} ${sub}` : bin;
}

export function summarizeShell(entries, { startTs, endTs, limit = 60 }) {
  const inRange = entries.filter((e) => e.ts >= startTs && e.ts <= endTs);
  const counts = new Map();
  const seen = new Set();
  const commands = [];
  let redacted = 0;
  for (const e of inRange) {
    const cmd = e.cmd.trim();
    if (!cmd) continue;
    if (looksSecret(cmd)) { redacted++; continue; }
    const tool = toolOf(cmd);
    if (!tool || NOISE.has(tool)) continue;
    counts.set(tool, (counts.get(tool) ?? 0) + 1);
    if (!seen.has(cmd)) { seen.add(cmd); commands.push({ ts: e.ts, cmd: clip(cmd.replace(/\n/g, ' ⏎ '), 160) }); }
  }
  const tools = [...counts].sort((a, b) => b[1] - a[1]).slice(0, 15).map(([tool, count]) => ({ tool, count }));
  return { inRange: inRange.length, redacted, tools, commands: commands.slice(0, limit), truncated: Math.max(0, commands.length - limit) };
}

function shellHistoryFiles(home) {
  const candidates = [process.env.HISTFILE, join(home, '.zsh_history'), join(home, '.bash_history'), join(home, '.local/share/fish/fish_history')];
  return [...new Set(candidates.filter((f) => f && existsSync(f)))];
}

function collectShell({ startTs, endTs, home }) {
  const files = shellHistoryFiles(home);
  if (!files.length) return { error: 'no shell history file found' };
  const out = { files: files.map((f) => basename(f)), total: 0, untimed: 0, inRange: 0, redacted: 0, tools: [], commands: [], truncated: 0 };
  const all = [];
  for (const f of files) {
    const { entries, untimed } = parseShellHistory(readFileSync(f, 'utf8'));
    out.total += entries.length;
    out.untimed += untimed;
    all.push(...entries);
  }
  all.sort((a, b) => a.ts - b.ts);
  Object.assign(out, summarizeShell(all, { startTs, endTs }));
  if (!out.total && out.untimed) out.error = 'history has no timestamps; for zsh run `setopt EXTENDED_HISTORY`, for bash set HISTTIMEFORMAT';
  return out;
}

// ---------------------------------------------------------------- git

function git(args, cwd) {
  return execFileSync('git', args, { cwd, encoding: 'utf8', timeout: 15000, stdio: ['ignore', 'pipe', 'ignore'], maxBuffer: 32 * 1024 * 1024 });
}

const SKIP_DIRS = new Set(['node_modules', 'vendor', 'Library', 'target', 'dist', 'build']);
export function findRepos(roots, depth = 3, cap = 200) {
  const repos = [];
  const walk = (dir, left) => {
    if (repos.length >= cap) return;
    if (existsSync(join(dir, '.git'))) { repos.push(dir); return; }
    if (left === 0) return;
    let names;
    try { names = readdirSync(dir, { withFileTypes: true }); } catch { return; }
    for (const e of names) {
      if (e.isDirectory() && !e.name.startsWith('.') && !SKIP_DIRS.has(e.name)) walk(join(dir, e.name), left - 1);
    }
  };
  for (const r of roots) if (existsSync(r)) walk(r, depth);
  return repos;
}

function gitAuthors(configured) {
  if (configured) return [configured];
  const get = (k) => { try { return git(['config', '--global', k]).trim(); } catch { return ''; } };
  return [get('user.email'), get('user.name')].filter(Boolean);
}

function collectGit({ start, end, startTs, endTs, roots, author }) {
  const repos = findRepos(roots);
  const authors = gitAuthors(author);
  if (!authors.length) return { error: 'no git author: set gitAuthor in the config or `git config --global user.name`' };
  const seenHashes = new Set();
  const out = [];
  for (const repo of repos) {
    const args = ['log', '--all', '--no-merges', '--date-order', `--since=${start}T00:00:00`, `--until=${end}T23:59:59`, '--pretty=format:%h%x09%at%x09%s'];
    for (const a of authors) args.push(`--author=${a}`);
    let commits = [];
    try {
      commits = git(args, repo).split('\n').filter(Boolean).map((l) => {
        const [hash, at, ...subject] = l.split('\t');
        return { hash, ts: +at, subject: subject.join('\t') };
      }).filter((c) => !seenHashes.has(c.hash) && seenHashes.add(c.hash));
    } catch { /* unreadable repo: skip */ }
    let dirty = [];
    try {
      dirty = git(['status', '--porcelain'], repo).split('\n').filter(Boolean).map((l) => l.slice(3)).filter((p) => {
        try { const t = statSync(join(repo, p)).mtimeMs / 1000; return t >= startTs && t <= endTs; } catch { return false; }
      });
    } catch { /* skip */ }
    if (commits.length || dirty.length) out.push({ repo: basename(repo), commits, dirty: dirty.slice(0, 10), dirtyCount: dirty.length });
  }
  return { scanned: repos.length, authors, repos: out };
}

// ---------------------------------------------------------------- AI coding sessions (Claude Code transcripts)

function promptText(msg) {
  const c = msg?.content;
  if (typeof c === 'string') return c;
  if (Array.isArray(c)) return c.filter((b) => b?.type === 'text').map((b) => b.text).join(' ');
  return '';
}

export function parseSessionLines(lines, { startTs, endTs }) {
  const prompts = [];
  let cwd = null;
  for (const line of lines) {
    let o;
    try { o = JSON.parse(line); } catch { continue; }
    if (o.cwd) cwd = o.cwd;
    if (o.type !== 'user' || o.isSidechain || o.isMeta) continue;
    const ts = Date.parse(o.timestamp) / 1000;
    if (!(ts >= startTs && ts <= endTs)) continue;
    const text = promptText(o.message).trim();
    if (!text || text.startsWith('<') || text.startsWith('Caveat:')) continue;
    prompts.push(looksSecret(text) ? '[redacted]' : clip(text.replace(/\s+/g, ' '), 140));
  }
  return { cwd, prompts };
}

function collectAiSessions({ startTs, endTs, home }) {
  const base = join(home, '.claude/projects');
  if (!existsSync(base)) return { error: 'no Claude Code transcripts found' };
  const byDir = new Map();
  for (const proj of readdirSync(base, { withFileTypes: true })) {
    if (!proj.isDirectory()) continue;
    for (const f of readdirSync(join(base, proj.name))) {
      if (!f.endsWith('.jsonl')) continue;
      const file = join(base, proj.name, f);
      const st = statSync(file);
      if (st.mtimeMs / 1000 < startTs || st.size > 50 * 1024 * 1024) continue;
      const { cwd, prompts } = parseSessionLines(readFileSync(file, 'utf8').split('\n'), { startTs, endTs });
      if (!prompts.length) continue;
      const key = cwd ?? proj.name;
      const cur = byDir.get(key) ?? { project: basename(key), sessions: 0, prompts: 0, samples: [] };
      cur.sessions++;
      cur.prompts += prompts.length;
      cur.samples.push(...prompts.slice(0, 2));
      byDir.set(key, cur);
    }
  }
  const projects = [...byDir.values()].sort((a, b) => b.prompts - a.prompts).slice(0, 25).map((p) => ({ ...p, samples: p.samples.slice(0, 3) }));
  return { projects };
}

// ---------------------------------------------------------------- browser history

const WORK_HOSTS = [
  'github.com', 'gitlab.com', 'bitbucket.org', 'atlassian.net', 'atlassian.com', 'linear.app',
  'larksuite.com', 'larkoffice.com', 'feishu.cn', 'notion.so', 'figma.com', 'docs.google.com', 'drive.google.com',
  'slack.com', 'stackoverflow.com', 'sentry.io', 'datadoghq.com', 'grafana.net', 'pagerduty.com',
  'console.cloud.google.com', 'console.aws.amazon.com', 'portal.azure.com', 'vercel.com', 'localhost', '127.0.0.1',
];
const WORK_PATH_RE = /\/-\/(merge_requests|issues)\/\d+|\/pull\/\d+|\/browse\/[A-Z][A-Z0-9]+-\d+/;

export function hostMatches(host, patterns) {
  return patterns.some((p) => {
    const bare = p.startsWith('*.') ? p.slice(2) : p;
    return host === bare || host.endsWith(`.${bare}`);
  });
}

/** Drops query and fragment (they carry tokens and session ids) and flags whether the URL looks like work. */
export function classifyUrl(raw, patterns) {
  let u;
  try { u = new URL(raw); } catch { return null; }
  if (u.protocol !== 'http:' && u.protocol !== 'https:') return null;
  const clean = `${u.origin}${u.pathname.replace(/\/$/, '')}`;
  return { host: u.hostname, clean, work: hostMatches(u.hostname, patterns) || WORK_PATH_RE.test(u.pathname) };
}

export const chromiumToUnix = (t) => t / 1e6 - 11644473600;

export function summarizeVisits(rows, { patterns, includeAll = false }) {
  const hosts = new Map();
  const other = new Map();
  let filtered = 0;
  for (const r of rows) {
    const c = classifyUrl(r.url, patterns);
    if (!c) continue;
    if (!c.work) {
      filtered++;
      if (includeAll) other.set(c.host, (other.get(c.host) ?? 0) + 1);
      continue;
    }
    const h = hosts.get(c.host) ?? { host: c.host, visits: 0, pages: new Map() };
    h.visits++;
    const p = h.pages.get(c.clean) ?? { url: c.clean, title: '', visits: 0, first: r.ts, last: r.ts };
    p.visits++;
    p.first = Math.min(p.first, r.ts);
    p.last = Math.max(p.last, r.ts);
    if (r.title) p.title = r.title;
    h.pages.set(c.clean, p);
    hosts.set(c.host, h);
  }
  return {
    hosts: [...hosts.values()].sort((a, b) => b.visits - a.visits).slice(0, 20)
      .map((h) => ({ host: h.host, visits: h.visits, pages: [...h.pages.values()].sort((a, b) => b.visits - a.visits).slice(0, 8) })),
    otherDomains: [...other].sort((a, b) => b[1] - a[1]).slice(0, 15).map(([host, visits]) => ({ host, visits })),
    filteredOut: filtered,
  };
}

export function browserDbs(home = homedir(), os = platform()) {
  const mac = os === 'darwin';
  const support = mac ? join(home, 'Library/Application Support') : join(home, '.config');
  const chromium = mac
    ? { chrome: 'Google/Chrome', arc: 'Arc/User Data', brave: 'BraveSoftware/Brave-Browser', edge: 'Microsoft Edge', chromium: 'Chromium', vivaldi: 'Vivaldi' }
    : { chrome: 'google-chrome', brave: 'BraveSoftware/Brave-Browser', edge: 'microsoft-edge', chromium: 'chromium', vivaldi: 'vivaldi' };
  const dbs = [];
  const blocked = [];
  const subdirs = (d, label) => {
    try {
      return readdirSync(d, { withFileTypes: true }).filter((e) => e.isDirectory()).map((e) => e.name);
    } catch (e) {
      if (e.code === 'EPERM' || e.code === 'EACCES') blocked.push(label);
      return [];
    }
  };
  for (const [browser, rel] of Object.entries(chromium)) {
    const root = join(support, rel);
    for (const prof of subdirs(root, browser).filter((n) => n === 'Default' || /^Profile \d+$/.test(n))) {
      const path = join(root, prof, 'History');
      if (existsSync(path)) dbs.push({ browser, profile: prof, kind: 'chromium', path });
    }
  }
  const ffRoot = mac ? join(support, 'Firefox/Profiles') : join(home, '.mozilla/firefox');
  for (const prof of subdirs(ffRoot, 'firefox')) {
    const path = join(ffRoot, prof, 'places.sqlite');
    if (existsSync(path)) dbs.push({ browser: 'firefox', profile: prof, kind: 'firefox', path });
  }
  const safari = join(home, 'Library/Safari/History.db');
  if (mac && existsSync(safari)) dbs.push({ browser: 'safari', profile: 'default', kind: 'safari', path: safari });
  return { dbs, blocked };
}

function querySqlite(dbPath, sql) {
  const dir = mkdtempSync(join(tmpdir(), 'standup-'));
  try {
    const copy = join(dir, 'db');
    copyFileSync(dbPath, copy); // the live DB is locked while the browser runs
    for (const ext of ['-wal', '-shm']) if (existsSync(dbPath + ext)) copyFileSync(dbPath + ext, copy + ext);
    const out = execFileSync('sqlite3', ['-json', copy, sql], { encoding: 'utf8', timeout: 20000, maxBuffer: 64 * 1024 * 1024, stdio: ['ignore', 'pipe', 'pipe'] });
    return out.trim() ? JSON.parse(out) : [];
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

const QUERIES = {
  chromium: (a, b) => `SELECT u.url AS url, u.title AS title, v.visit_time AS t FROM visits v JOIN urls u ON u.id = v.url WHERE v.visit_time BETWEEN ${Math.floor((a + 11644473600) * 1e6)} AND ${Math.floor((b + 11644473600) * 1e6)}`,
  firefox: (a, b) => `SELECT p.url AS url, p.title AS title, v.visit_date AS t FROM moz_historyvisits v JOIN moz_places p ON p.id = v.place_id WHERE v.visit_date BETWEEN ${a * 1e6} AND ${b * 1e6}`,
  safari: (a, b) => `SELECT i.url AS url, COALESCE(v.title, '') AS title, v.visit_time AS t FROM history_visits v JOIN history_items i ON i.id = v.history_item WHERE v.visit_time BETWEEN ${a - 978307200} AND ${b - 978307200}`,
};
const TO_UNIX = { chromium: chromiumToUnix, firefox: (t) => t / 1e6, safari: (t) => t + 978307200 };

const DENIED = 'permission denied (macOS: grant Full Disk Access to your terminal app, then retry)';

function collectBrowser({ startTs, endTs, patterns, includeAll, home }) {
  const { dbs, blocked } = browserDbs(home);
  if (!dbs.length && !blocked.length) return { error: 'no supported browser history found (Chrome, Arc, Brave, Edge, Chromium, Vivaldi, Firefox, Safari)' };
  const rows = [];
  const errors = [];
  const used = [];
  for (const b of blocked) errors.push(`${b}: ${DENIED}`);
  for (const db of dbs) {
    try {
      const got = querySqlite(db.path, QUERIES[db.kind](startTs, endTs));
      used.push(`${db.browser}:${db.profile}`);
      for (const r of got) rows.push({ url: r.url, title: r.title, ts: TO_UNIX[db.kind](r.t) });
    } catch (e) {
      const msg = e.code === 'ENOENT' ? 'sqlite3 CLI not found' : /EPERM|EACCES|not permitted/i.test(String(e.message)) ? DENIED : clip(String(e.message).split('\n')[0], 120);
      errors.push(`${db.browser}:${db.profile}: ${msg}`);
    }
  }
  return { browsers: used, errors, ...summarizeVisits(rows, { patterns, includeAll }) };
}

// ---------------------------------------------------------------- output

function formatRange(r) {
  const lines = [`range: ${r.label}`, `start: ${r.startIso}`, `end:   ${r.endIso}`, `tz:    ${r.tz}`];
  for (const d of r.days) lines.push(`  ${d.date} ${d.weekday}${d.working ? '' : '  (non-working)'}`);
  return lines.join('\n');
}

function formatMachine(m) {
  const out = [];
  if (m.shell) {
    const s = m.shell;
    out.push(`## Shell history${s.files ? ` (${s.files.join(', ')})` : ''}`);
    if (s.error && !s.commands?.length) out.push(`- ${s.error}`);
    else {
      out.push(`- ${s.inRange} commands in range, ${s.redacted} withheld as possibly secret${s.untimed ? `, ${s.untimed} lines had no timestamp` : ''}`);
      if (s.tools.length) out.push(`- top: ${s.tools.map((t) => `${t.tool} ×${t.count}`).join(', ')}`);
      for (const c of s.commands) out.push(`- ${fmtTime(c.ts)}  ${c.cmd}`);
      if (s.truncated) out.push(`- … ${s.truncated} more distinct commands not shown`);
    }
  }
  if (m.git) {
    out.push(`## Git (${m.git.scanned ?? 0} repos scanned)`);
    if (m.git.error) out.push(`- ${m.git.error}`);
    else if (!m.git.repos.length) out.push('- no commits or edits in range');
    for (const r of m.git?.repos ?? []) {
      out.push(`### ${r.repo}`);
      for (const c of r.commits) out.push(`- ${fmtTime(c.ts)}  ${c.hash}  ${c.subject}`);
      if (r.dirtyCount) out.push(`- uncommitted: ${r.dirty.join(', ')}${r.dirtyCount > r.dirty.length ? ` (+${r.dirtyCount - r.dirty.length} more)` : ''}`);
    }
  }
  if (m.ai) {
    out.push('## AI coding sessions');
    if (m.ai.error) out.push(`- ${m.ai.error}`);
    else if (!m.ai.projects.length) out.push('- none in range');
    for (const p of m.ai?.projects ?? []) out.push(`- ${p.project}: ${p.prompts} prompts in ${p.sessions} session(s); e.g. ${p.samples.map((s) => `"${s}"`).join(' / ')}`);
  }
  return out.join('\n');
}

function formatBrowser(b) {
  if (b.error) return `## Browser history\n- ${b.error}`;
  const out = [`## Browser history (${b.browsers.join(', ') || 'none readable'})`];
  for (const e of b.errors) out.push(`- skipped ${e}`);
  for (const h of b.hosts) {
    out.push(`### ${h.host} (${h.visits} visits)`);
    for (const p of h.pages) out.push(`- ${p.title ? `${clip(p.title, 90)} — ` : ''}${p.url}${p.visits > 1 ? ` ×${p.visits}` : ''}`);
  }
  out.push(`- ${b.filteredOut} visits to non-work sites ignored (titles and URLs not read)`);
  if (b.otherDomains.length) out.push(`- other domains by visits (add work ones with --domains): ${b.otherDomains.map((d) => `${d.host} ${d.visits}`).join(', ')}`);
  return out.join('\n');
}

// ---------------------------------------------------------------- cli

function main(argv) {
  const [cmd, ...rest] = argv;
  const { values: v } = parseArgs({
    args: rest,
    options: {
      today: { type: 'string' }, start: { type: 'string' }, end: { type: 'string' }, config: { type: 'string' },
      sources: { type: 'string' }, repos: { type: 'string' }, author: { type: 'string' }, domains: { type: 'string' },
      'include-all': { type: 'boolean' }, json: { type: 'boolean' },
    },
  });
  const cfg = loadConfig(v.config);
  const home = homedir();
  const print = (data, text) => console.log(v.json ? JSON.stringify(data, null, 2) : text);
  const window = () => {
    if (!v.start || !v.end) throw new Error('--start and --end (YYYY-MM-DD) are required; get them from `range`');
    return { start: v.start, end: v.end, startTs: localTime(v.start, '00:00:00').ts, endTs: localTime(v.end, '23:59:59').ts };
  };

  if (cmd === 'range') {
    const r = dayRange({ today: v.today, workdays: cfg.workdays, holidays: cfg.holidays });
    return print(r, formatRange(r));
  }
  if (cmd === 'machine') {
    const w = window();
    const sources = new Set((v.sources ?? 'shell,git,ai').split(','));
    const roots = (v.repos ? v.repos.split(',') : cfg.repoRoots ?? [process.cwd()]).map(expand);
    const m = {};
    if (sources.has('shell')) m.shell = collectShell({ ...w, home });
    if (sources.has('git')) m.git = collectGit({ ...w, roots, author: v.author ?? cfg.gitAuthor });
    if (sources.has('ai')) m.ai = collectAiSessions({ ...w, home });
    return print(m, formatMachine(m));
  }
  if (cmd === 'browser') {
    const w = window();
    const patterns = [...WORK_HOSTS, ...(cfg.workDomains ?? []), ...(v.domains ? v.domains.split(',') : [])];
    const b = collectBrowser({ ...w, patterns, includeAll: v['include-all'], home });
    return print(b, formatBrowser(b));
  }
  console.error('usage: collect.mjs <range|machine|browser> [flags]; see the header of this file');
  process.exitCode = 2;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    main(process.argv.slice(2));
  } catch (e) {
    console.error(`collect: ${e.message}`);
    process.exitCode = 1;
  }
}
