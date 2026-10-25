#!/usr/bin/env node
// Check rule files for the mistakes that make a rule silently never apply.
//
//   node check-rule.mjs <file-or-dir> [--json]
//
// Accepts .md and .mdc files; a directory is searched recursively. Exit code 1 when there is an error.
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { basename, extname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const INFO_LINES = 50;
export const WARN_LINES = 200;

function splitFrontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!m) return { has: false, lines: [], body: text };
  return { has: true, lines: m[1].split(/\r?\n/), body: m[2] };
}

// Top-level `key: value` pairs. Returns the raw value so quoting can be judged.
function readFields(lines) {
  const fields = new Map();
  for (let i = 0; i < lines.length; i++) {
    const kv = lines[i].match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!kv) continue;
    let value = kv[2].trim();
    const block = value.match(/^[>|][+-]?$/);
    if (block || value === '') {
      const parts = [];
      while (i + 1 < lines.length && (/^\s+\S/.test(lines[i + 1]) || /^\s*-\s/.test(lines[i + 1]))) parts.push(lines[++i].trim());
      value = parts.join(block ? ' ' : '\n');
      fields.set(kv[1], { value, quoted: true, list: !block && parts.length > 0 });
    } else {
      const quoted = /^(".*"|'.*')$/.test(value);
      fields.set(kv[1], { value: quoted ? value.slice(1, -1) : value, quoted, list: false });
    }
  }
  return fields;
}

export function checkRule(file, text = readFileSync(file, 'utf8')) {
  const findings = [];
  const add = (severity, code, message) => findings.push({ severity, code, file, message });
  const ext = extname(file);
  const inClaudeRules = /(^|\/)\.claude\/rules\//.test(file);
  const { has, lines, body } = splitFrontmatter(text);

  if (!has) {
    if (ext === '.mdc') add('error', 'no-frontmatter', 'a Cursor .mdc rule needs frontmatter (description, globs, alwaysApply)');
    else add('info', 'no-frontmatter', 'no frontmatter: the rule is always on (fine for a Claude Code rule, but say so on purpose)');
  }
  const fields = readFields(lines);
  const get = (k) => fields.get(k);

  for (const [key, f] of fields) {
    if (f.quoted || f.list) continue;
    if (/:\s|\s#/.test(f.value)) add('error', 'yaml-unquoted', `"${key}" contains ": " or " #" unquoted; quote the value`);
    if (/^[*&!%@`]/.test(f.value)) add('error', 'yaml-leading-indicator', `"${key}: ${f.value}" starts with a YAML indicator (a leading * is an alias); quote the value`);
  }

  const desc = get('description')?.value ?? '';
  const globs = get('globs')?.value ?? '';
  const paths = get('paths')?.value ?? '';
  const always = get('alwaysApply')?.value === 'true';

  if (has && ext === '.mdc' && !desc && !globs && !always) {
    add('warn', 'never-applies', 'no description, no globs and alwaysApply is not true: only a manual mention loads this rule');
  }
  if (has && !desc && ext !== '.mdc' && !inClaudeRules && !paths) {
    add('warn', 'no-description', 'catalog-style rules need a one-line description (it is how the rule is chosen and listed)');
  }
  if (desc.length > 300) add('warn', 'description-long', `description is ${desc.length} chars; keep it to one line`);
  if (always && globs) add('warn', 'scope-conflict', 'alwaysApply is true and globs is set; the globs add nothing');
  if (always && paths) add('warn', 'scope-conflict', 'alwaysApply is true and paths is set; the paths add nothing');
  if (inClaudeRules) {
    for (const k of ['description', 'globs', 'alwaysApply']) {
      if (fields.has(k)) add('info', 'ignored-field', `Claude Code reads only "paths" in .claude/rules; "${k}" is ignored there`);
    }
    if (ext === '.mdc') add('warn', 'claude-ext', 'Claude Code discovers .md rule files; check that an .mdc file loads before relying on it');
  } else if (paths && ext === '.mdc') {
    add('info', 'ignored-field', 'Cursor reads "globs", not "paths"');
  }
  if (!body.trim()) add('error', 'empty-body', 'the rule has no content');
  const n = body.replace(/\s+$/, '').split('\n').length;
  if (body.trim() && n > WARN_LINES) add('warn', 'too-long', `body is ${n} lines; split it into one concern per rule`);
  else if (body.trim() && n > INFO_LINES) add('info', 'long', `body is ${n} lines; rules work best under ${INFO_LINES}`);
  if (/(api[_-]?key|secret|token|password)\s*[:=]\s*['"][A-Za-z0-9_-]{16,}['"]/i.test(text)) add('error', 'secret', 'looks like a secret');
  return findings;
}

function collect(path) {
  const p = resolve(path);
  if (statSync(p).isFile()) return [p];
  const out = [];
  const walk = (d) => {
    for (const e of readdirSync(d, { withFileTypes: true })) {
      if (e.name === 'node_modules' || e.name === '.git') continue;
      const full = join(d, e.name);
      if (e.isDirectory()) walk(full);
      else if (/\.mdc?$/.test(e.name) && basename(e.name) !== 'README.md') out.push(full);
    }
  };
  walk(p);
  return out;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const args = process.argv.slice(2);
  const target = args.find((a) => !a.startsWith('--'));
  if (!target) {
    console.error('usage: check-rule.mjs <file-or-dir> [--json]');
    process.exit(2);
  }
  let files;
  try {
    files = collect(target);
  } catch (e) {
    console.error(`check-rule: ${e.message}`);
    process.exit(2);
  }
  const findings = files.flatMap((f) => checkRule(f));
  if (args.includes('--json')) console.log(JSON.stringify({ files: files.length, findings }, null, 2));
  else {
    for (const f of findings) console.log(`${f.severity.padEnd(5)} ${f.file}: ${f.message} [${f.code}]`);
    const errors = findings.filter((f) => f.severity === 'error').length;
    console.log(`checked ${files.length} rule file(s): ${errors} error(s), ${findings.length - errors} other finding(s)`);
  }
  process.exit(findings.some((f) => f.severity === 'error') ? 1 : 0);
}
