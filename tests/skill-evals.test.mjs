import assert from 'node:assert/strict';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { test } from 'node:test';
import {
  catalogSkills,
  readEvalFixture,
  validateSkillEvalFixtures,
} from '../scripts/lib/skill-evals.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

test('every catalog skill has evals.json or cases.json', () => {
  const errors = validateSkillEvalFixtures(root);
  assert.deepEqual(errors, [], errors.join('\n'));
});

test('catalog skill count matches fixture coverage', () => {
  const skills = catalogSkills(root);
  assert.ok(skills.length >= 40);
  let covered = 0;
  for (const s of skills) {
    if (readEvalFixture(root, s.group, s.name)) covered += 1;
  }
  assert.equal(covered, skills.length);
});

test('diagram and infographic use cases.json fixtures', () => {
  const diagram = readEvalFixture(root, 'product', 'diagram');
  const infographic = readEvalFixture(root, 'product', 'infographic');
  assert.equal(diagram?.kind, 'cases');
  assert.equal(infographic?.kind, 'cases');
  assert.ok(diagram.data.cases.length >= 5);
  assert.ok(infographic.data.cases.length >= 5);
});
