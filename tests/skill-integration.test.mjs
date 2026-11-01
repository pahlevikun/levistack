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
  ['blast radius outside the diff', 'blast-radius'],
  ['types signatures module shape before code', 'shape-and-build'],
  ['auditable run large migration decision log', 'figure-it-out'],
  ['check optional CLIs scripts setup', 'setup-levistack'],
  ['refresh stale merge request', 'refresh-pr'],
  ['lanes under one controller digest', 'lane-lead'],
  ['compare one prompt across models', 'compare-models'],
  ['export import agent setup directory git', 'dev-environment'],
]) {
  test(`catalog search finds ${expected} for "${query}"`, () => {
    const names = rank(catalog(), query).slice(0, 3).map((skill) => skill.name);
    assert.ok(names.includes(expected), `expected ${expected} among ${names.join(', ')}`);
  });
}

test('new skills are reachable from both routing entry points', () => {
  const map = readFileSync(join(root, 'skills/workflow/find-skills/references/routing.md'), 'utf8');
  const invoke = readFileSync(join(root, 'skills/foundation/use-levistack/playbooks/invoke.md'), 'utf8');
  for (const [group, name] of [
    ['workflow', 'retrospective'], ['knowledge', 'research'],
    ['product', 'diagram'], ['product', 'infographic'],
    ['foundation', 'help-levistack'], ['foundation', 'setup-levistack'],
    ['architecture', 'shape-and-build'], ['engineering', 'blast-radius'], ['workflow', 'figure-it-out'],
    ['delivery', 'refresh-pr'], ['workflow', 'lane-lead'], ['workflow', 'compare-models'],
    ['agent-authoring', 'dev-environment'],
  ]) {
    assert.ok(existsSync(join(root, `skills/${group}/${name}/SKILL.md`)));
    assert.ok(map.includes(`\`${name}\``), `${name} is missing from routing`);
    assert.ok(invoke.includes(`\`${name}\``), `${name} is missing from invocation`);
  }
});
