import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { test } from 'node:test';
import { collect, rank } from '../skills/workflow/find-skills/scripts/catalog.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const catalog = () => collect([join(root, 'skills')]);

for (const [query, expected] of [
  ['retrospective repeated agent mistakes', 'retrospective'],
  ['primary sources research note', 'research'],
  ['questionnaire for one person', 'research'],
  ['Mermaid Excalidraw SVG diagram', 'diagram'],
  ['editorial infographic comparison', 'infographic'],
]) {
  test(`catalog search finds ${expected} for "${query}"`, () => {
    const names = rank(catalog(), query).slice(0, 3).map((skill) => skill.name);
    assert.ok(names.includes(expected), `expected ${expected} among ${names.join(', ')}`);
  });
}

test('new skills are reachable from both routing entry points', () => {
  const map = readFileSync(join(root, 'skills/workflow/find-skills/references/routing.md'), 'utf8');
  const invoke = readFileSync(join(root, 'skills/workflow/use-levistack/playbooks/invoke.md'), 'utf8');
  for (const [group, name] of [
    ['agent-authoring', 'retrospective'], ['knowledge', 'research'],
    ['product', 'diagram'], ['product', 'infographic'],
  ]) {
    assert.ok(existsSync(join(root, `skills/${group}/${name}/SKILL.md`)));
    assert.ok(map.includes(`\`${name}\``), `${name} is missing from routing`);
    assert.ok(invoke.includes(`\`${name}\``), `${name} is missing from invocation`);
  }
});
