#!/usr/bin/env node
// Convert agent-requested rules, slash commands and subagents into skills. The body is copied verbatim.
//
//   node convert.mjs <source...> --out <skills-dir> [--kind rule|command|agent] [--name <name>]
//                    [--description "<text>"] [--paths] [--force] [--dry-run]
//
// Rule     (.mdc / .md with description, no alwaysApply): SKILL.md with name + description.
// Agent    (subagent .md): SKILL.md with name + description (+ model); tools and other agent-only keys are
//          dropped with a warning. --fork adds context: fork so it still runs in its own context.
// Command  (.md, frontmatter optional): SKILL.md with name + description + disable-model-invocation: true,
//          other frontmatter keys (argument-hint, allowed-tools, model, ...) kept as written.
// Skipped on purpose: always-on rules (a skill would stop applying them) and, unless --paths, file-scoped rules.
// Never deletes or edits a source file.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { basename, extname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

export const MAX_DESCRIPTION = 1024;

export function parseFrontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)([\s\S]*)$/);
  if (!m) return { has: false, blocks: [], body: text };
  const lines = m[1].split(/\r?\n/);
  const blocks = [];
  for (let i = 0; i < lines.length; i++) {
    const kv = lines[i].match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!kv) {
      if (blocks.length && lines[i].trim()) blocks.at(-1).lines.push(lines[i]);
      continue;
    }
    const block = { key: kv[1], first: kv[2].trim(), lines: [lines[i]] };
    while (i + 1 < lines.length && (/^\s+\S/.test(lines[i + 1]) || /^\s*-\s/.test(lines[i + 1]) || (lines[i + 1].trim() === '' && /^\s/.test(lines[i + 2] ?? '')))) {
      block.lines.push(lines[++i]);
    }
    blocks.push(block);
  }
  return { has: true, blocks, body: m[2] };
}

// The text value of a frontmatter block: unquoted scalar, or folded block text.
export function valueOf(block) {
  if (!block) return '';
  const first = block.first;
  if (/^[>|][+-]?$/.test(first) || first === '') {
    return block.lines.slice(1).map((l) => l.trim().replace(/^-\s+/, '')).filter(Boolean).join(first.startsWith('|') ? '\n' : ' ');
  }
  if (/^(".*"|'.*')$/.test(first)) return first.slice(1, -1);
  return first;
}

export const slugify = (s) =>
  s.toLowerCase().replace(/\.[a-z]+$/, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').replace(/-{2,}/g, '-');

const oneLine = (s) => s.replace(/\s+/g, ' ').trim();
const yamlString = (s) => JSON.stringify(oneLine(s));

export function inferKind(file) {
  const parts = resolve(file).split(sep);
  if (parts.includes('commands')) return 'command';
  if (parts.includes('agents')) return 'agent';
  if (parts.includes('rules') || extname(file) === '.mdc') return 'rule';
  return null;
}

// "<commands-dir>/frontend/component.md" -> "frontend-component"
export function nameFromPath(file, kind) {
  const parts = resolve(file).split(sep);
  const dir = { command: 'commands', agent: 'agents', rule: 'rules' }[kind];
  const at = parts.lastIndexOf(dir);
  const rel = at === -1 ? [basename(file)] : parts.slice(at + 1);
  return slugify(rel.join('-'));
}

function firstLineDescription(text) {
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith('---')) continue;
    return line.replace(/^#+\s*/, '').replace(/[`*_]/g, '').trim();
  }
  return '';
}

function compose({ name, description, extraBlocks = [], paths, body, blankBefore = false }) {
  const head = ['---', `name: ${name}`, `description: ${yamlString(description)}`];
  if (paths) head.push(...paths.lines);
  for (const b of extraBlocks) head.push(...b.lines);
  head.push('---');
  return `${head.join('\n')}\n${blankBefore ? '\n' : ''}${body}`;
}

