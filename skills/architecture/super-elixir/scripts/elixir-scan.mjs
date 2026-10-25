#!/usr/bin/env node
// Project facts and risk-pattern candidates for the elixir skill.
//
//   node elixir-scan.mjs detect [dir] [--json]
//   node elixir-scan.mjs scan   [dir] [--json] [--strict]
//
// detect  reports the Elixir version, kind of project, dependencies, which linters exist,
//         counts of GenServers, supervisors, schemas and LiveViews, and which passes apply.
// scan    lists places worth reading. These are CANDIDATES, not findings: confirm each one
//         with references/verification-protocol.md before reporting it.
// --strict makes scan exit 1 when a critical candidate exists.
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const SKIP = new Set(['deps', '_build', 'node_modules', '.git', 'cover', 'doc', '.elixir_ls', '.elixir-tools', 'static']);
const EXT = /\.(ex|exs|heex)$/;
const SEV_ORDER = ['critical', 'major', 'minor', 'info'];
const G = 'specialities';

export function walk(root) {
  const out = [];
  const go = (dir) => {
    let entries;
    try {
      entries = readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const e of entries) {
      if (e.name.startsWith('.') && e.isDirectory() && e.name !== '.') continue;
      const p = join(dir, e.name);
      if (e.isDirectory()) {
        if (!SKIP.has(e.name)) go(p);
      } else if (EXT.test(e.name)) out.push(p);
    }
  };
  go(root);
  return out.sort();
}

const isTest = (rel) => /(^|\/)test\//.test(rel) || rel.endsWith('_test.exs');
const isConfig = (rel) => /(^|\/)config\/[^/]+\.exs$/.test(rel) && !rel.endsWith('runtime.exs') && !rel.endsWith('test.exs');

// ---- scan rules ---------------------------------------------------------------------------

