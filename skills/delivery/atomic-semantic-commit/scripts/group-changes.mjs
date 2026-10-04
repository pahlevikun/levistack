#!/usr/bin/env node
// Propose a starting grouping of the working-tree changes: one group per context and kind.
//
//   node group-changes.mjs [dir] [--json]
//
// This is a hint, not a plan. It groups by path. It cannot tell a feature from a fix or a refactor,
// so code groups show the type as "?". Read the diff and decide.
import { execFileSync } from 'node:child_process';
import { readFileSync, statSync } from 'node:fs';
import { basename, extname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const git = (dir, args) => execFileSync('git', ['-C', dir, ...args], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });

const CONTAINER_ROOTS = new Set(['apps', 'packages', 'crates', 'services', 'libs', 'modules']);
const PLAIN_ROOTS = new Set(['src', 'lib', 'app', 'pkg', 'internal', 'cmd', 'test', 'tests', '__tests__', 'spec', 'specs']);
const LOCKFILES = /(^|\/)(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|mix\.lock|go\.sum|Cargo\.lock|Gemfile\.lock|poetry\.lock|uv\.lock|composer\.lock)$/;
const BUILD = /(^|\/)(package\.json|mix\.exs|go\.mod|Cargo\.toml|Gemfile|pyproject\.toml|requirements[^/]*\.txt|pom\.xml|build\.gradle(\.kts)?|Makefile|Dockerfile|docker-compose[^/]*\.ya?ml|tsconfig[^/]*\.json|webpack[^/]*|vite[^/]*|rollup[^/]*)$/;
const CI = /^(\.github\/|\.gitlab-ci\.yml|\.circleci\/|Jenkinsfile|\.buildkite\/)/;
const DOCS = /(^docs?\/|(^|\/)(README|CHANGELOG|CONTRIBUTING|LICENSE|SECURITY)[^/]*$|\.(md|mdx|rst|adoc)$)/i;
const TEST = /(^|\/)(tests?|__tests__|specs?)\/|(_test|_spec|\.test|\.spec)\.[a-z]+$/i;
const DOTFILE = /(^|\/)\.(gitignore|gitattributes|editorconfig|prettierrc[^/]*|eslintrc[^/]*|eslintignore|prettierignore|nvmrc|tool-versions|npmrc)$/;
const DANGER = /(^|\/)(\.env(\.[^/]+)?|id_rsa|id_ed25519|[^/]+\.(pem|key|p12|pfx)|\.DS_Store|[^/]+\.log)$|(^|\/)(node_modules|dist|build|coverage|_build|deps|\.next|target)\//;

export function classify(path) {
  if (DANGER.test(path)) return 'danger';
  if (CI.test(path)) return 'ci';
  if (LOCKFILES.test(path) || BUILD.test(path)) return 'build';
  if (DOTFILE.test(path)) return 'chore';
  if (TEST.test(path)) return 'test';
  if (DOCS.test(path)) return 'docs';
  return 'source';
}

// Directory segments of the context, after the usual source roots are stripped.
export function contextOf(path, repoName = '') {
  const parts = path.split('/');
  parts.pop();
  let segs = parts;
  const norm = (s) => s.toLowerCase().replace(/-/g, '_');
  while (segs.length) {
    const head = segs[0];
    if (CONTAINER_ROOTS.has(head) && segs[1]) return segs.slice(1);
    if (PLAIN_ROOTS.has(head) || (repoName && norm(head) === norm(repoName))) segs = segs.slice(1);
    else break;
  }
  return segs;
}

export function scopeOf(path, repoName = '') {
  const parts = path.split('/');
  const file = parts.pop();
  let segs = parts;
  const norm = (s) => s.toLowerCase().replace(/-/g, '_');
  while (segs.length) {
    const head = segs[0];
    if (CONTAINER_ROOTS.has(head) && segs[1]) return segs[1];
    if (PLAIN_ROOTS.has(head) || (repoName && norm(head) === norm(repoName))) segs = segs.slice(1);
    else break;
  }
  if (segs.length) return segs[0];
  const stem = basename(file, extname(file)).replace(/([._-])?(test|spec)$/i, '');
  return stem && !/^(index|main|mod|app)$/i.test(stem) ? stem : null;
}

