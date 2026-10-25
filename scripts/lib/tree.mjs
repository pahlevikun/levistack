import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { parseFrontmatter } from './frontmatter.mjs';

const visible = (n) => !n.startsWith('.');
const dirs = (p) =>
  existsSync(p) ? readdirSync(p).filter((n) => visible(n) && statSync(join(p, n)).isDirectory()).sort() : [];
const mdFiles = (p, exts = ['.md']) =>
  existsSync(p)
    ? readdirSync(p).filter((n) => visible(n) && exts.some((e) => n.endsWith(e)) && n !== 'README.md').sort()
    : [];

const read = (p) => parseFrontmatter(readFileSync(p, 'utf8'));

export function scanTree(root) {
  const skillsDir = join(root, 'skills');
  const groups = dirs(skillsDir).map((g) => {
    const gdir = join(skillsDir, g);
    const descPath = join(gdir, 'DESCRIPTION.md');
    const hasDescriptionFile = existsSync(descPath);
    const descRead = hasDescriptionFile ? read(descPath) : null;
    const description = descRead?.data.description ?? '';
    const descUnsafe = descRead?.unsafe ?? [];
    const skills = dirs(gdir)
      .filter((s) => existsSync(join(gdir, s, 'SKILL.md')))
      .map((s) => {
        const { data, hasFrontmatter, unsafe } = read(join(gdir, s, 'SKILL.md'));
        return { name: s, group: g, fm: data, hasFrontmatter, unsafe };
      });
    return { name: g, description, descUnsafe, hasDescriptionFile, skills };
  });

  const collect = (sub) =>
    mdFiles(join(root, sub)).map((f) => {
      const { data, body, hasFrontmatter, unsafe } = read(join(root, sub, f));
      return { name: f.replace(/\.md$/, ''), file: f, fm: data, body, hasFrontmatter, unsafe };
    });

  // Rules: flat files or one level of source subfolders; .md (canonical) or .mdc (already Cursor format).
  const rules = [];
  const rulesDir = join(root, 'rules');
  const addRules = (dir, group) => {
    for (const f of mdFiles(dir, ['.md', '.mdc'])) {
      const raw = readFileSync(join(dir, f), 'utf8');
      const { data, body, hasFrontmatter, unsafe } = parseFrontmatter(raw);
      const ext = f.endsWith('.mdc') ? '.mdc' : '.md';
      const base = f.slice(0, -ext.length);
      rules.push({
        name: group ? `${group}/${base}` : base,
        slug: group ? `${group}-${base}` : base,
        group,
        file: group ? `${group}/${f}` : f,
        ext, raw, fm: data, body, hasFrontmatter, unsafe,
      });
    }
  };
  addRules(rulesDir, '');
  for (const g of dirs(rulesDir)) addRules(join(rulesDir, g), g);

  return { groups, agents: collect('agents'), rules, commands: collect('commands') };
}