// Pure: returns { status: 'convert'|'skip'|'error', name, skillMd, warnings, reason }.
export function convertSource({ file, text, kind, name, description, paths = false, fork = false }) {
  const warnings = [];
  const fail = (status, reason) => ({ status, reason, warnings });
  const k = kind ?? inferKind(file);
  if (!k) return fail('error', 'cannot tell if this is a rule or a command; pass --kind rule|command');
  const skillName = name ?? nameFromPath(file, k);
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(skillName) || skillName.length > 64) {
    return fail('error', `"${skillName}" is not a valid skill name (1-64 chars of a-z, 0-9, single hyphens); pass --name`);
  }
  const fm = parseFrontmatter(text);
  const block = (key) => fm.blocks.find((b) => b.key === key);

  if (k === 'rule') {
    const always = valueOf(block('alwaysApply')) === 'true';
    if (always) return fail('skip', 'always-on rule (alwaysApply: true); a skill loads on demand and would stop applying it');
    const scope = block('globs') ?? block('paths');
    if (scope && valueOf(scope) && !paths) {
      return fail('skip', 'file-scoped rule (globs/paths); a skill is chosen by its description, not by the file open. Pass --paths to keep the scope as `paths`');
    }
    if (!fm.has && !description) return fail('skip', 'no frontmatter: the rule is always on. Pass --description to convert it anyway');
    const desc = description ?? valueOf(block('description'));
    if (!desc) return fail('error', 'no description; pass --description');
    const dropped = fm.blocks.filter((b) => !['description', 'globs', 'paths', 'alwaysApply'].includes(b.key)).map((b) => b.key);
    if (dropped.length) warnings.push(`dropped frontmatter key(s): ${dropped.join(', ')}`);
    let pathsBlock = null;
    if (scope && paths) {
      pathsBlock = scope.key === 'paths' ? scope : { lines: [`paths: ${yamlString(valueOf(scope))}`] };
    }
    return finish({ name: skillName, description: desc, paths: pathsBlock, body: fm.has ? fm.body : text, blankBefore: !fm.has }, warnings);
  }

  if (k === 'agent') {
    const desc = description ?? valueOf(block('description'));
    if (!desc) return fail('error', 'no description; pass --description');
    const keep = fm.blocks.filter((b) => b.key === 'model');
    const lost = fm.blocks.filter((b) => !['name', 'description', 'model'].includes(b.key)).map((b) => b.key);
    if (lost.length) warnings.push(`dropped agent-only key(s): ${lost.join(', ')}. A skill cannot restrict tools or set permissions; the work now runs with the caller's tools unless --fork`);
    const extra = [...keep];
    if (fork) {
      extra.push({ key: 'context', lines: ['context: fork'] });
      warnings.push('context: fork runs it in a general-purpose subagent, not in the original agent definition');
    } else warnings.push('runs inline in the current context now; isolation is lost (pass --fork to keep it)');
    return finish({ name: skillName, description: desc, extraBlocks: extra, body: fm.has ? fm.body : text, blankBefore: !fm.has }, warnings);
  }

  // command
  const explicit = description ?? valueOf(block('description'));
  let desc = explicit;
  if (!desc) {
    desc = firstLineDescription(fm.has ? fm.body : text);
    if (!desc) return fail('error', 'empty command; nothing to convert');
    warnings.push(`description inferred from the first line ("${desc}"); rewrite it as what it does plus "Use when ..."`);
  }
  const extra = fm.blocks.filter((b) => !['name', 'description'].includes(b.key));
  if (!extra.some((b) => b.key === 'disable-model-invocation')) extra.push({ key: 'disable-model-invocation', lines: ['disable-model-invocation: true'] });
  const unsupported = fm.blocks.filter((b) => ['paths', 'context', 'agent', 'background'].includes(b.key));
  if (unsupported.length) warnings.push(`kept ${unsupported.map((b) => b.key).join(', ')}: valid on a skill, but check it was intended`);
  const segments = resolve(file).split(sep);
  const at = segments.lastIndexOf('commands');
  if (at !== -1 && segments.length - at - 1 > 1) {
    warnings.push('nested command folder joined with "-" (Claude Code namespaced it with ":"); pass --name to choose');
  }
  return finish({ name: skillName, description: desc, extraBlocks: extra, body: fm.has ? fm.body : text, blankBefore: !fm.has }, warnings);
}

