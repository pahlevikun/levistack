#!/usr/bin/env node
// Lint subagent files and skills.
//
//   node lint.mjs <path> [--json] [--strict]
//
// <path> is a skill folder, a SKILL.md, an agent .md file, or a directory holding either
// (agents are the .md files inside any directory named `agents`).
// Exit code 1 when there is an error, or a warning under --strict.
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { basename, dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const SKILL_KEYS = new Set([
  'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools', 'disallowed-tools', 'when_to_use',
  'argument-hint', 'arguments', 'disable-model-invocation', 'user-invocable', 'model', 'effort', 'context', 'agent',
  'background', 'hooks', 'paths', 'shell', 'icon', 'color', 'version',
]);
const AGENT_KEYS = new Set([
  'name', 'description', 'tools', 'disallowedTools', 'model', 'permissionMode', 'maxTurns', 'skills', 'mcpServers',
  'hooks', 'memory', 'background', 'omitClaudeMd', 'effort', 'isolation', 'color', 'initialPrompt', 'experimental',
  'readonly', 'is_background',
]);
const WHEN = /\b(use (when|for|this|if|to|after|before|on|in|it|proactively|immediately|whenever)|when (the )?(user|you|a|an|asked)|whenever|invoke (when|after|before))\b/i;
const SKIP_DIRS = new Set(['node_modules', '.git', 'templates', 'references', 'assets', 'scripts', '_docs']);
const SKIP_AGENT_FILES = new Set(['README.md', 'readme.md']);
const FIRST_PERSON = /^\s*(I|We)\s|\bI (can|will|'ll|help|am)\b|\bhelps? you\b|\byou can (use|ask)\b/;
const RESERVED_NAME = /(^|-)(anthropic|claude)(-|$)/;
const XML_TAG = /<\/?[a-z][a-z0-9_-]*(\s[^>]*)?>/i;
const NEEDS_USER = /\bAskUserQuestion\b|\bask the user\b|\bask (them|me) (a|for|which|whether)\b|\bwait for (the )?(user|confirmation|approval)\b|\bpresent (the )?options to the user\b/i;
export const BODY_LINES_SKILL = 500;
export const BODY_LINES_AGENT = 120;

export function parseFrontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!m) return { data: {}, body: text, has: false, unsafe: [], keys: [] };
  const data = {};
  const unsafe = [];
  const keys = [];
  const lines = m[1].split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const kv = lines[i].match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!kv) continue;
    keys.push(kv[1]);
    let v = kv[2].trim();
    const block = v.match(/^([>|])[+-]?$/);
    if (block || v === '') {
      const parts = [];
      while (i + 1 < lines.length && (/^\s+\S/.test(lines[i + 1]) || /^\s*-\s/.test(lines[i + 1]) || lines[i + 1].trim() === '')) {
        parts.push(lines[++i].trim());
      }
      v = block && block[1] === '>' ? parts.join(' ').replace(/\s+/g, ' ').trim() : parts.join('\n').trim();
    } else if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
      v = v.slice(1, -1);
    } else if (/:\s|\s#|^[&*!%@`'"]/.test(v)) {
      unsafe.push(kv[1]);
    }
    data[kv[1]] = v;
  }
  return { data, body: m[2], has: true, unsafe, keys };
}

const bodyLines = (body) => body.replace(/\s+$/, '').split('\n').length;

