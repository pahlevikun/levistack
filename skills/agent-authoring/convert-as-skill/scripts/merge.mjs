#!/usr/bin/env node
// Draft a merge of two or more skill folders. Does not write or delete.
//
//   node merge.mjs <skill-dir...> [--name <name>] [--out <skills-dir>] [--json]
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { basename, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseFrontmatter, slugify, valueOf } from './convert.mjs';

function localLinks(text) {
  const t = text.replace(/```[\s\S]*?```/g, '').replace(/`[^`\n]*`/g, '');
  const out = [];
  for (const m of t.matchAll(/\]\(([^)\s]+)\)/g)) {
    const l = m[1].split('#')[0];
    if (l && !/^(https?:|mailto:|tel:)/.test(l)) out.push(l);
  }
  return out;
}

function walkFiles(dir, acc = []) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith('.')) continue;
    const p = join(dir, e.name);
    if (e.isDirectory()) walkFiles(p, acc);
    else acc.push(p);
  }
  return acc;
}

export function readSkillDir(dir) {
  const root = resolve(dir);
  const skillMd = join(root, 'SKILL.md');
  if (!existsSync(skillMd) || !statSync(skillMd).isFile()) {
    return { status: 'error', reason: `${dir} is not a skill directory (missing SKILL.md)` };
  }
  const text = readFileSync(skillMd, 'utf8');
  const fm = parseFrontmatter(text);
  const name = valueOf(fm.blocks.find((b) => b.key === 'name')) || basename(root);
  const description = valueOf(fm.blocks.find((b) => b.key === 'description'));
  const linked = [];
  for (const l of localLinks(text)) {
    const target = join(root, l);
    if (existsSync(target)) linked.push(relative(root, target));
  }
  const files = walkFiles(root).map((p) => relative(root, p));
  return {
    status: 'ok',
    dir: root,
    name,
    description,
    bodyChars: fm.body.length,
    linked,
    files,
  };
}

export function mergeSkills({ sources, name, out } = {}) {
  if (!sources || sources.length < 2) {
    return { status: 'error', reason: 'merge needs two or more skill directories' };
  }
  const skills = [];
  for (const dir of sources) {
    const r = readSkillDir(dir);
    if (r.status === 'error') return r;
    skills.push(r);
  }
  const proposedName = name ?? slugify(skills.map((s) => s.name).join('-'));
  return {
    status: 'ok',
    proposedName,
    out: out ? resolve(out) : null,
    sources: skills,
    note: 'Sources are not deleted. Write the new skill only after the outline is approved. Do not overwrite an existing skill unless asked.',
  };
}

function parseArgs(argv) {
  const sources = [];
  const opts = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') opts.json = true;
    else if (a === '--name' || a === '--out') {
      if (argv[i + 1] === undefined) throw new Error(`${a} needs a value`);
      opts[a.slice(2)] = argv[++i];
    } else if (a.startsWith('--')) {
      throw new Error(`unknown flag ${a}`);
    } else sources.push(a);
  }
  return { sources, opts };
}

function format(result) {
  if (result.status === 'error') return `error ${result.reason}`;
  const lines = [
    `merge outline → ${result.proposedName}`,
    result.out ? `  would write under ${result.out}/${result.proposedName}/` : '  pass --out <skills-dir> to name the destination',
    `  ${result.note}`,
  ];
  for (const s of result.sources) {
    lines.push(`  source ${s.name} (${s.dir})`);
    lines.push(`    description: ${s.description || '(none)'}`);
    lines.push(`    linked: ${s.linked.join(', ') || '(none)'}`);
  }
  return lines.join('\n');
}

function main() {
  let parsed;
  try {
    parsed = parseArgs(process.argv.slice(2));
  } catch (e) {
    console.error(`merge: ${e.message}`);
    process.exit(2);
  }
  if (parsed.sources.length < 2) {
    console.error('usage: merge.mjs <skill-dir...> [--name <name>] [--out <skills-dir>] [--json]');
    process.exit(2);
  }
  const result = mergeSkills({ sources: parsed.sources, name: parsed.opts.name, out: parsed.opts.out });
  if (parsed.opts.json) console.log(JSON.stringify(result, null, 2));
  else console.log(format(result));
  if (result.status !== 'ok') process.exit(1);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) main();