function readChanges(dir) {
  const out = git(dir, ['status', '--porcelain=v1', '-z', '--untracked-files=all']);
  const parts = out.split('\0').filter(Boolean);
  const entries = [];
  for (let i = 0; i < parts.length; i++) {
    const rec = parts[i];
    const x = rec[0];
    const y = rec[1];
    const path = rec.slice(3);
    if (x === 'R' || x === 'C') i++; // the old name follows
    entries.push({ path, x, y, untracked: x === '?' });
  }
  const stats = new Map();
  const addStats = (text) => {
    for (const line of text.split('\n')) {
      const m = line.match(/^(\d+|-)\t(\d+|-)\t(.+)$/);
      if (!m) continue;
      const cur = stats.get(m[3]) ?? { added: 0, deleted: 0, binary: false };
      if (m[1] === '-') cur.binary = true;
      else {
        cur.added += Number(m[1]);
        cur.deleted += Number(m[2]);
      }
      stats.set(m[3], cur);
    }
  };
  addStats(git(dir, ['diff', '--numstat']));
  addStats(git(dir, ['diff', '--cached', '--numstat']));
  for (const e of entries) {
    if (e.untracked && !stats.has(e.path)) {
      let added = 0;
      try {
        const p = join(dir, e.path);
        if (statSync(p).size < 1_000_000) added = readFileSync(p, 'utf8').split('\n').length;
      } catch {
        // unreadable or binary: leave at 0
      }
      stats.set(e.path, { added, deleted: 0, binary: false });
    }
  }
  return entries.map((e) => ({ ...e, ...(stats.get(e.path) ?? { added: 0, deleted: 0, binary: false }) }));
}