function localLinks(text) {
  const t = text.replace(/```[\s\S]*?```/g, '').replace(/`[^`\n]*`/g, '');
  const out = [];
  for (const m of t.matchAll(/\]\(([^)\s]+)\)/g)) {
    const l = m[1].split('#')[0];
    if (l && !/^(https?:|mailto:|tel:)/.test(l)) out.push(l);
  }
  return out;
}

function lintSkill(file, add) {
  const dir = dirname(file);
  const folder = basename(dir);
  const { data, body, has, unsafe, keys } = parseFrontmatter(readFileSync(file, 'utf8'));
  if (!has) return add('error', 'no-frontmatter', file, 'missing YAML frontmatter');
  const name = data.name;
  if (!name) add('error', 'name-missing', file, 'name is required');
  else {
    if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(name) || name.length > 64) add('error', 'name-format', file, `name "${name}" must be 1-64 chars of a-z, 0-9 and single hyphens`);
    if (name !== folder) add('error', 'name-folder', file, `name "${name}" must equal the folder name "${folder}"`);
  }
  const desc = data.description;
  if (!desc) add('error', 'description-missing', file, 'description is required');
  else {
    if (desc.length > 1024) add('error', 'description-length', file, `description is ${desc.length} chars; the limit is 1024`);
    if (desc.length + (data.when_to_use?.length ?? 0) > 1536) add('warn', 'listing-budget', file, 'description plus when_to_use is over 1,536 chars; Claude Code truncates the listing');
    if (!WHEN.test(desc) && !data.when_to_use) add('warn', 'no-trigger', file, 'description has no "Use when ..." trigger');
  }
  if (desc && FIRST_PERSON.test(desc)) add('warn', 'first-person', file, 'description is not in the third person ("I can help you ..."); write what the skill does ("Extracts ...")');
  if (name && RESERVED_NAME.test(name)) add('warn', 'reserved-name', file, `name "${name}" contains a word that Anthropic's skill guidance reserves ("anthropic", "claude"); choose another`);
  if ((desc && XML_TAG.test(desc)) || (name && XML_TAG.test(name))) add('warn', 'xml-in-description', file, 'name or description contains an XML-like tag; the skill listing does not allow them');
  if (unsafe.includes('description') || unsafe.includes('name')) add('error', 'yaml-unquoted', file, 'a value contains ": " or "#" unquoted; strict YAML parsers (including the skills CLI) skip the skill. Quote it');
  for (const k of keys) if (!SKILL_KEYS.has(k)) add('warn', 'unknown-field', file, `unknown frontmatter field "${k}"`);
  if (!body.trim()) add('error', 'empty-body', file, 'SKILL.md has no instructions');
  const n = bodyLines(body);
  if (n > BODY_LINES_SKILL) add('warn', 'too-long', file, `body is ${n} lines; keep under ${BODY_LINES_SKILL} and move detail to references/`);

  const text = readFileSync(file, 'utf8');
  const linked = new Set();
  for (const l of localLinks(text)) {
    const target = join(dir, l);
    if (!existsSync(target)) add('error', 'broken-link', file, `linked file not found: ${l}`);
    else linked.add(resolve(target));
  }
  for (const target of linked) {
    if (!target.endsWith('.md') || !statSync(target).isFile()) continue;
    // Only plain reference files form a chain. A router skill's speciality GUIDE.md, a template and a README
    // may link onward to their own references (router -> guide -> reference).
    if (!relative(dir, target).split('/').includes('references')) continue;
    for (const l of localLinks(readFileSync(target, 'utf8'))) {
      const next = resolve(dirname(target), l);
      if (next.endsWith('.md') && next.startsWith(resolve(dir)) && next !== resolve(file) && next !== target && existsSync(next)) {
        add('warn', 'deep-reference', target, `links to ${relative(dir, next)}; keep references one level from SKILL.md`);
      }
    }
  }
  const mdText = [];
  const files = [];
  const walk = (d) => {
    for (const e of readdirSync(d, { withFileTypes: true })) {
      if (e.name.startsWith('.')) continue;
      const p = join(d, e.name);
      if (e.isDirectory()) walk(p);
      else {
        files.push(p);
        if (e.name.endsWith('.md')) mdText.push(readFileSync(p, 'utf8'));
      }
    }
  };
  walk(dir);
  const all = mdText.join('\n');
  for (const p of files) {
    if (p === file || p.endsWith('.md') && basename(p) === 'DESCRIPTION.md') continue;
    const rel = relative(dir, p);
    if (!rel.includes('/')) continue; // only files inside subfolders
    if (!all.includes(basename(p))) add('warn', 'unreferenced-file', p, `${rel} is not mentioned in any markdown file of the skill`);
  }
}

function toolList(v) {
  if (!v) return [];
  return v.split(/[\n,]/).map((s) => s.replace(/^\s*-\s*/, '').trim()).filter(Boolean).flatMap((s) => (s.includes(' ') && !s.includes('(') ? s.split(/\s+/) : [s]));
}

