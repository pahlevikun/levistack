#!/usr/bin/env node
// Audit how the skills in a catalog connect to each other.
//
//   node links.mjs [--root <skills dir>] [--json]
//
// "## Related skills" is optional. A skill may have none.
// Errors (exit 1):
//   - a backticked name in a Related skills section is not a skill in the catalog
//   - a skill is missing from references/routing.md, so find-skills cannot route to it
// Notes (exit 0): one-way links, and skills no other skill points at.
// Nested skills (a skill folder inside a skill) count as catalog skills.
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const SELF = 'find-skills';
const NAME = /^name:\s*["']?([^"'\n]+?)["']?\s*$/m;

function* walk(dir) {
  for (const n of readdirSync(dir).sort()) {
    if (n.startsWith('.') || n === 'node_modules') continue;
    const p = join(dir, n);
    if (statSync(p).isDirectory()) yield* walk(p);
    else if (n === 'SKILL.md') yield p;
  }
}

export function related(text) {
  const m = text.match(/^## Related skills\s*\n([\s\S]*?)(?=^## |(?![\s\S]))/m);
  if (!m) return null;
  return [...m[1].matchAll(/^\s*[-*]\s+`([a-z0-9][a-z0-9-]*)`/gm)].map((x) => x[1]);
}

export function audit(root, routingFile) {
  const skills = new Map();
  for (const file of walk(root)) {
    const text = readFileSync(file, 'utf8');
    const name = NAME.exec(text)?.[1];
    if (name) skills.set(name, { file, links: related(text) });
  }
  const routing = existsSync(routingFile) ? readFileSync(routingFile, 'utf8') : '';
  const errors = [];
  const notes = [];
  const inbound = new Map([...skills.keys()].map((n) => [n, new Set()]));

  for (const [name, s] of skills) {
    for (const to of s.links ?? []) {
      if (!skills.has(to)) errors.push(`${name}: related skill "${to}" is not in the catalog`);
      else if (to !== name) inbound.get(to).add(name);
    }
    if (name !== SELF && !new RegExp('`' + name + '`').test(routing)) errors.push(`${name}: missing from references/routing.md`);
  }
  for (const [name, s] of skills) {
    for (const to of s.links ?? []) {
      if (skills.has(to) && !(skills.get(to).links ?? []).includes(name)) notes.push(`one-way: ${name} -> ${to}`);
    }
    if (name !== SELF && !inbound.get(name).size) notes.push(`no inbound link: ${name}`);
  }
  return { skills: [...skills.keys()], errors, notes };
}

function main(argv) {
  let root = null;
  let json = false;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--root') root = resolve(argv[++i] ?? '');
    else if (argv[i] === '--json') json = true;
  }
  root ??= [join(HERE, '../../..'), join(process.cwd(), 'skills')].find((d) => existsSync(d) && basename(resolve(d)) === 'skills');
  if (!root) {
    console.error('no skills directory found; pass --root');
    process.exit(2);
  }
  const result = audit(root, join(HERE, '../references/routing.md'));
  if (json) console.log(JSON.stringify(result, null, 2));
  else {
    console.log(`${result.skills.length} skills, ${result.errors.length} errors, ${result.notes.length} notes`);
    for (const e of result.errors) console.log(`error: ${e}`);
    for (const n of result.notes) console.log(`note: ${n}`);
  }
  process.exit(result.errors.length ? 1 : 0);
}

if (import.meta.url === `file://${process.argv[1]}`) main(process.argv.slice(2));
