#!/usr/bin/env node
// Search skills that are already on this machine.
//
//   node catalog.mjs [query words] [--root <dir>]... [--limit N] [--json] [--self]
//
// Default roots, local first: ./skills (grouped catalog), ./.cursor/skills, ./.claude/skills,
// ./.agents/skills, ~/.claude/skills, ~/.agents/skills. Pass --root to use only the roots you name.
// With no query it lists every skill. The first skill seen under a name wins.
// Each hit says how to run it: `loaded` skills sit in a folder the host registers, so the Skill tool can
// invoke them by name. The others (the grouped ./skills catalog, custom --root) are file-only: read the
// SKILL.md and follow it. A skill reached through both, such as a symlink, counts as loaded.
// find-skills never lists itself; pass --self to include it.
import { existsSync, readdirSync, readFileSync, realpathSync, statSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, resolve } from 'node:path';

const MAX_DEPTH = 2; // <root>/<name>/SKILL.md or <root>/<group>/<name>/SKILL.md
const STOP = new Set(['the', 'a', 'an', 'to', 'of', 'for', 'and', 'or', 'in', 'on', 'my', 'me', 'i', 'it', 'is', 'we', 'with', 'that', 'this', 'want', 'need', 'please']);

export function defaultRoots(cwd = process.cwd(), home = homedir()) {
  return [
    { dir: join(cwd, 'skills'), loaded: false },
    { dir: join(cwd, '.cursor/skills'), loaded: true },
    { dir: join(cwd, '.claude/skills'), loaded: true },
    { dir: join(cwd, '.agents/skills'), loaded: true },
    { dir: join(home, '.claude/skills'), loaded: true },
    { dir: join(home, '.agents/skills'), loaded: true },
  ];
}

export function readSkill(file) {
  const m = readFileSync(file, 'utf8').match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return null;
  const lines = m[1].split(/\r?\n/);
  const out = {};
  for (let i = 0; i < lines.length; i++) {
    const kv = lines[i].match(/^(name|description):\s*(.*)$/);
    if (!kv) continue;
    let v = kv[2].trim();
    if (/^[>|][+-]?$/.test(v)) {
      const parts = [];
      while (i + 1 < lines.length && /^\s+\S/.test(lines[i + 1])) parts.push(lines[++i].trim());
      v = parts.join(' ');
    } else if (/^(".*"|'.*')$/.test(v)) {
      v = v.slice(1, -1);
    }
    out[kv[1]] = v;
  }
  return out.name ? out : null;
}

function* skillFiles(dir, depth = 1) {
  if (!existsSync(dir) || !statSync(dir).isDirectory()) return;
  if (existsSync(join(dir, 'SKILL.md'))) {
    yield join(dir, 'SKILL.md');
    return; // do not descend into a skill: nested folders are its own references
  }
  if (depth > MAX_DEPTH) return;
  for (const n of readdirSync(dir).sort()) {
    if (n.startsWith('.') || n === 'node_modules') continue;
    yield* skillFiles(join(dir, n), depth + 1);
  }
}

// roots: directory strings (file-only) or { dir, loaded } objects.
export function collect(roots) {
  const byReal = new Map();
  const names = new Set();
  const skills = [];
  for (const r of roots) {
    const { dir: root, loaded = false } = typeof r === 'string' ? { dir: r } : r;
    if (!existsSync(root)) continue;
    for (const dir of readdirSync(root).sort()) {
      if (dir.startsWith('.')) continue;
      for (const file of skillFiles(join(root, dir), 1)) {
        const real = realpathSync(file);
        if (byReal.has(real)) {
          if (loaded) byReal.get(real).loaded = true;
          continue;
        }
        const fm = readSkill(file);
        if (!fm || names.has(fm.name)) continue;
        names.add(fm.name);
        const skill = { name: fm.name, description: fm.description ?? '', path: file, root, loaded };
        byReal.set(real, skill);
        skills.push(skill);
      }
    }
  }
  return skills.map((s) => ({ ...s, invoke: s.loaded ? `Skill tool: ${s.name}` : `read ${s.path} and follow it` }));
}

const stem = (w) => (w.length > 4 ? w.replace(/(ing|ed|es|s)$/, '') : w);
export const tokens = (q) => [...new Set(q.toLowerCase().split(/[^a-z0-9]+/).filter((w) => w.length > 1 && !STOP.has(w)).map(stem))];

export function rank(skills, query) {
  const toks = tokens(query);
  if (!toks.length) return skills.map((s) => ({ ...s, score: 0 }));
  return skills
    .map((s) => {
      const name = s.name.toLowerCase();
      const desc = s.description.toLowerCase();
      let score = 0;
      for (const t of toks) {
        if (name === t) score += 6;
        else if (name.includes(t)) score += 3;
        if (new RegExp(`\\b${t}`).test(desc)) score += 1;
      }
      return { ...s, score };
    })
    .filter((s) => s.score > 0)
    .sort((a, b) => b.score - a.score || a.name.localeCompare(b.name));
}

function main(argv) {
  const words = [];
  const roots = [];
  let limit = 10;
  let json = false;
  let self = false;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--root') roots.push(resolve(argv[++i] ?? ''));
    else if (argv[i] === '--limit') limit = Number(argv[++i]) || limit;
    else if (argv[i] === '--json') json = true;
    else if (argv[i] === '--self') self = true;
    else words.push(argv[i]);
  }
  const query = words.join(' ');
  const all = collect(roots.length ? roots : defaultRoots()).filter((s) => self || s.name !== 'find-skills');
  const found = rank(all, query);
  const shown = query ? found.slice(0, limit) : found;
  if (json) {
    console.log(JSON.stringify(shown, null, 2));
    return;
  }
  if (!shown.length) {
    console.log(`no local skill matches "${query}"`);
    return;
  }
  for (const s of shown) {
    const first = s.description.split(/(?<=[.!?])\s/)[0].slice(0, 160);
    console.log(`${query ? `${s.score}\t` : ''}${s.name}\t${s.loaded ? 'loaded' : 'file-only'}\t${s.path}\n\t${first}`);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) main(process.argv.slice(2));