function lintAgent(file, add) {
  const { data, body, has, unsafe, keys } = parseFrontmatter(readFileSync(file, 'utf8'));
  if (!has) return add('error', 'no-frontmatter', file, 'missing YAML frontmatter');
  const base = basename(file, '.md');
  const name = data.name;
  if (!name) add('warn', 'name-missing', file, 'name is missing (Claude Code requires it; Cursor falls back to the filename)');
  else {
    if (!/^[a-z0-9][a-z0-9-]*$/.test(name)) add('error', 'name-format', file, `name "${name}" must be lowercase letters, digits and hyphens, not starting with "-" or containing ":"`);
    if (name !== base) add('warn', 'name-filename', file, `name "${name}" differs from the filename "${base}"`);
  }
  const desc = data.description;
  if (!desc) add('error', 'description-missing', file, 'description is required; it is how the model decides to delegate');
  else {
    if (!WHEN.test(desc)) add('warn', 'no-trigger', file, 'description does not say when to call the agent ("Use after ...")');
    if (desc.length > 600) add('warn', 'description-long', file, `description is ${desc.length} chars; it is loaded every session, keep it short`);
  }
  if (unsafe.includes('description')) add('warn', 'yaml-unquoted', file, 'description contains ": " or "#" unquoted; quote it so strict parsers read it');
  for (const k of keys) if (!AGENT_KEYS.has(k)) add('warn', 'unknown-field', file, `unknown frontmatter field "${k}"`);
  const tools = toolList(data.tools);
  if (tools.some((t) => /^shell$/i.test(t))) add('warn', 'tool-name', file, '"Shell" is not a Claude Code tool name; use "Bash"');
  const writes = tools.some((t) => /^(write|edit|multiedit|notebookedit)$/i.test(t));
  if (writes && /read-only|never edit (any )?files|do not edit (any )?files|don't edit (any )?files/i.test(body)) add('warn', 'tools-vs-body', file, 'body says read-only but tools include Write or Edit');
  if (tools.some((t) => /^askuserquestion$/i.test(t)) || NEEDS_USER.test(body)) add('warn', 'needs-user', file, 'a subagent cannot ask the user (it runs in its own context and returns one report). Return open questions in the report, and keep the questioning in the main session');
  if (data.model && /\s/.test(data.model)) add('warn', 'model-format', file, `model "${data.model}" contains whitespace`);
  if (!body.trim()) add('error', 'empty-body', file, 'the body is the system prompt and is empty');
  const n = bodyLines(body);
  if (n > BODY_LINES_AGENT) add('warn', 'too-long', file, `body is ${n} lines; keep an agent under about ${BODY_LINES_AGENT}`);
  if (!/\bdo not\b|\bdon't\b|\bnever\b/i.test(body)) add('info', 'no-guardrails', file, 'no explicit "Do not" list');
}

function collect(path) {
  const p = resolve(path);
  const items = [];
  const st = statSync(p);
  if (st.isFile()) {
    items.push({ type: basename(p) === 'SKILL.md' ? 'skill' : 'agent', file: p });
    return items;
  }
  if (existsSync(join(p, 'SKILL.md'))) {
    items.push({ type: 'skill', file: join(p, 'SKILL.md') });
    return items;
  }
  const walk = (d, inAgents) => {
    for (const e of readdirSync(d, { withFileTypes: true })) {
      if (e.name.startsWith('.') && !['.claude', '.cursor', '.codex', '.agents'].includes(e.name)) continue;
      const full = join(d, e.name);
      if (e.isDirectory()) {
        if (SKIP_DIRS.has(e.name) && !(e.name === 'agents')) continue;
        walk(full, inAgents || e.name === 'agents');
      } else if (e.name === 'SKILL.md') items.push({ type: 'skill', file: full });
      else if (inAgents && e.name.endsWith('.md') && !SKIP_AGENT_FILES.has(e.name)) items.push({ type: 'agent', file: full });
    }
  };
  walk(p, basename(p) === 'agents');
  return items;
}

export function lintPath(path) {
  const base = resolve(path);
  const root = statSync(base).isDirectory() ? base : dirname(base);
  const findings = [];
  const items = collect(path);
  for (const it of items) {
    const add = (severity, code, file, message) => findings.push({ severity, code, type: it.type, file: relative(root, file) || basename(file), message });
    (it.type === 'skill' ? lintSkill : lintAgent)(it.file, add);
  }
  return { root, items: items.map((i) => ({ type: i.type, file: relative(root, i.file) || basename(i.file) })), findings };
}

function format(r) {
  const lines = [`Checked ${r.items.length} item(s) under ${r.root}`];
  for (const f of r.findings) lines.push(`${f.severity.toUpperCase().padEnd(5)} ${f.code.padEnd(17)} ${f.file}: ${f.message}`);
  const c = (s) => r.findings.filter((f) => f.severity === s).length;
  lines.push('', `${c('error')} error(s), ${c('warn')} warning(s), ${c('info')} note(s)`);
  return lines.join('\n');
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const args = process.argv.slice(2);
  const target = args.find((a) => !a.startsWith('--'));
  if (!target || !existsSync(target)) {
    console.error('usage: node lint.mjs <skill-dir | SKILL.md | agent.md | directory> [--json] [--strict]');
    process.exit(2);
  }
  const r = lintPath(target);
  console.log(args.includes('--json') ? JSON.stringify(r, null, 2) : format(r));
  if (r.findings.some((f) => f.severity === 'error' || (args.includes('--strict') && f.severity === 'warn'))) process.exitCode = 1;
}
