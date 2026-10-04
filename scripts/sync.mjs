#!/usr/bin/env node
// Generates every manifest from the folder tree. Run `npm run sync`; CI runs `--check`.
import { existsSync, lstatSync, mkdirSync, readdirSync, readFileSync, readlinkSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { scanTree } from './lib/tree.mjs';

const json = (o) => JSON.stringify(o, null, 2) + '\n';
const START = '<!-- groups:start -->';
const END = '<!-- groups:end -->';

// Claude Code reads `.claude/*`; this repo keeps `.cursor/*` as the source tree.
export const CLAUDE_CURSOR_LINKS = [
  ['.claude/agents', '../.cursor/agents'],
  ['.claude/rules', '../.cursor/rules'],
  ['.claude/skills', '../.cursor/skills'],
];

function linkStat(p) {
  try {
    return lstatSync(p);
  } catch {
    return null;
  }
}

export function diffClaudeCursorLinks(root) {
  if (!existsSync(join(root, '.cursor', 'agents'))) return [];
  const drift = [];
  for (const [rel, target] of CLAUDE_CURSOR_LINKS) {
    const p = join(root, rel);
    const st = linkStat(p);
    if (!st) drift.push(`missing link: ${rel}`);
    else if (!st.isSymbolicLink()) drift.push(`not a symlink: ${rel}`);
    else if (readlinkSync(p) !== target) drift.push(`link target: ${rel} (want ${target})`);
  }
  return drift;
}

export function writeClaudeCursorLinks(root) {
  if (!existsSync(join(root, '.cursor', 'agents'))) return;
  for (const [rel, target] of CLAUDE_CURSOR_LINKS) {
    const p = join(root, rel);
    const st = linkStat(p);
    if (st?.isSymbolicLink() && readlinkSync(p) === target) continue;
    if (st) rmSync(p, { recursive: true, force: true });
    mkdirSync(dirname(p), { recursive: true });
    symlinkSync(target, p);
  }
}

export function build(root) {
  const pkg = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8'));
  const tree = scanTree(root);
  const groups = tree.groups.filter((g) => g.skills.length);
  const out = new Map();

  const common = { version: pkg.version, description: pkg.description, author: pkg.author, license: pkg.license };

  // Claude Code: one plugin per group (rooted at the group dir) plus one for everything.
  for (const g of groups) {
    out.set(
      `skills/${g.name}/.claude-plugin/plugin.json`,
      json({
        name: `levistack-${g.name}`,
        version: pkg.version,
        description: g.description,
        author: pkg.author,
        license: pkg.license,
        skills: g.skills.map((s) => `./${s.name}`),
      }),
    );
  }
  out.set(
    '.claude-plugin/plugin.json',
    json({
      name: 'levistack',
      ...common,
      skills: groups.flatMap((g) => g.skills.map((s) => `./skills/${g.name}/${s.name}`)),
    }),
  );
  out.set(
    '.claude-plugin/marketplace.json',
    json({
      name: 'levistack',
      owner: pkg.author,
      metadata: { description: pkg.description },
      plugins: [
        { name: 'levistack', source: './', description: 'Every group: all skills, agents, commands and opt-in hooks.' },
        ...groups.map((g) => ({
          name: `levistack-${g.name}`,
          source: `./skills/${g.name}`,
          description: g.description,
        })),
      ],
    }),
  );

  // Cursor: one plugin; rules are converted from rules/*.md to .mdc.
  out.set(
    '.cursor-plugin/plugin.json',
    json({
      name: 'levistack',
      displayName: 'Levistack',
      ...common,
      keywords: ['skills', 'rules', 'agents', 'personal'],
      skills: './skills/',
      agents: './agents/',
      rules: './generated/cursor/rules/',
    }),
  );
  out.set(
    '.cursor-plugin/marketplace.json',
    json({
      name: 'levistack',
      owner: pkg.author,
      plugins: [{ name: 'levistack', source: './', description: pkg.description }],
    }),
  );
  for (const r of tree.rules) {
    const dest = `generated/cursor/rules/${r.slug}.mdc`;
    if (r.ext === '.mdc') {
      out.set(dest, r.raw); // already Cursor format: pass through unchanged
      continue;
    }
    const lines = [`description: ${JSON.stringify(r.fm.description ?? '')}`];
    if (r.fm.globs) lines.push(`globs: ${JSON.stringify(r.fm.globs)}`);
    lines.push(`alwaysApply: ${r.fm.alwaysApply ?? 'false'}`);
    out.set(dest, `---\n${lines.join('\n')}\n---\n<!-- generated from rules/${r.file}; do not edit -->\n${r.body}`);
  }

  // Codex
  out.set(
    '.codex-plugin/plugin.json',
    json({
      name: 'levistack',
      ...common,
      skills: './skills/',
      interface: { displayName: 'Levistack', shortDescription: pkg.description, category: 'Productivity' },
    }),
  );

  // README group table
  const readmePath = join(root, 'README.md');
  if (existsSync(readmePath)) {
    const readme = readFileSync(readmePath, 'utf8');
    const a = readme.indexOf(START);
    const b = readme.indexOf(END);
    if (a !== -1 && b > a) {
      const rows = groups.map(
        (g) => `| \`${g.name}\` | ${g.description} | ${g.skills.map((s) => `\`${s.name}\``).join(', ')} |`,
      );
      const table = ['| Group | About | Skills |', '|---|---|---|', ...rows].join('\n');
      out.set('README.md', `${readme.slice(0, a + START.length)}\n${table}\n${readme.slice(b)}`);
    }
  }
  return out;
}

// Generated files on disk that the current tree no longer produces.
export function staleFiles(root, out) {
  const stale = [];
  const skillsDir = join(root, 'skills');
  if (existsSync(skillsDir)) {
    for (const g of readdirSync(skillsDir)) {
      const rel = `skills/${g}/.claude-plugin/plugin.json`;
      if (existsSync(join(root, rel)) && !out.has(rel)) stale.push(rel);
    }
  }
  const rulesDir = join(root, 'generated/cursor/rules');
  if (existsSync(rulesDir)) {
    for (const f of readdirSync(rulesDir)) {
      const rel = `generated/cursor/rules/${f}`;
      if (!out.has(rel)) stale.push(rel);
    }
  }
  return stale;
}

// Returns human-readable drift lines; empty when the tree is in sync.
export function diffGenerated(root) {
  const out = build(root);
  const drift = [];
  for (const [rel, content] of out) {
    const p = join(root, rel);
    if (!existsSync(p)) drift.push(`missing: ${rel}`);
    else if (readFileSync(p, 'utf8') !== content) drift.push(`out of date: ${rel}`);
  }
  for (const rel of staleFiles(root, out)) drift.push(`stale: ${rel}`);
  drift.push(...diffClaudeCursorLinks(root));
  return drift;
}

export function writeGenerated(root) {
  const out = build(root);
  for (const [rel, content] of out) {
    const p = join(root, rel);
    mkdirSync(dirname(p), { recursive: true });
    writeFileSync(p, content);
  }
  writeClaudeCursorLinks(root);
  for (const rel of staleFiles(root, out)) rmSync(join(root, rel));
  return out;
}

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  // hooks/hooks.json and the hooks README table come from each hook's `meta` (async: it imports the hooks).
  const hooks = await import('../hooks/lib/generate.mjs');
  if (process.argv.includes('--check')) {
    const drift = [...diffGenerated(root), ...(await hooks.diffHooks(root))];
    if (drift.length) {
      console.error(`Generated files are out of sync. Run \`npm run sync\`.\n${drift.map((d) => `  ${d}`).join('\n')}`);
      process.exit(1);
    }
    console.log('sync: up to date');
  } else {
    const out = writeGenerated(root);
    const hookOut = await hooks.writeHooks(root);
    console.log(`sync: wrote ${out.size + hookOut.size} files`);
    for (const rel of [...out.keys(), ...hookOut.keys()]) console.log(`  ${relative(root, join(root, rel))}`);
  }
}
