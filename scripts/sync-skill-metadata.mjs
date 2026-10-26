#!/usr/bin/env node
/**
 * Merge levistack catalog metadata blocks into every skills/<group>/<name>/SKILL.md.
 * Source: skills/catalog-metadata.json (per-skill overrides + group defaults).
 *
 *   node scripts/sync-skill-metadata.mjs          # write
 *   node scripts/sync-skill-metadata.mjs --check  # exit 1 if any file would change
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { catalogSkills } from './lib/skill-evals.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const catalogPath = join(root, 'skills', 'catalog-metadata.json');
const check = process.argv.includes('--check');

const catalog = JSON.parse(readFileSync(catalogPath, 'utf8'));
const { defaults, groupCategory, skills: overrides } = catalog;

function quoteScalar(v) {
  if (typeof v === 'number' || typeof v === 'boolean') return String(v);
  const s = String(v);
  if (/[:#\[\]{}&*!|>'"@`]/.test(s) || /^\s|\s$/.test(s)) return `"${s.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
  return s;
}

function stringifyMetadata(meta) {
  const lines = ['metadata:'];
  const order = [
    'version',
    'author',
    'license',
    'group',
    'category',
    'department',
    'related_skills',
    'invokes',
    'tags',
    'capabilities',
    'languages',
  ];
  for (const key of order) {
    const val = meta[key];
    if (val === undefined || val === null) continue;
    if (key === 'invokes' && Array.isArray(val)) {
      if (!val.length) continue;
      lines.push('  invokes:');
      for (const row of val) {
        lines.push(`    - skill: ${row.skill}`);
        lines.push(`      when: ${quoteScalar(row.when)}`);
      }
      continue;
    }
    if (Array.isArray(val)) {
      if (!val.length) continue;
      lines.push(`  ${key}:`);
      for (const item of val) lines.push(`    - ${quoteScalar(item)}`);
      continue;
    }
    lines.push(`  ${key}: ${quoteScalar(val)}`);
  }
  return lines.join('\n');
}

function stripMetadataBlock(fm) {
  const lines = fm.split(/\r?\n/);
  const out = [];
  let i = 0;
  while (i < lines.length) {
    if (lines[i] === 'metadata:' || lines[i].startsWith('metadata:')) {
      i += 1;
      while (i < lines.length && (/^  /.test(lines[i]) || lines[i].trim() === '')) i += 1;
      continue;
    }
    out.push(lines[i]);
    i += 1;
  }
  return out.join('\n').replace(/\n+$/, '');
}

function readExistingVersion(raw) {
  const m = raw.match(/\nmetadata:\n  version:\s*"?([^"\n]+)"?/);
  return m ? m[1].trim() : null;
}

function buildMeta(group, name, description, existingVersion) {
  const ov = overrides[name] ?? {};
  const slug = name.replace(/-/g, '_');
  return {
    version: ov.version ?? existingVersion ?? '1.0.0',
    author: defaults.author,
    license: defaults.license,
    group,
    category: ov.category ?? groupCategory[group] ?? group,
    department: group,
    related_skills: ov.related_skills ?? [],
    invokes: ov.invokes ?? [],
    tags: ov.tags ?? [name, group],
    capabilities: ov.capabilities ?? [slug],
    languages: defaults.languages ?? ['en'],
  };
}

function rebuildSkillMd(raw, meta) {
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!m) throw new Error('missing frontmatter');
  const fm = stripMetadataBlock(m[1]);
  const newFm = `${fm}\n${stringifyMetadata(meta)}\n`;
  return `---\n${newFm}\n---\n${m[2]}`;
}

let changed = 0;
for (const { group, name, description } of catalogSkills(root)) {
  const path = join(root, 'skills', group, name, 'SKILL.md');
  const raw = readFileSync(path, 'utf8');
  const meta = buildMeta(group, name, description, readExistingVersion(raw));
  const next = rebuildSkillMd(raw, meta);
  if (next !== raw) {
    changed += 1;
    if (!check) writeFileSync(path, next, 'utf8');
  }
}

if (check && changed) {
  console.error(`sync-skill-metadata: ${changed} SKILL.md file(s) out of date; run node scripts/sync-skill-metadata.mjs`);
  process.exit(1);
}
console.log(check ? `sync-skill-metadata: ok (${catalogSkills(root).length} skills)` : `sync-skill-metadata: updated ${changed} file(s)`);