function finish(parts, warnings) {
  const description = oneLine(parts.description);
  if (description.length > MAX_DESCRIPTION) return { status: 'error', reason: `description is ${description.length} chars; the limit is ${MAX_DESCRIPTION}`, warnings };
  if (!/\b(use (when|for|this|if|to|after|before|whenever)|when (the )?(user|you|a|an|asked)|whenever)\b/i.test(description) && !parts.extraBlocks?.some((b) => b.key === 'disable-model-invocation')) {
    warnings.push('description has no "Use when ..." trigger; a skill is chosen from it');
  }
  return { status: 'convert', name: parts.name, skillMd: compose({ ...parts, description }), warnings };
}

function parseArgs(argv) {
  const sources = [];
  const opts = {};
  const flags = new Set(['paths', 'force', 'dry-run', 'fork']);
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) sources.push(a);
    else if (flags.has(a.slice(2))) opts[a.slice(2)] = true;
    else {
      if (argv[i + 1] === undefined) throw new Error(`${a} needs a value`);
      opts[a.slice(2)] = argv[++i];
    }
  }
  return { sources, opts };
}

function main() {
  let parsed;
  try {
    parsed = parseArgs(process.argv.slice(2));
  } catch (e) {
    console.error(`convert: ${e.message}`);
    process.exit(2);
  }
  const { sources, opts } = parsed;
  if (!sources.length || !opts.out) {
    console.error('usage: convert.mjs <source...> --out <skills-dir> [--kind rule|command|agent] [--name n] [--description d] [--paths] [--fork] [--force] [--dry-run]');
    process.exit(2);
  }
  if (opts.kind && !['rule', 'command', 'agent'].includes(opts.kind)) {
    console.error('convert: --kind must be rule, command or agent');
    process.exit(2);
  }
  if (sources.length > 1 && (opts.name || opts.description)) {
    console.error('convert: --name and --description apply to one source at a time');
    process.exit(2);
  }
  const out = resolve(opts.out);
  if (out.split(sep).includes('skills-cursor')) {
    console.error('convert: skills-cursor is reserved for Cursor built-in skills; choose another --out');
    process.exit(2);
  }
  let failed = 0;
  const seen = new Set();
  for (const source of sources) {
    if (!existsSync(source)) {
      console.log(`error   ${source}: file not found`);
      failed++;
      continue;
    }
    const r = convertSource({ file: source, text: readFileSync(source, 'utf8'), kind: opts.kind, name: opts.name, description: opts.description, paths: opts.paths, fork: opts.fork });
    if (r.status === 'convert' && seen.has(r.name)) {
      r.status = 'error';
      r.reason = `two sources map to the skill name "${r.name}"; convert them separately with --name`;
    }
    if (r.status === 'skip') {
      console.log(`skipped ${source}: ${r.reason}`);
      continue;
    }
    if (r.status === 'error') {
      console.log(`error   ${source}: ${r.reason}`);
      failed++;
      continue;
    }
    seen.add(r.name);
    const dest = join(out, r.name, 'SKILL.md');
    if (existsSync(dest) && !opts.force) {
      console.log(`error   ${source}: ${dest} already exists (use --force to overwrite)`);
      failed++;
      continue;
    }
    if (!opts['dry-run']) {
      mkdirSync(join(out, r.name), { recursive: true });
      writeFileSync(dest, r.skillMd);
    }
    console.log(`${opts['dry-run'] ? 'would convert' : 'converted'} ${source} -> ${dest}`);
    for (const w of r.warnings) console.log(`  warning: ${w}`);
  }
  if (failed) process.exit(1);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) main();
