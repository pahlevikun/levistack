#!/usr/bin/env node
// Produce an attributable date-bounded work report from caller-selected evidence.
import { readFileSync, writeFileSync, lstatSync, statSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

function date(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value ?? '') || !Number.isFinite(Date.parse(value)) || new Date(value).toISOString().slice(0, 10) !== value) throw new Error('start/end must be real YYYY-MM-DD dates');
  return value;
}
const text = value => String(value ?? '').replace(/[\r\n|]/g, ' ').replace(/[\[\]<>`]/g, '').slice(0, 1000);
function safeUrl(value) {
  if (!value) return '';
  const u = new URL(value);
  if (!['http:', 'https:'].includes(u.protocol) || u.username || u.password) throw new Error('evidence URL must be HTTP(S) without embedded credentials');
  u.search = ''; u.hash = '';
  return u.toString().replaceAll('(', '%28').replaceAll(')', '%29');
}

export function report(records, { start, end, timezone, actor }) {
  date(start); date(end);
  if (start > end) throw new Error('start must not follow end');
  if (!actor?.trim()) throw new Error('actor is required');
  const formatter = new Intl.DateTimeFormat('en-CA', { timeZone: timezone, year: 'numeric', month: '2-digit', day: '2-digit' });
  if (!Array.isArray(records) || records.length > 100000) throw new Error('input must be an array of at most 100000 records');
  const unique = new Map();
  for (const r of records) {
    if (!r || typeof r !== 'object' || Array.isArray(r)) throw new Error('evidence records must be objects');
    if (r.actor !== actor) continue;
    if (!r.id || !r.source || !r.kind || !r.title || typeof r.timestamp !== 'string') throw new Error('records require id, source, kind, title and an ISO timestamp with offset');
    const match = /^(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,9})?(Z|[+-](\d{2}):(\d{2}))$/.exec(r.timestamp);
    if (!match) throw new Error('ISO timestamp must include seconds and an explicit offset');
    date(match[1]);
    if (+match[2] > 23 || +match[3] > 59 || +match[4] > 59 || +(match[6] || 0) > 23 || +(match[7] || 0) > 59) throw new Error('invalid timestamp time or offset');
    const instant = new Date(r.timestamp);
    if (!Number.isFinite(instant.getTime())) throw new Error('invalid record timestamp');
    const parts = Object.fromEntries(formatter.formatToParts(instant).map(p => [p.type, p.value]));
    const day = `${parts.year}-${parts.month}-${parts.day}`;
    const kind = r.kind === 'review' ? 'reviewed' : r.kind;
    if (day < start || day > end || (kind === 'reviewed' && r.subject_author === actor)) continue;
    const item = { ...r, kind, day, url: safeUrl(r.url), instant: instant.getTime() };
    const key = JSON.stringify([r.source, r.id, kind, instant.toISOString(), r.status ?? '']);
    if (!unique.has(key)) unique.set(key, item);
  }
  const selected = [...unique.values()].sort((a, b) => a.instant - b.instant);
  const lines = [`# Activity report: ${start} to ${end}`, '', `Actor: ${text(actor)}. Timezone: ${text(timezone)}.`, '', 'Evidence records describe observed activity; they do not establish business impact or completion beyond their recorded status.', '', '| Date | Activity | Status | Source |', '|---|---|---|---|'];
  for (const r of selected) lines.push(`| ${r.day} | ${text(r.kind)}: ${text(r.title)} | ${text(r.status || 'unspecified')} | ${r.url ? `[${text(r.source)}](<${r.url}>)` : text(r.source)} |`);
  if (!selected.length) lines.push('| — | No matching evidence in the selected input | — | — |');
  lines.push('', `Included ${selected.length} unique records. Coverage is limited to the input sources supplied; missing sources are not evidence of inactivity.`, '');
  return lines.join('\n');
}

function main() {
  const args = process.argv.slice(2), options = {};
  for (let i = 0; i < args.length; i++) {
    const key = args[i];
    if (key === '--overwrite') { options.overwrite = true; continue; }
    if (!['--input', '--output', '--start', '--end', '--timezone', '--actor'].includes(key) || !args[i + 1]) throw new Error('usage: period-report.mjs --input evidence.json --output report.md --start YYYY-MM-DD --end YYYY-MM-DD --timezone AREA/CITY --actor ID [--overwrite]');
    options[key.slice(2)] = args[++i];
  }
  if (!options.input || !options.output || !options.timezone) throw new Error('input, output and timezone are required');
  if (resolve(options.input) === resolve(options.output)) throw new Error('output must differ from input');
  try {
    if (lstatSync(options.output).isSymbolicLink()) throw new Error('output must not be a symlink');
    const inputInfo = statSync(options.input), outputInfo = statSync(options.output);
    if (inputInfo.dev === outputInfo.dev && inputInfo.ino === outputInfo.ino) throw new Error('output must not alias input');
  } catch (error) { if (error.code !== 'ENOENT') throw error; }
  const raw = readFileSync(options.input, 'utf8');
  if (Buffer.byteLength(raw) > 20_000_000) throw new Error('input exceeds 20 MB');
  const rendered = report(JSON.parse(raw), options);
  writeFileSync(options.output, rendered, { flag: options.overwrite ? 'w' : 'wx' });
  process.stdout.write(JSON.stringify({ output: options.output }) + '\n');
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { main(); } catch (error) { process.stderr.write(`error: ${error.message}\n`); process.exitCode = 2; }
}