export const RULES = [
  { id: 'SEC001', sev: 'critical', guide: `${G}/security-review/references/code-injection.md`, skipTests: true,
    re: /\bCode\.(eval_string|eval_quoted|eval_file|compile_string)\b/, msg: 'Code evaluation: where does the string come from?' },
  { id: 'SEC002', sev: 'critical', guide: `${G}/security-review/references/code-injection.md`, skipTests: true,
    re: /:erlang\.binary_to_term\(/, not: /:safe/, msg: 'binary_to_term without :safe: is the data untrusted?' },
  { id: 'SEC003', sev: 'major', guide: `${G}/security-review/references/atom-exhaustion.md`, skipTests: true,
    re: /String\.to_atom\(\s*(?!")/, msg: 'String.to_atom on a non-literal: name the ingress, or use to_existing_atom' },
  { id: 'SEC003', sev: 'major', guide: `${G}/security-review/references/atom-exhaustion.md`, skipTests: true,
    re: /:"[^"]*#\{/, msg: 'Interpolated atom: dynamic atoms leak the atom table' },
  { id: 'SEC004', sev: 'critical', guide: `${G}/security-review/GUIDE.md`, skipTests: true,
    re: /(Repo\.query!?|SQL\.query!?|\.query!?)\([^)]*#\{|fragment\(\s*"[^"]*#\{/, msg: 'SQL built by interpolation: use bound parameters' },
  { id: 'SEC005', sev: 'major', guide: `${G}/security-review/GUIDE.md`, skipTests: true,
    re: /:os\.cmd\(|System\.cmd\(\s*"(sh|bash|zsh)"/, msg: 'Shell command execution: is any part user-controlled?' },
  { id: 'SEC006', sev: 'major', guide: `${G}/security-review/GUIDE.md`, skipTests: true,
    re: /Phoenix\.HTML\.raw\(|<%=\s*raw\(?/, msg: 'Raw HTML output: is the value escaped upstream?' },
  { id: 'SEC007', sev: 'major', guide: `${G}/security-review/references/secrets.md`, only: 'config',
    re: /\b(secret|password|api_key|token|salt)\w*:\s*"[^"#{]{8,}"/i, msg: 'Possible secret in compile-time config: real credential?' },
  { id: 'SEC008', sev: 'info', guide: `${G}/security-review/references/process-exposure.md`, skipTests: true,
    re: /:ets\.new\([^)]*:public/, msg: 'Public ETS table: does it hold sensitive data?' },
  { id: 'SEC009', sev: 'major', guide: `${G}/security-review/references/secrets.md`, skipTests: true,
    re: /Logger\.\w+\(.*inspect\(\s*(params|conn|socket|assigns)\b/, msg: 'Logging a whole params/conn/socket can leak secrets or PII' },
  { id: 'OTP001', sev: 'major', guide: `${G}/otp/GUIDE.md`, skipTests: true,
    re: /\bspawn(_link)?\(|\bTask\.start\(/, msg: 'Unsupervised process: use a supervisor or Task.Supervisor' },
  { id: 'CODE002', sev: 'minor', guide: `${G}/code-review/GUIDE.md`, skipTests: true,
    re: /\bIO\.inspect\(|\bdbg\(/, msg: 'Debug output left in code' },
  { id: 'CODE003', sev: 'minor', guide: `${G}/tdd/GUIDE.md`, only: 'test',
    re: /Process\.sleep\(/, msg: 'Process.sleep in a test: wait on a message or condition instead' },
  { id: 'CODE005', sev: 'info', guide: `${G}/idioms/references/error-handling.md`, skipTests: true,
    re: /^\s*rescue\s*$|\brescue\s+(_|e)\b/, msg: 'rescue: only around external code, never for control flow' },
  { id: 'PERF001', sev: 'info', guide: `${G}/performance-review/GUIDE.md`, skipTests: true,
    re: /Enum\.(map|each|reduce|flat_map)\([^)]*Repo\.(get!?|one!?|all)\b|for\s.*<-.*,\s*do:.*Repo\.(get|one)/, msg: 'Query inside an enumeration: possible N+1' },
];

const BLOCKING = /\b(Process\.sleep|HTTPoison\.|Req\.(get|post|request)|Finch\.request|Tesla\.|Repo\.(all|get|one|insert|update|delete)|File\.(read|write)|System\.cmd)/;

function scanFile(path, rel) {
  const text = readFileSync(path, 'utf8');
  const lines = text.split('\n');
  const test = isTest(rel);
  const config = isConfig(rel);
  const found = [];
  const add = (rule, i, msg = rule.msg) => found.push({ id: rule.id, severity: rule.sev, file: rel, line: i + 1, message: msg, guide: rule.guide, text: lines[i].trim().slice(0, 120) });

  lines.forEach((raw, i) => {
    const t = raw.trim();
    if (!t || t.startsWith('#') || t.startsWith('iex>') || t.startsWith('...>')) return;
    for (const rule of RULES) {
      if (rule.only === 'config' && !config) continue;
      if (rule.only === 'test' && !test) continue;
      if (rule.skipTests && test) continue;
      if (rule.not && rule.not.test(raw)) continue;
      if (rule.re.test(raw)) add(rule, i);
    }
  });

  if (!test) {
    // Blocking work inside GenServer callbacks.
    lines.forEach((raw, i) => {
      if (!/^\s*def\s+handle_(call|cast|info)\(/.test(raw)) return;
      for (let j = i + 1; j < Math.min(lines.length, i + 40); j++) {
        if (/^\s*def(p|macro|macrop)?\s/.test(lines[j]) && !/^\s*def\s+handle_(call|cast|info)\(/.test(lines[j])) break;
        if (/^\s*def\s+handle_(call|cast|info)\(/.test(lines[j])) continue;
        if (BLOCKING.test(lines[j]) && !lines[j].trim().startsWith('#')) {
          found.push({ id: 'PERF002', severity: 'major', file: rel, line: j + 1, message: 'Possible blocking call inside a GenServer callback', guide: `${G}/performance-review/references/genserver-bottlenecks.md`, text: lines[j].trim().slice(0, 120) });
          break;
        }
      }
    });
    // `=` used for a step inside `with`.
    lines.forEach((raw, i) => {
      if (!/^\s*with\s/.test(raw) || !/<-/.test(raw) && !(lines[i + 1] ?? '').includes('<-')) return;
      for (let j = i; j < Math.min(lines.length, i + 20); j++) {
        const s = lines[j];
        if (j > i && /^\s*[a-z_]\w*\s*=\s*\S/.test(s) && !s.includes('<-')) {
          found.push({ id: 'CODE001', severity: 'info', file: rel, line: j + 1, message: 'Step in `with` uses `=`: if it can fail, use `<-`', guide: `${G}/pattern-matching/GUIDE.md`, text: s.trim().slice(0, 120) });
        }
        if (/\bdo\s*$|\bdo:/.test(s)) break;
      }
    });
  }
  return found;
}

export function scan(rootArg) {
  const root = resolve(rootArg);
  const files = walk(root);
  const candidates = [];
  for (const f of files) candidates.push(...scanFile(f, relative(root, f)));
  candidates.sort((a, b) => SEV_ORDER.indexOf(a.severity) - SEV_ORDER.indexOf(b.severity) || a.file.localeCompare(b.file) || a.line - b.line);
  return { root, filesScanned: files.length, candidates };
}

// ---- detect -------------------------------------------------------------------------------

function mixFiles(root) {
  const out = [];
  if (existsSync(join(root, 'mix.exs'))) out.push(join(root, 'mix.exs'));
  const apps = join(root, 'apps');
  if (existsSync(apps)) {
    for (const d of readdirSync(apps)) {
      const p = join(apps, d, 'mix.exs');
      if (existsSync(p)) out.push(p);
    }
  }
  return out;
}

export function detect(rootArg) {
  const root = resolve(rootArg);
  const mixes = mixFiles(root);
  const mixText = mixes.map((p) => readFileSync(p, 'utf8')).join('\n');
  const deps = new Set([...mixText.matchAll(/\{:([a-z0-9_]+)\s*,/g)].map((m) => m[1]));
  const elixirReq = mixText.match(/\belixir:\s*"([^"]+)"/)?.[1] ?? null;
  let toolVersions = null;
  const tv = join(root, '.tool-versions');
  if (existsSync(tv)) toolVersions = readFileSync(tv, 'utf8').match(/^elixir\s+(\S+)/m)?.[1] ?? null;

  const files = walk(root);
  const count = (re, only) => files.filter((f) => (only ? only(relative(root, f)) : true)).reduce((n, f) => n + (re.test(readFileSync(f, 'utf8')) ? 1 : 0), 0);
  const src = (rel) => !isTest(rel);
  const counts = {
    exFiles: files.filter((f) => f.endsWith('.ex')).length,
    exsFiles: files.filter((f) => f.endsWith('.exs')).length,
    testFiles: files.filter((f) => isTest(relative(root, f))).length,
    genServers: count(/\buse GenServer\b/, src),
    supervisors: count(/\buse (Supervisor|DynamicSupervisor)\b|Supervisor\.start_link/, src),
    schemas: count(/\buse Ecto\.Schema\b/, src),
    liveViews: count(/\buse \w+(\.\w+)*, :live_view\b|\buse Phoenix\.LiveView\b/, src),
    obanWorkers: count(/\buse Oban\.Worker\b/, src),
  };
  const has = (d) => deps.has(d);
  const kind = existsSync(join(root, 'apps')) && mixes.length > 1 ? 'umbrella' : has('phoenix') ? 'phoenix' : mixes.length ? 'library or application' : 'no mix.exs found';
  const gates = [];
  if (mixes.length) {
    gates.push('mix format --check-formatted', 'mix compile --warnings-as-errors', 'mix test');
    if (has('credo') || existsSync(join(root, '.credo.exs'))) gates.push('mix credo --strict');
    if (has('sobelow')) gates.push('mix sobelow');
    if (has('dialyxir')) gates.push('mix dialyzer');
    if (has('mix_audit')) gates.push('mix deps.audit');
    if (existsSync(join(root, 'mix.lock'))) gates.push('mix hex.audit');
  }
  const passes = ['code-review', 'antipatterns'];
  if (has('phoenix') || has('plug') || has('plug_cowboy') || has('bandit') || counts.schemas || has('ecto') || has('ecto_sql')) passes.push('security-review');
  if (counts.genServers || counts.supervisors || has('ecto') || has('ecto_sql') || has('oban') || has('broadway')) passes.push('performance-review');
  const specialities = [];
  if (counts.genServers || counts.supervisors) specialities.push('otp');
  if (counts.schemas || has('ecto') || has('ecto_sql')) specialities.push('ecto');
  if (has('phoenix')) specialities.push('phoenix');
  if (counts.liveViews || has('phoenix_live_view')) specialities.push('phoenix-liveview (separate skill)');
  if (has('ash')) specialities.push('architect (Ash)');
  const notable = ['phoenix', 'phoenix_live_view', 'ecto_sql', 'postgrex', 'oban', 'broadway', 'ash', 'absinthe', 'plug', 'bandit', 'credo', 'sobelow', 'dialyxir', 'mox', 'stream_data', 'benchee', 'req', 'finch'].filter(has);
  return {
    root,
    kind,
    elixir: { requirement: elixirReq, toolVersions },
    deps: notable,
    counts,
    gates,
    reviewPasses: passes,
    specialities,
    note: 'Passes and specialities are suggestions from what the project contains, not a verdict.',
  };
}

// ---- cli ----------------------------------------------------------------------------------

function formatDetect(d) {
  const lines = [
    `Project:     ${d.root}`,
    `Kind:        ${d.kind}`,
    `Elixir:      ${d.elixir.requirement ?? 'unspecified'}${d.elixir.toolVersions ? ` (.tool-versions: ${d.elixir.toolVersions})` : ''}`,
    `Deps:        ${d.deps.join(', ') || '(none of the usual suspects)'}`,
    `Files:       ${d.counts.exFiles} .ex, ${d.counts.exsFiles} .exs, ${d.counts.testFiles} test`,
    `Processes:   ${d.counts.genServers} GenServer, ${d.counts.supervisors} supervisor, ${d.counts.obanWorkers} Oban worker`,
    `Data / web:  ${d.counts.schemas} schema, ${d.counts.liveViews} LiveView`,
    `Gates:       ${d.gates.join(' | ') || '(no mix.exs)'}`,
    `Review:      ${d.reviewPasses.join(' -> ')}`,
    `Also load:   ${d.specialities.join(', ') || '(nothing extra)'}`,
  ];
  return lines.join('\n');
}

function formatScan(r) {
  const lines = [`Scanned ${r.filesScanned} file(s) under ${r.root}`, 'Candidates, not findings. Read the code and apply references/verification-protocol.md before reporting any.', ''];
  if (!r.candidates.length) lines.push('No candidates.');
  for (const c of r.candidates) lines.push(`${c.severity.toUpperCase().padEnd(8)} ${c.id.padEnd(8)} ${c.file}:${c.line}  ${c.message}\n${' '.repeat(18)}${c.text}\n${' '.repeat(18)}-> ${c.guide}`);
  const n = (s) => r.candidates.filter((c) => c.severity === s).length;
  lines.push('', `${n('critical')} critical, ${n('major')} major, ${n('minor')} minor, ${n('info')} info`);
  return lines.join('\n');
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const [cmd, ...rest] = process.argv.slice(2);
  const dir = rest.find((a) => !a.startsWith('--')) ?? '.';
  const json = rest.includes('--json');
  if (!['detect', 'scan'].includes(cmd) || !existsSync(dir) || !statSync(dir).isDirectory()) {
    console.error('usage: node elixir-scan.mjs <detect|scan> [dir] [--json] [--strict]');
    process.exit(2);
  }
  if (cmd === 'detect') {
    const d = detect(dir);
    console.log(json ? JSON.stringify(d, null, 2) : formatDetect(d));
  } else {
    const r = scan(dir);
    console.log(json ? JSON.stringify(r, null, 2) : formatScan(r));
    if (rest.includes('--strict') && r.candidates.some((c) => c.severity === 'critical')) process.exitCode = 1;
  }
}
