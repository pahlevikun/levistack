#!/usr/bin/env node
// Read-only helper for the enhance-skill use case. It inventories the target skill, checks that the
// scratch folder is ignored by git, and prints the commands that fetch each source. It never clones or writes.
//
//   node enhance.mjs <skill-dir> [--source <url|dir>...] [--scratch <folder>] [--json]
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, realpathSync } from 'node:fs';
import { dirname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { readSkillDir } from './merge.mjs';

const slug = (s) => s.toLowerCase().replace(/[^a-z0-9.]+/g, '-').replace(/^-+|-+$/g, '');

/** Describe one source and the command that fetches it. */
export function parseSource(src, scratch) {
  if (!/^https?:\/\//i.test(src)) {
    const ok = existsSync(src);
    return { source: src, kind: ok ? 'dir' : 'missing', fetch: null, note: ok ? 'read in place' : 'the path does not exist. Check it' };
  }
  let u;
  try {
    u = new URL(src);
  } catch {
    return { source: src, kind: 'bad-url', fetch: null, note: 'not a valid URL' };
  }
  const parts = u.pathname.split('/').filter(Boolean);
  if (u.hostname === 'github.com' && parts.length >= 2) {
    const [owner, repo] = parts;
    const dest = `${scratch}/${slug(owner)}__${slug(repo.replace(/\.git$/, ''))}`;
    const focus = parts.length > 4 && (parts[2] === 'tree' || parts[2] === 'blob') ? parts.slice(4).join('/') : null;
    return { source: src, kind: 'github', fetch: `git clone --depth 1 https://github.com/${owner}/${repo.replace(/\.git$/, '')}.git ${dest}`, dest, focus, note: focus ? `read ${focus} first, then every file it points to` : 'read the main skill file, then every reference' };
  }
  if (/(^|\.)skills\.sh$/.test(u.hostname) && parts.length >= 3) {
    const [owner, repo, skill] = parts;
    const dest = `${scratch}/${slug(owner)}__${slug(repo)}`;
    return { source: src, kind: 'skills.sh', fetch: `git clone --depth 1 https://github.com/${owner}/${repo}.git ${dest}`, dest, focus: skill, note: `a skills.sh page. The repo is a guess from the path. Find the skill named "${skill}" inside it` };
  }
  const dest = `${scratch}/singles/${slug(u.hostname + u.pathname)}`;
  return { source: src, kind: 'page', fetch: `curl -sL ${src} -o ${dest}`, dest, note: 'a single page. Save it, then read it to the end' };
}

/** The real path of a path that may not exist yet: resolve the nearest existing parent, then add the rest. */
function realish(p) {
  let cur = resolve(p);
  const rest = [];
  while (!existsSync(cur) && dirname(cur) !== cur) {
    rest.unshift(cur.slice(dirname(cur).length + 1));
    cur = dirname(cur);
  }
  return join(realpathSync(cur), ...rest);
}

function gitInfo(path) {
  try {
    const root = execFileSync('git', ['-C', path, 'rev-parse', '--show-toplevel'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
    return realpathSync(root);
  } catch {
    return null;
  }
}

/** Is the scratch folder safe to fetch into? Outside the repo is fine. Inside it must be ignored. */
export function scratchStatus(scratch, repoRoot) {
  if (!repoRoot) return { inside: false, ignored: null, ok: true, note: 'the target is not in a git repository' };
  const rel = relative(realpathSync(repoRoot), realish(scratch));
  if (rel === '' || rel === '..' || rel.startsWith('..' + sep) || resolve(rel) === rel) return { inside: false, ignored: null, ok: true, note: 'the scratch folder is outside the repository' };
  try {
    execFileSync('git', ['-C', repoRoot, 'check-ignore', '-q', rel + '/'], { stdio: 'ignore' });
    return { inside: true, ignored: true, ok: true, note: 'ignored by git' };
  } catch {
    return { inside: true, ignored: false, ok: false, note: `NOT ignored by git. Add "${rel}/" to .gitignore before you fetch anything` };
  }
}

export function plan({ target, sources = [], scratch } = {}) {
  const t = readSkillDir(target);
  if (t.status !== 'ok') return t;
  const root = gitInfo(t.dir);
  const scratchDir = scratch || (root ? `${root}/scratch/${slug(t.name)}-sources` : `${dirname(t.dir)}/scratch/${slug(t.name)}-sources`);
  const skillMd = readFileSync(`${t.dir}/SKILL.md`, 'utf8');
  const groups = {};
  for (const f of t.files) {
    const top = f.includes('/') ? f.split('/')[0] : '(root)';
    groups[top] = (groups[top] || 0) + 1;
  }
  const warnings = [];
  if (skillMd.split('\n').length > 450) warnings.push(`SKILL.md has ${skillMd.split('\n').length} lines. The limit is 500, so new depth must go to references`);
  if ((t.description || '').length > 900) warnings.push(`the description is ${(t.description || '').length} characters. The limit is 1024, so a scope change must stay short`);
  const sc = scratchStatus(scratchDir, root);
  if (!sc.ok) warnings.push(sc.note);
  if (!sources.length) warnings.push('no source given. Pass --source <url-or-dir>');
  return {
    status: 'ok',
    target: { name: t.name, dir: t.dir, lines: skillMd.split('\n').length, descriptionChars: (t.description || '').length, files: t.files.length, groups },
    scratch: { dir: scratchDir, ...sc },
    sources: sources.map((s) => parseSource(s, scratchDir)),
    map: 'templates/enhance-map.md',
    warnings,
  };
}

function parseArgs(argv) {
  const o = { target: null, sources: [], scratch: null, json: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') o.json = true;
    else if (a === '--source') o.sources.push(argv[++i]);
    else if (a === '--scratch') o.scratch = argv[++i];
    else if (a.startsWith('--')) throw new Error(`unknown flag ${a}`);
    else if (!o.target) o.target = a;
    else throw new Error('one target skill only. Use merge.mjs for two skills');
  }
  return o;
}

function main() {
  let o;
  try {
    o = parseArgs(process.argv.slice(2));
  } catch (e) {
    console.error(`enhance: ${e.message}`);
    process.exit(2);
  }
  if (!o.target) {
    console.error('usage: enhance.mjs <skill-dir> [--source <url|dir>...] [--scratch <folder>] [--json]');
    process.exit(2);
  }
  const r = plan({ target: o.target, sources: o.sources, scratch: o.scratch });
  if (r.status !== 'ok') {
    console.error(`enhance: ${r.reason}`);
    process.exit(2);
  }
  if (o.json) return console.log(JSON.stringify(r, null, 2));
  console.log(`target   ${r.target.name} (${r.target.lines} lines, description ${r.target.descriptionChars} chars, ${r.target.files} files)`);
  console.log(`folders  ${Object.entries(r.target.groups).map(([k, v]) => `${k}:${v}`).join(' ')}`);
  console.log(`scratch  ${r.scratch.dir} (${r.scratch.note})`);
  for (const s of r.sources) console.log(`source   ${s.kind.padEnd(9)} ${s.source}\n         ${s.fetch ? '$ ' + s.fetch : ''}\n         ${s.note}`);
  for (const w of r.warnings) console.log(`warning  ${w}`);
  console.log(`next     fill ${r.map}, show it to the user, then write the additions`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) main();