export function group(entries, repoName = '') {
  const groups = new Map();
  const skipped = [];
  for (const e of entries) {
    const kind = classify(e.path);
    if (kind === 'danger') {
      skipped.push(e);
      continue;
    }
    const scope = kind === 'source' || kind === 'test' ? scopeOf(e.path, repoName) : null;
    const key = kind === 'source' || kind === 'test' ? `code:${scope ?? ''}` : kind;
    if (!groups.has(key)) groups.set(key, { key, kind: kind === 'test' ? 'code' : kind === 'source' ? 'code' : kind, scope, files: [] });
    groups.get(key).files.push({ ...e, kind });
  }
  const MAX_GROUP = 8;
  const refined = [];
  const split = (g, depth) => {
    if (g.files.length <= MAX_GROUP || depth >= 4) return [g];
    const sub = new Map();
    for (const f of g.files) {
      const ctx = contextOf(f.path, repoName);
      const k = ctx.slice(0, depth).join('/') || '(root)';
      if (!sub.has(k)) sub.set(k, []);
      sub.get(k).push(f);
    }
    if (sub.size < 2) return depth + 1 <= 4 ? split(g, depth + 1) : [g];
    return [...sub.entries()].flatMap(([k, files]) => split({ ...g, key: `${g.key.split(':')[0]}:${k}`, scope: k.split('/').pop(), context: k, files }, depth + 1));
  };
  for (const g of groups.values()) {
    if (g.kind === 'code') refined.push(...split(g, 2));
    else refined.push(g);
  }
  const list = refined.map((g) => {
    const kinds = new Set(g.files.map((f) => f.kind));
    let type = '?';
    let hint = 'feat | fix | refactor | style';
    if (g.kind === 'docs') ([type, hint] = ['docs', '']);
    else if (g.kind === 'ci') ([type, hint] = ['ci', 'chore if the repository does not use "ci"']);
    else if (g.kind === 'build') ([type, hint] = ['build', 'chore if the repository does not use "build"']);
    else if (g.kind === 'chore') ([type, hint] = ['chore', '']);
    else if (kinds.size === 1 && kinds.has('test')) ([type, hint] = ['test', '']);
    const notes = [];
    if (g.kind === 'docs' && g.files.length > 20) notes.push(`${g.files.length} Markdown files. If they are the product (skills, rules, prompts) and not documentation, regroup them by context and use feat, fix or refactor`);
    const big = g.files.filter((f) => f.added > 0 && f.deleted > 0 && f.added + f.deleted > 300);
    for (const f of big.slice(0, 3)) notes.push(`${f.path}: ${f.added + f.deleted} changed lines (edited, not moved). Check whether it holds two purposes (git add -p)`);
    if (big.length > 3) notes.push(`${big.length - 3} more edited files with over 300 changed lines`);
    for (const f of g.files) {
      if (f.x !== ' ' && f.x !== '?' && f.y !== ' ' && f.y !== '?') notes.push(`${f.path}: part is staged and part is not`);
      if (f.binary) notes.push(`${f.path}: binary file`);
    }
    return {
      group: g.key,
      scope: g.scope,
      context: g.context ?? g.scope,
      kind: g.kind,
      suggestedType: type,
      typeHint: hint,
      files: g.files.map((f) => ({ path: f.path, status: `${f.x}${f.y}`.trim() || '?', added: f.added, deleted: f.deleted })),
      added: g.files.reduce((n, f) => n + f.added, 0),
      deleted: g.files.reduce((n, f) => n + f.deleted, 0),
      notes,
    };
  });
  const order = { build: 0, ci: 1, code: 2, docs: 3, chore: 4 };
  list.sort((a, b) => (order[a.kind] ?? 9) - (order[b.kind] ?? 9) || a.group.localeCompare(b.group));
  return { groups: list, skipped: skipped.map((e) => e.path) };
}

export function analyze(dirArg) {
  const dir = resolve(dirArg);
  const top = git(dir, ['rev-parse', '--show-toplevel']).trim();
  const entries = readChanges(top);
  return { root: top, changed: entries.length, ...group(entries, basename(top)) };
}

function format(r) {
  const lines = [`${r.changed} changed file(s) in ${r.groups.length} group(s) under ${r.root}`, 'A starting point, not a plan. Read the diff before you decide the types.', ''];
  if (!r.groups.length && !r.skipped.length) lines.push('The working tree is clean.');
  r.groups.forEach((g, i) => {
    const label = g.context ? `${g.kind}: ${g.context}` : g.kind;
    lines.push(`${i + 1}. ${label} (${g.files.length} file${g.files.length === 1 ? '' : 's'}, +${g.added} -${g.deleted})  type: ${g.suggestedType}${g.typeHint ? ` (${g.typeHint})` : ''}`);
    for (const f of g.files) lines.push(`   ${f.status.padEnd(2)} ${f.path}  +${f.added} -${f.deleted}`);
    for (const n of g.notes) lines.push(`   note: ${n}`);
  });
  if (r.skipped.length) {
    lines.push('', 'Do not commit these (secrets, build output, logs, junk):');
    for (const p of r.skipped) lines.push(`   ${p}`);
  }
  if (r.groups.length === 1) lines.push('', 'One group: likely one commit, unless the diff holds two purposes.');
  else if (r.groups.length > 1) lines.push('', 'Tests stay with the code they test. Dependency order decides the commit order.');
  return lines.join('\n');
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const args = process.argv.slice(2);
  const dir = args.find((a) => !a.startsWith('--')) ?? '.';
  try {
    const r = analyze(dir);
    console.log(args.includes('--json') ? JSON.stringify(r, null, 2) : format(r));
  } catch (e) {
    console.error(`group-changes: ${String(e.message).split('\n')[0]}`);
    process.exit(2);
  }
}
