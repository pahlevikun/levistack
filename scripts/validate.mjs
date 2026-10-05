#!/usr/bin/env node
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { scanTree } from './lib/tree.mjs';
import { diffGenerated } from './sync.mjs';

const MAX_DESC = 1024; // Agent Skills spec maximum
// Public repo guard: nothing employer-owned, no local paths, no obvious secrets.
// `hard` hits always fail. Soft hits are warnings during import cleanup and fail under --strict (publish gate).
// Built from parts so this file does not spell out the names it guards against.
const EMPLOYER_NAMES = new RegExp(
  ['go-?', 'jek|go', 'food|go', 'biz|go', 'pay|goto', 'company|toko', 'pedia|sauda', 'gar|nexo', 'cean'].join(''),
  'i',
);
const FORBIDDEN = [
  [/(api[_-]?key|secret|token|password)\s*[:=]\s*['"][A-Za-z0-9_\-]{16,}['"]/i, 'possible secret', true],
  [EMPLOYER_NAMES, 'employer identifier', false],
  [/teamharness|teamonia/i, 'teamonia tooling reference (not installable by others)', false],
  [/\/Users\/[A-Za-z0-9._-]+/, 'absolute local path', false],
];

function oneLine(desc) {
  return typeof desc === 'string' && desc.length > 0 && !['>', '|', '>-', '|-'].includes(desc);
}

function walkText(dir, acc = []) {
  if (!existsSync(dir)) return acc;
  for (const n of readdirSync(dir)) {
    if (n.startsWith('.')) continue;
    const p = join(dir, n);
    if (statSync(p).isDirectory()) walkText(p, acc);
    else if (/\.(md|mjs|json|sh|txt|ya?ml)$/.test(n)) acc.push(p);
  }
  return acc;
}

const PROVENANCE_MANIFESTS = new Set(['THIRD_PARTY.md', 'UPSTREAM.md']);

function findProvenanceManifests(root) {
  const hits = [];
  for (const name of PROVENANCE_MANIFESTS) {
    const atRoot = join(root, name);
    if (existsSync(atRoot)) hits.push(name);
  }
  for (const sub of ['skills', 'agents', 'rules', 'commands', 'hooks']) {
    const base = join(root, sub);
    if (!existsSync(base)) continue;
    for (const f of walkText(base)) {
      const baseName = f.slice(f.lastIndexOf('/') + 1);
      if (PROVENANCE_MANIFESTS.has(baseName)) hits.push(f.slice(root.length + 1));
    }
  }
  return hits;
}

export function validateTree(root, { strict = false } = {}) {
  const errors = [];
  const warnings = [];
  for (const rel of findProvenanceManifests(root)) {
    errors.push(
      `${rel}: remove import provenance manifests (see rules/core/no-third-party-md.md); keep LICENSE beside copied code only when the license requires it`,
    );
  }
  const tree = scanTree(root);

  for (const g of tree.groups) {
    if (!g.skills.length) {
      errors.push(`group "${g.name}": no skills (remove the folder or add a skill)`);
      continue;
    }
    if (!g.hasDescriptionFile) errors.push(`group "${g.name}": missing DESCRIPTION.md`);
    else if (!oneLine(g.description)) errors.push(`group "${g.name}": DESCRIPTION.md needs a one-line description`);
    if (g.descUnsafe.length) errors.push(`group "${g.name}": DESCRIPTION.md values must be quoted (${g.descUnsafe.join(', ')})`);
    for (const s of g.skills) {
      const id = `skill ${g.name}/${s.name}`;
      if (!s.hasFrontmatter) errors.push(`${id}: missing frontmatter`);
      if (s.unsafe.length) errors.push(`${id}: frontmatter values must be quoted (${s.unsafe.join(', ')}); unquoted ": " breaks YAML parsers`);
      if (s.fm.name !== s.name) errors.push(`${id}: name "${s.fm.name}" must equal folder name`);
      if (!oneLine(s.fm.description)) errors.push(`${id}: description must be a single line`);
      else if (s.fm.description.length > MAX_DESC) errors.push(`${id}: description over ${MAX_DESC} chars`);
    }
  }
  // Imported rules/agents often carry unquoted globs etc. Those parsers are lenient, so warn unless --strict.
  for (const x of [...tree.agents, ...tree.rules, ...tree.commands]) {
    if (x.unsafe.length) (strict ? errors : warnings).push(`${x.file}: frontmatter values should be quoted (${x.unsafe.join(', ')})`);
  }
  const slugs = new Map();
  for (const r of tree.rules) {
    if (slugs.has(r.slug)) errors.push(`rule ${r.name}: generated Cursor name "${r.slug}" collides with ${slugs.get(r.slug)}`);
    slugs.set(r.slug, r.name);
  }
  for (const a of tree.agents) {
    if (a.fm.name !== a.name) errors.push(`agent ${a.name}: name must equal file name`);
    if (!oneLine(a.fm.description)) errors.push(`agent ${a.name}: needs a one-line description`);
  }
  for (const r of tree.rules) if (!oneLine(r.fm.description)) errors.push(`rule ${r.name}: needs a one-line description`);
  for (const c of tree.commands) if (!oneLine(c.fm.description)) errors.push(`command ${c.name}: needs a one-line description`);

  const hooksJson = join(root, 'hooks/hooks.json');
  if (existsSync(hooksJson)) {
    let parsed;
    try {
      parsed = JSON.parse(readFileSync(hooksJson, 'utf8'));
    } catch (e) {
      errors.push(`hooks/hooks.json: invalid JSON (${e.message})`);
    }
    for (const m of JSON.stringify(parsed ?? {}).matchAll(/launcher\.mjs\\?"\s+([a-z0-9-]+)/g)) {
      if (!existsSync(join(root, `hooks/${m[1]}.mjs`))) errors.push(`hooks/hooks.json: hooks/${m[1]}.mjs does not exist`);
    }
  }

  // One language for hooks: Node. Shell scripts do not run on every platform and split the tooling.
  for (const f of walkText(join(root, 'hooks'))) {
    if (f.endsWith('.sh')) errors.push(`${f.slice(root.length + 1)}: hooks are Node (.mjs), not shell`);
  }

  for (const sub of ['skills', 'agents', 'rules', 'commands', 'hooks', 'statusline']) {
    for (const f of walkText(join(root, sub))) {
      const text = readFileSync(f, 'utf8');
      for (const [re, why, hard] of FORBIDDEN) {
        if (re.test(text)) (hard || strict ? errors : warnings).push(`${f.slice(root.length + 1)}: ${why}`);
      }
    }
  }

  errors.push(...diffGenerated(root).map((d) => `generated ${d}`));
  errors.warnings = warnings;
  return errors;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const root = join(dirname(fileURLToPath(import.meta.url)), '..');
  const errors = validateTree(root, { strict: process.argv.includes('--strict') });
  if (errors.warnings.length) {
    const byReason = {};
    for (const w of errors.warnings) {
      const why = w.slice(w.indexOf(': ') + 2);
      (byReason[why] ??= []).push(w.slice(0, w.indexOf(': ')));
    }
    for (const [why, files] of Object.entries(byReason)) {
      console.warn(`warning: ${files.length} file(s): ${why} (run \`npm run validate -- --strict\` to list as errors)`);
    }
  }
  if (errors.length) {
    console.error(`validate: ${errors.length} problem(s)\n${errors.map((e) => `  - ${e}`).join('\n')}`);
    process.exit(1);
  }
  console.log('validate: ok');
}
